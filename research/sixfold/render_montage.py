"""Edit all four views, with a continuous descent through the final 100 seconds."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

import imageio_ffmpeg

HERE = Path(__file__).resolve().parent
FPS = 30
# name, camera, duration, initial phase, phase advance
# The descent sections all follow phase = (montage_time - 14) / 32.
SHOTS = [
    ("Orbit", 0, 14, 0., .27),
    ("Twin passages", 1, 10, .27, 0.),
    ("Endless descent", 2, 64, 0., 2.),
    ("Winding light", 3, 24, 62/32, 24/32),
    ("Endless descent finale", 2, 16, 84/32, 16/32),
]
STARTS = [0, 12, 14, 76, 98]
LENGTH = 114


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--settings", type=Path, required=True)
    parser.add_argument("--work", type=Path, help="Retain rendered shots for review or revisions")
    parser.add_argument("--aspect", choices=["wide", "square", "portrait"], default="wide")
    parser.add_argument("--upscale", type=float, choices=[1., 1.5, 3.], default=1.5)
    args = parser.parse_args()
    width, height = {"wide": (1280,720), "square": (1280,1280), "portrait": (720,1280)}[args.aspect]
    out_width, out_height = round(width*args.upscale), round(height*args.upscale)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = TemporaryDirectory(prefix="sixfold-montage-") if not args.work else None
    work = args.work or Path(temporary.name)
    work.mkdir(parents=True, exist_ok=True)
    # Cache only sources made with the same shader, frame rate and colours.
    import hashlib
    signature = hashlib.sha256(
        args.settings.read_bytes() + (HERE/"sculpture.frag").read_bytes()
        + (HERE/"render_film.py").read_bytes()
        + (HERE/"gpu_renderer.py").read_bytes()
        + (HERE/"reference.glsl").read_bytes() + (HERE/"field.png").read_bytes()
        + (HERE/"contact_curve.png").read_bytes()
        + json.dumps([SHOTS, FPS, width, height]).encode()
    ).hexdigest()
    receipt = work/"source_signature.txt"
    reuse = receipt.is_file() and receipt.read_text() == signature
    clips = []
    for i,(name, mode, seconds, phase, cycles) in enumerate(SHOTS):
        path = work/f"{i+1:02d}.mp4"
        clips.append(path)
        if reuse and path.is_file():
            print(f"Using completed {name}", flush=True)
            continue
        print(f"Rendering {name}", flush=True)
        subprocess.run([
            sys.executable, str(HERE/"render_film.py"), str(path),
            "--width", str(width), "--height", str(height), "--fps", str(FPS),
            "--seconds", str(seconds), "--phase", str(phase), "--cycles", str(cycles),
            "--mode", str(mode), "--settings", str(args.settings),
        ], check=True)
    receipt.write_text(signature)
    filters = [f"[{i}:v]" + ("trim=duration=4," if i==1 else "")
               + f"settb=AVTB,setpts=PTS-STARTPTS,format=yuv444p[s{i}]" for i in range(5)]
    previous = "s0"
    for i, start in enumerate(STARTS[1:], start=1):
        filters.append(f"[{previous}][s{i}]xfade=transition=fade:duration=2:offset={start}[d{i}]")
        previous = f"d{i}"
    filters.append(
        f"[{previous}]fade=t=in:st=0:d=1,fade=t=out:st={LENGTH-1.5}:d=1.5,"
        f"scale={out_width}:{out_height}:flags=lanczos,setsar=1,"
        "unsharp=5:5:0.16:3:3:0,format=yuv420p[out]"
    )
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    command = [ffmpeg, "-hide_banner", "-loglevel", "error", "-y"]
    for clip in clips:
        command.extend(["-threads", "1", "-i", str(clip)])
    partial = args.output.with_suffix(".partial.mp4")
    command += [
        "-filter_complex_threads", "2", "-filter_complex", ";".join(filters),
        "-map", "[out]", "-an", "-frames:v", str(FPS*LENGTH),
        "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-profile:v", "high", "-threads", "4",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-r", str(FPS),
        "-metadata", "title=Sixfold - Endless Descent",
        "-metadata", f"comment={width}x{height} source, FFmpeg Lanczos scale to {out_width}x{out_height}",
        str(partial)
    ]
    print(f"Editing transitions and scaling to {out_width} × {out_height}", flush=True)
    subprocess.run(command, check=True)
    partial.replace(args.output)
    print(f"Saved {args.output}", flush=True)
    if temporary:
        temporary.cleanup()


if __name__ == "__main__":
    main()
