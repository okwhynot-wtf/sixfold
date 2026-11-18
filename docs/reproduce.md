# Reproduce the work

Use Python 3.12. Scientific dependencies are pinned in
[requirements.txt](../requirements.txt).

## Run all current implementation checks

With [uv](https://docs.astral.sh/uv/) installed, run

    git clone https://github.com/okwhynot-wtf/sixfold.git
    cd sixfold
    uv run --isolated --python 3.12 --with-requirements requirements.txt python scripts/verify.py --receipt .build/verification.json

The runner copies the scientific files to a temporary directory and performs
these stages in order.

1. Handover manifest, contact symmetries, integer packings, overlap obstruction and rotation premises.
2. Reference exact elimination, polynomial factor and word-freeness premises.
3. Second member's algebraic and modular checks.
4. Central passage.
5. Two independent passages.
6. Tilted bore witnesses and shrinking-loop premises.

Each completed stage reports PASS. A failure stops the runner and records
the completed stages and failed output when a receipt path was supplied.
Assertions must remain enabled. Independent review of the analytic arguments
and theorem applications is pending.

A conventional Python 3.12 virtual environment also works. Activate it using
your operating system's procedure, then run

    python -m pip install -r requirements.txt
    python scripts/verify.py --receipt .build/verification.json

The initial publication receipt is in
[verification/initial.json](../verification/initial.json). It records the
environment, source digest, stage outputs and scope. GitHub Actions reruns
the checks on Linux when scientific inputs or the runner change.

## Generate the reference shape

    uv run --isolated --python 3.12 --with-requirements requirements.txt python scripts/generate.py --depth 5 --output .build/sixfold.csv

The file contains $6^5=7,776$ word centres in x, y, z order. Depths zero to eight
are supported. The script uses floating-point reference maps and prints the
geometric tail scale. This approximation is suitable for visual exploration.
The [definition](definition.md) supports independent implementation. Interval
scripts supply the additional error accounting for mathematical arguments.

## Build the website

    uv run --isolated --python 3.12 --with-requirements site-requirements.txt python scripts/build_site.py
    python -m http.server 8765 --directory _site

Visit http://localhost:8765. The website renders the canonical Markdown
files in **docs**. Evidence links point into GitHub. Mathematical notation
uses MathJax in the browser.

## Render images and films

[research/sixfold](../research/sixfold/README.md) includes the renderer, shaders,
colour settings, textures and TouchDesigner project. Its OpenGL renderer
needs a compatible GPU and additional dependencies. Follow its instructions
from **research**, so the original sibling paths resolve.

Film exports are being organised in the working visualisation folder.
[Media instructions](media.md) explain how to attach the selected public film.
