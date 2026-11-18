"""Render stills or a seamless silent film with the same shader as TouchDesigner."""
import argparse
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

from gpu_renderer import Renderer
from PIL import Image

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=720)
    parser.add_argument("--supersample", type=int, choices=[1,2], default=1)
    parser.add_argument("--upscale", type=float, choices=[1.,1.5,3.], default=1.,
                        help="FFmpeg output scaling after rendering at the requested resolution")
    parser.add_argument("--phase", type=float, default=0.)
    parser.add_argument("--cycles", type=float, default=1., help="Camera cycles during the rendered clip")
    parser.add_argument("--mode", type=int, choices=[0,1,2,3,4,5], default=0)
    parser.add_argument("--material", choices=["metal","glass","compare"], default="metal")
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--seconds", type=float, default=48)
    parser.add_argument("--settings", type=Path, help="Colour and exposure snapshot from Sixfold Studio")
    args = parser.parse_args()
    if args.upscale != 1. and args.output.suffix.lower() != ".mp4":
        parser.error("--upscale applies to MP4 movies. Choose --width and --height for still images.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    size = args.width, args.height
    renderer = Renderer(args.width,args.height,args.supersample,args.material)
    if args.settings:
        renderer.colours(json.loads(args.settings.read_text(encoding="utf8")))
    def frame(phase):
        return renderer.frame(phase,args.mode)

    if args.output.suffix.lower() != ".mp4":
        Image.frombytes("RGB",size,frame(args.phase)).transpose(Image.Transpose.FLIP_TOP_BOTTOM).save(args.output)
        renderer.close()
        return
    import imageio_ffmpeg
    video_filter = "vflip"
    if args.upscale != 1.:
        scaled_width, scaled_height = (round(v*args.upscale/2)*2 for v in size)
        video_filter += f",scale={scaled_width}:{scaled_height}:flags=lanczos,setsar=1"
    command = [imageio_ffmpeg.get_ffmpeg_exe(),"-hide_banner","-loglevel","error","-y","-f","rawvideo",
               "-pix_fmt","rgb24","-s",f"{args.width}x{args.height}","-r",str(args.fps),
               "-i","-","-filter_threads","2","-vf",video_filter,"-an","-c:v","libx264","-preset","fast",
               "-crf","17","-threads","4","-pix_fmt","yuv420p","-movflags","+faststart"]
    count = max(1, round(args.fps*args.seconds))
    cancel = args.settings.with_suffix(".cancel") if args.settings else None
    with TemporaryDirectory(prefix=".sixfold-", dir=args.output.parent) as work:
        partial = Path(work)/"movie.mp4"
        with subprocess.Popen(command+[str(partial)], stdin=subprocess.PIPE) as encoder:
            for i in range(count):
                if cancel and cancel.exists():
                    raise SystemExit(2)
                encoder.stdin.write(frame(args.phase+args.cycles*i/count))
                if i % args.fps == 0 or i+1 == count:
                    print(f"{i+1}/{count}", flush=True)
            encoder.stdin.close()
            if encoder.wait():
                raise RuntimeError("Video encoding failed")
        partial.replace(args.output)
    renderer.close()


if __name__ == "__main__":
    main()
