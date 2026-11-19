# Sixfold paper: working draft 0.2

**Sixfold: a contact-defined family of spatial self-similar sets**

Author: **okwhynot-wtf**. Second draft dated 19 November 2026. Independent mathematical review is pending.

- [Read the PDF](../output/pdf/sixfold-draft.pdf).
- [Main LaTeX source](sixfold-draft.tex), with [topology](topology.tex), [discussion](discussion.tex), and [references](references.tex).
- Appendices: [reference algebraic proof](reference-proof.tex), [inherited bore](bore.tex), and [evidence map](evidence.tex).
- [Revision history](revisions.md): substantive changes from the first draft, which remains available in Git history.
- [Claim and review register](claims.md): scope, finite evidence, analytic step and outstanding review for each result.
- [Verification receipt](verification.json): all six groups passed on 18 November 2026. The scientific source files are unchanged in draft 0.2; the receipt does not independently validate the mathematical deductions.
- [Draft checks](draft-check.json): PDF, references, source links and visual inspection record.
- [Literature check notes](literature-check.md): sources checked for this draft, including an additional common-fixed-point precedent.

The draft leads with the exact construction and its documented properties. It makes no claim of a new topological type or established historical priority. It distinguishes a periodic point shared by two words from equality of the corresponding word maps.

## Build

Install a TeX distribution containing pdfLaTeX and the standard packages used in the preamble (TinyTeX or TeX Live, for example). Then run from the repository root:

```powershell
python paper/build.py
```

The build runs three LaTeX passes, checks for unresolved references and overfull boxes, and writes `output/pdf/sixfold-draft.pdf`. Intermediate files stay under the ignored `.build/paper/` directory. The three figure inputs are existing repository images, linked directly in the source. The PDF build does not run the scientific verifier; reproduce that separately using the command in the repository README.

## Evidence version and DOI

The source evidence is archived at [10.5281/zenodo.24336419](https://doi.org/10.5281/zenodo.24336419), Git commit `1c660bedf8cd3e52bad8e5d033535dcde6e06b6e`. The mathematical reports and code in phases 04–10 were unchanged when drafting began from publication commit `dc46aa50ac015db9134f14ddf5691f4178db33da`. The run receipt also records a hash of the current research tree; that includes visual assets and is not an archive ZIP checksum.

**This manuscript is newer than that deposit and is not included in it.** The DOI cites the evidence archive, not a published paper. Preserve that distinction until a reviewed manuscript and its exact supporting version are archived together.

## Next editorial steps

1. Read the abstract, early results table, originality section and open problems for the intended emphasis.
2. Arrange independent review of the five mathematical proof interfaces listed in [claims.md](claims.md), then record corrections alongside their evidence.
3. Decide whether a chosen venue wants the detailed reference elimination and bore investigation, now in appendices, as a separate supplement. The main text presents the shorter rational-tilt dimension proof.
4. Improve figure typography for the chosen venue if needed; the present three figures are clearly labelled finite visualisations from the repository.
5. Select a venue, apply its formatting and AI-disclosure requirements, and replace the working-draft status only after review.
6. Archive the finished manuscript with the exact repository version it uses; update the version DOI and citation metadata at that point.

The open research problems need not all be solved before publishing a sound construction paper. They do need to remain clearly separated from established claims. Text and figures use the repository's CC BY 4.0 terms; build code uses MIT.
