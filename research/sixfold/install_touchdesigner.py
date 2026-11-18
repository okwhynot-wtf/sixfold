"""Run inside TouchDesigner with SIXFOLD_DIR pointing to this folder."""
from pathlib import Path
import json


def install_studio(b, folder, shader, output):
    def node(kind, name, parent=b):
        return parent.op(name) or parent.create(kind, name)

    data = json.loads((folder/"palettes.json").read_text())
    node(textDAT, "palettes").text = json.dumps(data)
    b.store("studioSourceDir", folder.as_posix())
    controls = b.par.Camera.page
    controls.name = "Motion"
    if not b.pars("Openstudio"):
        controls.appendPulse("Openstudio", label="Open studio")
    pages = {p.name:p for p in b.customPages}
    colour = pages.get("Colour") or b.appendCustomPage("Colour")
    export = pages.get("Export") or b.appendCustomPage("Export")
    if not b.pars("Palette"):
        preset = colour.appendMenu("Palette", label="Starting palette")[0]
        preset.menuNames = list(data)
        preset.menuLabels = [p["label"] for p in data.values()]
        preset.default = preset.val = "original"
        colour.appendPulse("Resetcolours", label="Reset to palette")
    names = [f"Lobe{i+1}" for i in range(6)] + ["Backdrop", "Trace"]
    rgb_defaults = data["original"]["lobes"] + [data["original"][k] for k in ("backdrop","trace")]
    labels = [f"Lobe {i+1}" for i in range(6)] + ["Background", "Winding light"]
    shader.seq.vec.numBlocks = 1+len(names)
    for i,(name,label,rgb) in enumerate(zip(names, labels, rgb_defaults)):
        if not b.pars(name+"r"):
            parts = colour.appendRGB(name, label=label)
            for part, v in zip(parts, rgb):
                part.default = part.val = v
            parts[0].startSection = i in (0,6)
        block = shader.seq.vec[i+1]
        block.par.name = "u" + (f"Lobe{i}" if i<6 else name)
        for axis, channel in zip("xyz","rgb"):
            getattr(block.par, "value"+axis).expr = "parent().par."+name+channel
    if not b.pars("Renderloop"):
        size = export.appendMenu("Moviesize", label="Movie size")[0]
        size.menuNames, size.menuLabels = ["720","1080","2160"], ["Native · max 1280","Upscale 1.5×","Upscale 3×"]
        size.default = size.val = "1080"
        fps = export.appendMenu("Moviefps", label="Frames per second")[0]
        fps.menuNames = fps.menuLabels = ["24","30","60"]
        fps.default = fps.val = "24"
        dest = export.appendFolder("Destination", label="Save folder")[0]
        dest.default = dest.val = "exports"
        export.appendPulse("Renderloop", label="Render one loop")[0].startSection = True
        export.appendPulse("Cancelrender", label="Cancel render")[0].enable = False
        status = export.appendStr("Exportstatus", label="Status")[0]
        status.val = "Ready"
        status.readOnly = True
        export.appendFile("Lastmovie", label="Last movie")[0].readOnly = True
        export.appendPulse("Showfolder", label="Open save folder")
    if not b.pars("Aspect"):
        aspect = export.appendMenu("Aspect", label="Aspect ratio")[0]
        aspect.menuNames = ["wide", "square", "portrait"]
        aspect.menuLabels = ["16:9 · Landscape", "1:1 · Square", "9:16 · Portrait"]
        aspect.default = aspect.val = "wide"
        export.appendStr("Outputpixels", label="Render → export")[0].readOnly = True
    size = b.par.Moviesize
    previous_size = size.eval()
    size.menuNames = ["720","1080","2160"]
    size.menuLabels = ["Native · max 1280","Upscale 1.5×","Upscale 3×"]
    size.val = previous_size
    export.sort("Aspect","Moviesize","Outputpixels","Moviefps","Destination","Renderloop",
                "Cancelrender","Exportstatus","Lastmovie","Showfolder")
    b.sortCustomPages("Colour", "Motion", "Export")

    studio = node(containerCOMP, "studio")
    studio.par.w, studio.par.h = 1200, 500
    preview = node(containerCOMP, "preview", studio)
    preview.par.w, preview.par.h, preview.par.top = 800, 500, output
    preview.par.topfill, preview.par.bgalpha = "best", 1.
    editor = node(parameterCOMP, "settings", studio)
    editor.par.x, editor.par.w, editor.par.h = 800, 400, 500
    editor.par.op, editor.par.builtin, editor.par.custom = b, False, True
    editor.par.header, editor.par.pagenames, editor.par.allowexpand = False, True, False
    editor.par.pagescope, editor.par.syncpage = "Colour Motion Export", True
    win = node(windowCOMP, "studio_window")
    win.par.winop, win.par.title = studio, "Sixfold Studio"
    win.par.justifyh, win.par.justifyv, win.par.borders = "center","center",True
    win.par.cursorvisible = "alwaysvisible"
    actions = node(textDAT, "studio_actions")
    actions.text = (folder/"studio_actions.py").read_text(encoding="utf8")
    events = node(parameterexecuteDAT, "studio_events")
    events.par.op = b
    events.par.pars = "Palette Aspect Moviesize Resetcolours Openstudio Renderloop Cancelrender Showfolder"
    events.par.valuechange, events.par.onpulse = True, True
    events.text = """def onValueChange(par, prev):
    if par.name == 'Palette':
        parent().op('studio_actions').module.apply_palette()
    elif par.name in ('Aspect','Moviesize'):
        parent().op('studio_actions').module.update_format()

def onPulse(par):
    actions = parent().op('studio_actions').module
    callbacks = {'Resetcolours':actions.apply_palette, 'Openstudio':actions.open_studio,
                 'Renderloop':actions.start, 'Cancelrender':actions.cancel, 'Showfolder':actions.show_folder}
    if par.name in callbacks:
        callbacks[par.name]()
"""
    startup = node(executeDAT, "studio_start")
    startup.par.start = True
    startup.text = """def onStart():
    run("op(args[0]).module.on_start()", parent().op('studio_actions').path, delayFrames=3)
"""
    for i, item in enumerate((studio,win,actions,events,startup,b.op("palettes"))):
        item.nodeX, item.nodeY = -240+160*(i%3), -240-120*(i//3)
    b.currentPage = "Colour"
    shader.par.resolutionw.expr = "720 if parent().par.Aspect == 'portrait' else 1280"
    shader.par.resolutionh.expr = "720 if parent().par.Aspect == 'wide' else 1280"
    actions.module.update_format()


def install(folder):
    root = op("/project1")
    base = root.op("Sixfold") or root.create(baseCOMP, "Sixfold")
    base.nodeX, base.nodeY = 320, 60
    if not base.pars("Camera"):
        page = base.appendCustomPage("Sixfold")
        page.appendMenu("Camera")
        clock = page.appendMenu("Clock")[0]
        clock.menuNames, clock.menuLabels = ["live", "manual"], ["Live", "Scrub"]
        phase = page.appendFloat("Phase")[0]
        phase.min, phase.max, phase.clampMin, phase.clampMax = 0., 1., True, True
        seconds = page.appendFloat("Seconds", label="Loop seconds")[0]
        seconds.min, seconds.max, seconds.clampMin = 5., 120., True
        seconds.default = seconds.val = 48.
        exposure = page.appendFloat("Exposure")[0]
        exposure.min, exposure.max, exposure.clampMin = .2, 3., True
        exposure.default = exposure.val = 1.
    camera = base.par.Camera
    camera.menuNames = ["tour", "passages", "descent", "winding"]
    camera.menuLabels = ["Tour", "Twin passages", "Endless descent", "Winding light"]
    if base.pars("Material"):
        base.par.Material.destroy()
    def data_texture(name, filename, dimensions):
        node = base.op(name) or base.create(moviefileinTOP, name)
        node.lock = False
        node.par.file = (folder/filename).as_posix()
        node.par.inputcolorspace = "passthrough"
        node.par.play = False
        node.par.reloadpulse.pulse()
        node.cook(force=True)
        if (node.width, node.height) != dimensions:
            raise RuntimeError(f"{filename} has unexpected resolution")
        node.lock = True
        return node
    atlas = data_texture("reference_field", "field.png", (1152,768))
    curve = data_texture("contact_chords", "contact_curve.png", (27,120))

    shader = base.op("sculpture") or base.create(glslTOP, "sculpture")
    shader.par.pixeldat.eval().text = (
        "#define SIXFOLD_METAL_ONLY\n#define FIELD sTD2DInputs[0]\n#define CURVE sTD2DInputs[1]\n" + (folder/"reference.glsl").read_text()
        + (folder/"sculpture.frag").read_text()
        + "\nlayout(location=0) out vec4 fragColor;\n"
        + "void main(){fragColor=TDOutputSwizzle(vec4(render(vUV.st),1.));}")
    shader.inputConnectors[0].connect(atlas)
    shader.inputConnectors[1].connect(curve)
    shader.par.outputresolution = "custom"
    shader.par.resolutionw, shader.par.resolutionh = 1280, 720
    shader.par.inputfiltertype = "linear"
    shader.par.vec0name = "uView"
    shader.par.vec0valuex.expr = ("parent().par.Phase if parent().par.Clock == 'manual' "
                                  "else absTime.seconds / parent().par.Seconds")
    shader.par.vec0valuey.expr = "parent().par.Camera.menuIndex"
    shader.par.vec0valuez.expr = "parent().par.Exposure"
    shader.par.vec0valuew.expr = "me.par.resolutionw / me.par.resolutionh"
    output = base.op("view") or base.create(nullTOP, "view")
    output.inputConnectors[0].connect(shader)
    base.par.opviewer = output
    atlas.nodeX, atlas.nodeY = -240, 80
    curve.nodeX, curve.nodeY = -240, -70
    shader.nodeX, shader.nodeY = 0, 80
    shader.par.pixeldat.eval().nodeX, shader.par.pixeldat.eval().nodeY = 0, -70
    output.nodeX, output.nodeY = 230, 80
    output.viewer = base.viewer = True
    install_studio(base, folder, shader, output)
    shader.cook(force=True)
    return base


install(Path(SIXFOLD_DIR))
