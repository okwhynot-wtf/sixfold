"""Render stills or a seamless silent film with the same shader as TouchDesigner."""
import argparse
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

import moderngl as gl
from PIL import Image

HERE = Path(__file__).resolve().parent
VERTEX = """#version 430
out vec2 uv;
void main() {
    uv = vec2((gl_VertexID << 1) & 2, gl_VertexID & 2);
    gl_Position = vec4(uv*2.-1.,0.,1.);
}
"""


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
    parser.add_argument("--mode", type=int, choices=[0,1,2,3], default=0)
    parser.add_argument("--material", choices=["metal","glass","compare"], default="metal")
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--seconds", type=float, default=48)
    parser.add_argument("--settings", type=Path, help="Colour and exposure snapshot from Sixfold Studio")
    args = parser.parse_args()
    if args.upscale != 1. and args.output.suffix.lower() != ".mp4":
        parser.error("--upscale applies to MP4 movies. Choose --width and --height for still images.")
    size = args.width, args.height
    ctx = gl.create_standalone_context(require=430)
    metal_define = "#define SIXFOLD_METAL_ONLY\n" if args.material == "metal" else ""
    shader = ("#version 430\n" + metal_define + "uniform sampler2D atlasMap, curveMap;\n#define FIELD atlasMap\n#define CURVE curveMap\n"
              "in vec2 uv; out vec4 frag;\n" + (HERE/"reference.glsl").read_text()
              + (HERE/"sculpture.frag").read_text()
              + "\nvoid main(){frag=vec4(render(uv),1.);}\n")
    program = ctx.program(vertex_shader=VERTEX, fragment_shader=shader)
    if args.material != "metal":
        program["uFinish"].value = (("metal","glass","compare").index(args.material),0.,0.,0.)
    colours = (json.loads(args.settings.read_text(encoding="utf8")) if args.settings
               else json.loads((HERE/"palettes.json").read_text())["original"])
    for i, rgb in enumerate(colours["lobes"]):
        program[f"uLobe{i}"].value = (*rgb, 1.)
    program["uBackdrop"].value = (*colours["backdrop"], 1.)
    program["uTrace"].value = (*colours["trace"], 1.)
    exposure = colours.get("exposure", 1.)
    atlas = Image.open(HERE/"field.png").convert("RGB").transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    tex = ctx.texture(atlas.size, 3, atlas.tobytes(), alignment=1)
    tex.filter = (gl.LINEAR, gl.LINEAR)
    tex.use()
    curve = Image.open(HERE/"contact_curve.png").convert("RGB").transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    curve_tex = ctx.texture(curve.size, 3, curve.tobytes(), alignment=1)
    curve_tex.filter = (gl.NEAREST, gl.NEAREST)
    curve_tex.use(1)
    program["curveMap"].value = 1
    render_size = tuple(v*args.supersample for v in size)
    color = ctx.texture(render_size, 4)
    color.filter = (gl.LINEAR, gl.LINEAR)
    scene = ctx.framebuffer(color_attachments=[color])
    vao = ctx.vertex_array(program, [])
    output = scene
    if args.supersample == 2:
        output = ctx.simple_framebuffer(size, components=4)
        downsample = ctx.program(vertex_shader=VERTEX, fragment_shader="""#version 430
            uniform sampler2D source;
            in vec2 uv; out vec4 frag;
            void main(){frag=texture(source,uv);}
        """)
        downsample["source"].value = 2
        resolve = ctx.vertex_array(downsample, [])

    def frame(phase):
        program["uView"].value = phase, args.mode, exposure, args.width/args.height
        scene.use()
        vao.render(vertices=3)
        if args.supersample == 2:
            output.use()
            color.use(2)
            resolve.render(vertices=3)
        return output.read(components=3, alignment=1)

    if args.output.suffix.lower() != ".mp4":
        Image.frombytes("RGB",size,frame(args.phase)).transpose(Image.Transpose.FLIP_TOP_BOTTOM).save(args.output)
        return
    import imageio_ffmpeg
    video_filter = "vflip"
    if args.upscale != 1.:
        scaled_width, scaled_height = (round(v*args.upscale/2)*2 for v in size)
        video_filter += f",scale={scaled_width}:{scaled_height}:flags=lanczos,setsar=1"
    command = [imageio_ffmpeg.get_ffmpeg_exe(),"-hide_banner","-loglevel","error","-y","-f","rawvideo",
               "-pix_fmt","rgb24","-s",f"{args.width}x{args.height}","-r",str(args.fps),
               "-i","-","-vf",video_filter,"-an","-c:v","libx264","-preset","fast",
               "-crf","17","-pix_fmt","yuv420p","-movflags","+faststart"]
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


if __name__ == "__main__":
    main()
