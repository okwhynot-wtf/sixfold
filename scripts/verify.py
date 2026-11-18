"""Reproduce current scientific implementation checks in a temporary copy."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
CHECKS = [
    ("Handover integrity, contacts, packings and rotations", "fractal_handover/verify_handover.py"),
    ("Reference exact-dimension premises", "fractal_research_08/verify_reference.py"),
    ("Second member exact-dimension premises", "fractal_research_08/verify_member.py"),
    ("Central passage", "fractal_research_08/verify_tunnel.py"),
    ("Two independent passages", "fractal_research_09/verify_tunnels.py"),
    ("Tilted bore and shrinking-loop premises", "fractal_research_10_topology/verify.py"),
]


def source_digest():
    digest = hashlib.sha256()
    paths = sorted((ROOT / "research").rglob("*"),
                   key=lambda path: path.relative_to(ROOT).as_posix())
    for path in paths:
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
            digest.update(path.relative_to(ROOT).as_posix().encode())
            digest.update(b"\0")
            digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def main():
    if not __debug__:
        raise RuntimeError("Assertions must be enabled. Run without -O.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    receipt = {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "research_sha256": source_digest(),
        "scope": "Reproduces symbolic, integer and interval checks. Analytic deductions and theorem applications await independent mathematical review.",
        "checks": [],
        "passed": False,
    }
    env = os.environ.copy()
    env.pop("PYTHONOPTIMIZE", None)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    started = time.perf_counter()
    try:
        with tempfile.TemporaryDirectory(prefix="sixfold_verify_") as directory:
            work = Path(directory) / "research"
            shutil.copytree(ROOT / "research", work,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            for label, relative in CHECKS:
                print(f"Running {label} ...", flush=True)
                stage_start = time.perf_counter()
                result = subprocess.run(
                    [sys.executable, "-B", str(work / relative)],
                    cwd=work, env=env, capture_output=True, text=True,
                    encoding="utf-8", errors="replace",
                )
                receipt["checks"].append({
                    "label": label, "script": relative,
                    "passed": result.returncode == 0,
                    "seconds": round(time.perf_counter() - stage_start, 3),
                    "stdout": result.stdout, "stderr": result.stderr,
                })
                if result.returncode:
                    print(result.stdout, file=sys.stderr)
                    print(result.stderr, file=sys.stderr)
                    raise RuntimeError(f"Verification failed at {relative}")
                print(f"PASS {label}", flush=True)
        receipt["passed"] = True
    finally:
        receipt["seconds"] = round(time.perf_counter() - started, 3)
        if args.receipt:
            args.receipt.parent.mkdir(parents=True, exist_ok=True)
            args.receipt.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print("All current implementation checks passed.", flush=True)


if __name__ == "__main__":
    main()
