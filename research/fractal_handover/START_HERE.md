# Fractal research handover

Prepared 17 November 2026, Australia/Sydney.

This folder contains the seven research phases, their source code, saved
certificates and verification data, and all available PNG/PLY results.

**For Codex:** read AGENTS.md, HANDOVER.md, and the latest report
fractal_research_07/RESEARCH_07.md. CODEX_PROMPT.md is a ready-to-paste starting
instruction. Earlier reports are historical records; some open questions in them
were resolved in later phases.

The current object is a connected spatial six-map similarity attractor. The
latest claims, subject to independent mathematical review, are:

| Property | Current result |
|---|---|
| Exact self-similarity and connectedness | Established by the construction and interval contact certificate |
| Reference Hausdorff dimension | Strictly between 2.1984 and 2.4149 |
| Whole connected curve's Hausdorff dimension | Strictly between 2.1970 and 2.4150 |
| Assouad dimension | Exactly 3 throughout the connected curve, by the stated deduction using published theorems |
| OSC and WSP | Fail; phase 07 also excludes any alternative finite similarity presentation with either property |
| Exact Hausdorff dimension | Open |
| Historical originality | Open |

These are computer-assisted mathematical arguments, not proof-assistant
formalizations or independently peer-reviewed results. A passing script is
evidence for its implementation checks, not automatic verification of every
analytic deduction or cited theorem application.

## Setup on Windows

Use Python 3.12. From this extracted folder in PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe verify_handover.py
```

Using the environment's Python directly avoids PowerShell activation-policy
issues. If Python is already available as `python`, use that executable to
create the environment instead.

## Setup on macOS or Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python verify_handover.py
```

The default verification checks SHA-256 file integrity, then rechecks the current
contact, dimension-packing, OSC-obstruction and Assouad-premise calculations in
a temporary copy. **It needs no C++ compiler.** It leaves the supplied evidence
files unchanged. Do not run Python with `-O`, because the scientific code uses
assertions. Installation needs package access; the checks themselves run offline.

For an integrity check using only Python's standard library:

```bash
python verify_handover.py --manifest-only
```

For the older negative-certificate checks as well:

```bash
python verify_handover.py --historical
```

The validation receipt included here records the actual environment and checks
used when packaging. The portable entry point was tested on Linux; Windows
execution has not been observed in this session.

## Images to open first

- fractal_research_05/dimension_portrait.png: the six largest copies in colour.
- fractal_research_07/shared_point_zoom.png: selected copies crowding around the
  same fixed point at two rescaled depths.
- fractal_research_04/connected_contacts.png: the original six certified contacts.
- fractal_research_01/first_gallery.png: the early planar exploration.

These are finite geometry previews. Their pixels do not prove connectedness,
separation, exact dimension or novelty. The PLY exports in phase 02 are point
clouds, not watertight printable meshes.

Optional image regeneration, with portable font fallback:

```bash
python render_current.py
```

Regenerating images changes files covered by MANIFEST.json. Use a working copy
if preserving the original bundle's integrity is important.

## Recommended next action

Audit the phase-06/07 reasoning and its theorem hypotheses first. Then continue
the reference member's exact-Hausdorff-dimension problem by investigating
**finite exact word-map relations**. Sharing a fixed point does not mean that
two transformations are equal. The precise next task is in HANDOVER.md.
