# Images and films

![Sixfold in copper and teal](../site/assets/sixfold.png)

The [edition-01 gallery](../research/sixfold/assets/2026-11-18-library/index.html)
contains all **100 compositions and six films**: 34 landscape stills, 33 square
stills and 33 portrait stills, plus two films in each format. Each still has
a full-size JPEG and a lossless native PNG master.

The homepage features **Chromatic descent**, a 48-second loop through evolving
colours. **Through the passage** is a 36-second journey along the certified
phase-09 passage, turning back toward the sculpture. All six films are silent.

[Download the visualisation edition](https://github.com/okwhynot-wtf/sixfold/releases/tag/visuals-2026-11-18).
The six original MP4s are release attachments. The release's source archive
includes the TouchDesigner project, rendering source, all stills and masters,
posters, contact sheets, catalogue and render recipes.

## Credit and reuse

Images and films are by **okwhynot-wtf**, with substantial GPT assistance,
and are available under [CC BY 4.0](../CONTENT-LICENSE.md).
Code and the TouchDesigner project use [MIT](../LICENSE).
For a shared image or film, credit "Sixfold — okwhynot-wtf, CC BY 4.0", link
to this project and the licence, and identify any changes.

## Resolution and recipes

| Format | Native render / PNG master | Delivered JPEG / MP4 |
| --- | --- | --- |
| Landscape | 1280 × 720 | 1920 × 1080 |
| Square | 1280 × 1280 | 1920 × 1920 |
| Portrait | 720 × 1280 | 1080 × 1920 |

Films are H.264 at 30 fps. Stills average four subpixel samples and films
average two. FFmpeg performs 1.5× Lanczos enlargement; it adds no geometric
detail. The [catalogue](../research/sixfold/assets/2026-11-18-library/catalogue.csv)
maps S001–S100 to compositions. The [manifest](../research/sixfold/assets/2026-11-18-library/source/manifest.json)
and [palettes](../research/sixfold/assets/2026-11-18-library/source/palettes.json)
record the settings. SHA-256 hashes for the source, assets and films are in
the [publication inventory](../verification/visuals-edition-01.json).

## What the rendering shows

The renderer samples depth-eight word centres, applies additional outer maps
and lights a finite-resolution surface around the field. Surface thickness,
colour, exposure and lighting are artistic choices. The mathematical
definition specifies the limiting set.

Camera studies include an orbit, a view along the two parallel passages,
an endless descent toward the fixed point of map 0, and a winding light
following smaller copies of an independent loop. The highlighted curve is
a polygonal visual guide associated with the winding proof.
[Rendering source](../research/sixfold/README.md)

![Winding light following the repeated loops](../site/assets/winding-light.png)

## TouchDesigner and reproduction

The public [Sixfold.toe](../research/sixfold/Sixfold.toe) was saved with
TouchDesigner **2025.33230** on Windows. Its locked lookup textures and shaders
are embedded. The public copy uses relative texture paths and omits the
development automation bridge and machine-specific component storage.
The original working project is preserved separately; the inventory records
its hash and these packaging changes.

Open the project from its research/sixfold folder and keep the supporting
files alongside it. The export panel also needs uv. The batch contact-sheet
generator uses the Windows Segoe UI font. Rendering was checked on Intel UHD
Graphics with OpenGL 4.3; [pinned dependencies](../render-requirements.txt)
record the tested Python environment. Other platforms and GPUs have not been
tested for pixel-identical output.

From the repository root:

    python scripts/check_visuals.py
    python scripts/download_films.py

After downloading the films, reproduce the GPU and full-decode checks with:

    uv run --isolated --python 3.12 --with-requirements render-requirements.txt python scripts/check_render.py

The download command retrieves approximately 592 MiB and verifies every MP4.
It restores the film paths used by the original offline gallery. Existing
files are checked before being reused.

Two native stills were reproduced pixel for pixel in a fresh temporary
directory, all six camera modes rendered, and all six films passed a full
decode check. The [render receipt](../verification/visuals-render-check.json)
records the environment and scope. These checks concern the visualisation;
the mathematical verification is documented separately.

The packaged TouchDesigner file was re-expanded successfully and opened in
a separate TouchDesigner 2025.33230 process. Its window capture was blank
and the inspection tool reported a memory-resource error, so interactive
studio rendering and export were not verified in this packaging pass.

## Change the featured film

Edit [site/media.json](../site/media.json). Set **video_url** to a public HTTPS
MP4 URL, or **youtube_id** to the selected YouTube video's ID. Use one field
at a time and update **caption**.

Rebuild or push to the main branch. The homepage uses the still when both
fields are empty. A direct film has playback controls and uses the still as
its poster. A YouTube film loads when the visitor selects Play film.

Record the source commit, render settings, output resolution and edits in
the media credit. Preserve this edition when producing later collections.
The visualisation release is a dated distribution snapshot; the Zenodo DOI
archive remains a separate step on the [release checklist](release.md).
