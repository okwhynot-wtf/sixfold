"""Callbacks embedded in Sixfold's studio_actions Text DAT."""
import json
import os
from datetime import datetime
from pathlib import Path
import shutil
import subprocess
import tempfile


def owner():
    return me.parent()


def apply_palette():
    b = owner()
    data = json.loads(b.op("palettes").text)[b.par.Palette.eval()]
    for i, rgb in enumerate(data["lobes"]):
        getattr(b.parGroup, f"Lobe{i+1}").val = tuple(rgb)
    b.parGroup.Backdrop.val = tuple(data["backdrop"])
    b.parGroup.Trace.val = tuple(data["trace"])


def folder():
    value = Path(tdu.expandPath(owner().par.Destination.eval()))
    return (Path(project.folder) / value).resolve()


def show_folder():
    destination = folder()
    destination.mkdir(parents=True, exist_ok=True)
    os.startfile(str(destination))


def set_state(text, busy):
    b = owner()
    b.par.Exportstatus.val = text
    b.par.Renderloop.enable = not busy
    b.par.Cancelrender.enable = busy


def output_dimensions():
    b = owner()
    width, height = {"wide": (1280,720), "square": (1280,1280),
                     "portrait": (720,1280)}[b.par.Aspect.eval()]
    factor = {"720": 1., "1080": 1.5, "2160": 3.}[b.par.Moviesize.eval()]
    return width, height, factor


def update_format():
    width, height, factor = output_dimensions()
    label = f"{width} × {height}"
    if factor != 1:
        label += f" → {round(width*factor)} × {round(height*factor)}"
    owner().par.Outputpixels.val = label


def start():
    b = owner()
    if b.fetch("studioJob", None, search=False):
        return
    try:
        destination = folder()
        destination.mkdir(parents=True, exist_ok=True)
        source = Path(project.folder)
        if not (source/"render_film.py").is_file():
            source = Path(b.fetch("studioSourceDir"))
        if not (source/"render_film.py").is_file():
            raise FileNotFoundError("Keep render_film.py and its assets in the Sixfold folder.")
        uv = shutil.which("uv") or str(Path.home()/".local/bin/uv.exe")
        if not Path(uv).is_file():
            raise FileNotFoundError("The Sixfold movie exporter needs uv.")
        width, height, factor = output_dimensions()
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        target = destination/f"Sixfold-{b.par.Camera.eval()}-{stamp}.mp4"
        temp = tempfile.TemporaryDirectory(prefix="sixfold-job-")
        snap = Path(temp.name)/"settings.json"
        data = {"lobes": [list(getattr(b.parGroup, f"Lobe{i+1}").eval()) for i in range(6)],
                "backdrop": list(b.parGroup.Backdrop.eval()), "trace": list(b.parGroup.Trace.eval()),
                "exposure": b.par.Exposure.eval()}
        snap.write_text(json.dumps(data), encoding="utf8")
        phase = b.par.Phase.eval() if b.par.Clock.eval()=="manual" else 0.
        command = [uv, "run", "--python", "3.12", "--with", "pillow", "--with", "moderngl",
                   "--with", "imageio-ffmpeg", "python", str(source/"render_film.py"), str(target),
                   "--mode", str(b.par.Camera.menuIndex), "--phase", str(phase),
                   "--width", str(width), "--height", str(height), "--fps", b.par.Moviefps.eval(),
                   "--seconds", str(b.par.Seconds.eval()), "--upscale", str(factor), "--settings", str(snap)]
        log = Path(temp.name)/"render.log"
        with log.open("wb") as stream:
            process = subprocess.Popen(command, cwd=source, stdout=stream, stderr=subprocess.STDOUT,
                                       stdin=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
        # Runtime-only objects belong to the DAT module, never serialized OP storage.
        global job
        job = (process, temp, snap, target, log)
        b.store("studioJob", process.pid)
        b.storeStartupValue("studioJob", None)
        set_state("Starting export…", True)
        poll()
    except Exception as exc:
        set_state(f"Export failed · {exc}", False)


def poll():
    b = owner()
    if not b.fetch("studioJob", None, search=False):
        return
    process, temp, snap, target, log = job
    code = process.poll()
    with log.open("rb") as stream:
        stream.seek(max(0, log.stat().st_size-4096))
        lines = stream.read().decode("utf8", errors="replace").splitlines()
    if code is None:
        progress = next((line for line in reversed(lines) if "/" in line and
                         all(part.isdigit() for part in line.split("/", 1))), "")
        if progress and not snap.with_suffix(".cancel").exists():
            current, total = map(int, progress.split("/"))
            set_state(f"Rendering {100*current/total:.0f}%  ·  {current}/{total} frames", True)
        run("op(args[0]).module.poll()", me.path, delayMilliSeconds=350, wallTime=True)
        return
    if code==0 and target.is_file():
        b.par.Lastmovie = target.as_posix()
        message = f"Saved · {target.name}"
    elif snap.with_suffix(".cancel").exists():
        message = "Cancelled"
    else:
        message = "Export failed · " + (lines[-1] if lines else f"exit code {code}")
    b.unstore("studioJob")
    temp.cleanup()
    set_state(message, False)


def cancel():
    if owner().fetch("studioJob", None, search=False):
        job[2].with_suffix(".cancel").touch()
        set_state("Cancelling…", True)


def open_studio():
    owner().op("studio_window").par.winopen.pulse()


def on_start():
    set_state("Ready", False)
    update_format()
    open_studio()
