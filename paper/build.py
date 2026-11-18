"""Build the working manuscript using an installed pdfLaTeX distribution.

Run from any directory: python paper/build.py
No scientific calculations are performed by this document build.
"""
from pathlib import Path
import re
import shutil
import subprocess
import sys


def main():
    paper = Path(__file__).resolve().parent
    root = paper.parent
    build = root / ".build" / "paper"
    output = root / "output" / "pdf"
    engine = shutil.which("pdflatex")
    if engine is None:
        sys.exit("pdfLaTeX is required (for example, TinyTeX or TeX Live).")
    build.mkdir(parents=True, exist_ok=True)
    command = [engine, "-interaction=nonstopmode", "-halt-on-error",
               "-file-line-error", f"-output-directory={build}", "sixfold-draft.tex"]
    for number in range(1, 4):
        result = subprocess.run(command, cwd=paper, capture_output=True, text=True,
                                encoding="utf-8", errors="replace")
        (build / f"pass-{number}.txt").write_text(result.stdout + result.stderr,
                                                encoding="utf-8")
        if result.returncode:
            print(result.stdout[-8000:])
            sys.exit(f"pdfLaTeX failed on pass {number}; see {build}.")
    log = (build / "sixfold-draft.log").read_text(encoding="utf-8", errors="replace")
    problems = re.findall(r"^.*(?:Overfull|undefined|multiply defined|Rerun to get).*$",
                          log, flags=re.MULTILINE)
    if problems:
        print("\n".join(problems))
        sys.exit("Resolve the layout/reference warnings before exporting the PDF.")
    output.mkdir(parents=True, exist_ok=True)
    destination = output / "sixfold-draft.pdf"
    shutil.copy2(build / "sixfold-draft.pdf", destination)
    print(f"Built {destination}")


if __name__ == "__main__":
    main()
