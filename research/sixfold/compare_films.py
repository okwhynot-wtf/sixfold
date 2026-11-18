"""Pair the two 1280 x 720 tour exports using identical crops and timing."""
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent


def main():
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    with TemporaryDirectory() as work:
        label = Image.new("RGB", (1600, 48), "#070c10")
        draw = ImageDraw.Draw(label)
        try:
            font = ImageFont.truetype("segoeui.ttf", 20)
        except OSError:
            font = ImageFont.load_default(size=20)
        for x, name in [(400, "Brushed metal"), (1200, "Glass")]:
            draw.text((x, 23), name, font=font, fill="#d6e1e1", anchor="mm")
        footer = Path(work)/"labels.png"
        label.save(footer)
        target = HERE/"Metal-and-glass.mp4"
        # Write alongside the target so replacing a prior export is atomic.
        partial = target.with_suffix(".partial.mp4")
        graph = ("[0:v]crop=800:720,setsar=1[l];[1:v]crop=800:720,setsar=1[r];"
                 "[l][r]hstack=shortest=1,drawbox=x=799:y=0:w=2:h=ih:c=0x131b20:t=fill[pair];"
                 "[pair][2:v]vstack=inputs=2:shortest=1[out]")
        subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
                        "-i", str(HERE/"Sixfold.mp4"), "-i", str(HERE/"Sixfold-glass.mp4"),
                        "-loop", "1", "-framerate", "24", "-i", str(footer),
                        "-filter_complex", graph, "-map", "[out]", "-an", "-c:v", "libx264",
                        "-crf", "17", "-preset", "fast", "-pix_fmt", "yuv420p",
                        "-movflags", "+faststart", str(partial)], check=True)
        partial.replace(target)
        subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-ss", "13",
                        "-i", str(target), "-frames:v", "1",
                        str(HERE/"Metal-and-glass.png")], check=True)


if __name__ == "__main__":
    main()
