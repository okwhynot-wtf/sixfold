# Sixfold

Open **Sixfold.toe**. **Sixfold Studio** displays the original metal sculpture with live controls. To reopen the window, select **/project1/Sixfold**, choose **Motion**, and pulse **Open studio**. **F1** shows the clean artwork in Perform Mode. **Esc** returns to the network.

## Colour and motion

In **Colour**, choose a starting palette. Click a swatch to edit any of the six lobes, the background, or the illuminated path used by Winding light. **Reset to palette** restores the selected preset. **Original copper & teal** restores the original colours.

In **Motion**, choose a camera and set **Loop seconds** and **Exposure**. **Clock → Scrub** makes the **Phase** slider the playhead. Scrub is useful for comparing colours at a fixed view. Save the TouchDesigner project to keep your edits.

## Export a movie from the panel

1. Set the camera and loop duration in **Motion**.
2. In **Export**, choose **Aspect ratio**, **Movie size**, frame rate, and save folder. **Render → export** shows the actual dimensions. Choose **Native · max 1280** to keep the rendered resolution, or **Upscale 1.5× / 3×** for FFmpeg enlargement. The initial defaults are landscape, 1.5×, 24 fps, and **exports** beside the project.
3. Pulse **Render one loop**. **Status** shows progress. The exporter snapshots the current colours, camera and exposure. **Live** starts at phase zero. **Scrub** starts at the chosen phase and renders a complete cycle.
4. When **Status** says **Saved**, pulse **Open save folder**. Each render receives a new timestamped filename. At the defaults, the silent H.264 MP4 contains 1,152 frames over 48 seconds. **Cancel render** discards the unfinished movie.

| Aspect ratio | Native render | FFmpeg 1.5× | FFmpeg 3× |
| --- | --- | --- | --- |
| 16:9 Landscape | 1280 × 720 | 1920 × 1080 | 3840 × 2160 |
| 1:1 Square | 1280 × 1280 | 1920 × 1920 | 3840 × 3840 |
| 9:16 Portrait | 720 × 1280 | 1080 × 1920 | 2160 × 3840 |

The live preview follows the selected aspect ratio. Portrait framing fits the full assembly during the opening orbit and eases into a close-up during the descent.

The panel launches the project's GPU renderer and FFmpeg through `uv` in the background. Native dimensions stay within the [TouchDesigner Non-Commercial 1280 × 1280 limit](https://docs.derivative.ca/TouchDesigner_Non-Commercial). Enlargement happens afterward in FFmpeg using Lanczos; it does not add geometric detail. The clean movie includes only the artwork. Keep the Sixfold source files and lookup textures alongside the project when moving it to another folder.

**exports/Sixfold-Endless-Descent-1080p-revised.mp4** is the revised 1:54 montage of all four modes. Six seconds have been removed from the stationary Twin passages view near 12 seconds. It includes a 64-second Endless Descent shot and returns to that view at the end. Square and portrait versions are **Sixfold-Endless-Descent-square.mp4** and **Sixfold-Endless-Descent-portrait.mp4** in the same folder. They use the original copper-and-teal colours captured in **montage_colours.json**, 30 fps, and a 32-second camera cycle during the descent. Each uses the native dimensions above and FFmpeg's 1.5× Lanczos enlargement. The movies are silent. The original two-minute landscape edit is also retained.

## Still images

The renderer can save a lossless PNG at any camera phase, in any of the three aspect ratios. A phase is a position within the camera cycle, not a timestamp in seconds. Choose **Clock → Scrub** and **Phase** to find a composition. Stills can be made later with the same colours and exposure as the movies; no separate scene is needed. The command-line renderer accepts a PNG filename instead of an MP4:

```powershell
uv run --python 3.12 --with pillow --with moderngl --with imageio-ffmpeg python sixfold/render_film.py sixfold/exports/Descent-still.png --mode 2 --phase 0.75 --width 1280 --height 720 --settings sixfold/montage_colours.json
```

This example uses the montage palette. The movie panel snapshots your current custom colours automatically; its current **Render one loop** button exports a movie.

| Camera | What to watch |
| --- | --- |
| Tour | A 48-second orbit aligns the two passages, moves into the upper lobe, and returns. The exported film is **Sixfold.mp4**. |
| Twin passages | A fixed orthographic sight line along the two phase-09 axes. Amber and teal distinguish the two opposite lobes. |
| Endless descent | A logarithmic zoom follows the repeated address 0. One cycle spans four generations. The renderer blends adjacent coordinate frames to maintain detail at the same apparent scale. |
| Winding light | The same descent carries an illuminated contact path. Four generations take one highlighted loop to the next. **Winding-light.mp4** plays this study in 32 seconds. |

## Research and rendering

The six similarities come from the handover’s phase-07 `geometry.maps()` at the reference height. The field samples all 1,679,616 depth-eight word centres. The shader applies four outer maps and lights a thin finite-resolution envelope of that field. Surface thickness, material, exposure and view-dependent lighting are artistic choices.

The earlier glass experiment is preserved in **Sixfold-glass.mp4** and **Metal-and-glass.mp4**.

The parallel passages are the phase-09 lines through opposite lobe centres, directed along (−1, 0, 1). Phase 10’s first intrusion concerns the different, inherited tilted bore. The winding overlay uses the phase-09 chain of 1,434 chords in the upper lobe and the phase-10 sequence obtained by applying four copies of map 0 at each step. The path is drawn through foreground material so its projected course stays legible. Finer loops tend toward the fixed point of map 0.

Current research incorporated into the cameras is [phase 09](../fractal_research_09/RESEARCH_09.md) and [phase 10](../fractal_research_10_topology/RESEARCH_10.md). Future research can change the camera, curves or geometry independently.

## Updating this study

Run the relevant build step from the workspace root after a geometry or path change. The shaders, controls, presets and both lookup textures used for the live view are embedded in the saved TouchDesigner project. Palette definitions for future builds are in **palettes.json**.

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
uv run --python 3.12 --with-requirements fractal_handover/requirements.txt python sixfold/build_field.py
uv run --python 3.12 --with-requirements fractal_handover/requirements.txt python sixfold/build_curve.py
uv run --python 3.12 --with pillow --with moderngl --with imageio-ffmpeg python sixfold/render_film.py sixfold/Sixfold.mp4 --fps 24 --seconds 48
uv run --python 3.12 --with pillow --with moderngl --with imageio-ffmpeg python sixfold/render_film.py sixfold/Sixfold-glass.mp4 --material glass --fps 24 --seconds 48 --supersample 2
uv run --python 3.12 --with pillow --with imageio-ffmpeg python sixfold/compare_films.py
uv run --python 3.12 --with pillow --with moderngl --with imageio-ffmpeg python sixfold/render_film.py sixfold/Winding-light.mp4 --mode 3 --fps 24 --seconds 32
uv run --python 3.12 --with pillow --with moderngl --with imageio-ffmpeg python sixfold/render_montage.py sixfold/exports/Sixfold-Endless-Descent-1080p.mp4 --settings sixfold/montage_colours.json
```

To refresh the component in the open Sixfold project, run this in the TouchDesigner textport or through its MCP Python tool. Save after checking the output. The installer preserves existing camera settings.

```python
from pathlib import Path
SIXFOLD_DIR = Path(project.folder)
exec(compile((SIXFOLD_DIR / "install_touchdesigner.py").read_text(), "install_touchdesigner.py", "exec"))
```
