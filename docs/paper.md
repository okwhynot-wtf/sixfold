# Paper draft and source map

The second working manuscript is **Sixfold: a contact-defined family of spatial
self-similar sets**, by **okwhynot-wtf**, dated 19 November 2026.

**[Read draft 0.2 (PDF)](../output/pdf/sixfold-draft.pdf)** ·
**[Editable source and build instructions](../paper/README.md)** ·
**[Claims and review priorities](../paper/claims.md)**

The draft gives the exact family definition, the computer-assisted dimension
and linking arguments, a bounded originality assessment, and explicit open
problems. The second draft adds an early results table, develops the proof
steps more explicitly, and moves the longer algebraic calculation and bore
study to appendices. See the [revision history](../paper/revisions.md).

All six verification groups passed on 18 November, as recorded in the
[draft receipt](../paper/verification.json); the scientific inputs are unchanged.
The analytic deductions still await
independent mathematical review. The [literature check notes](../paper/literature-check.md)
record the additional common-fixed-point precedent found while drafting.

The repository is the working record from which the paper can be developed.
The paper should identify one archived version and refer to its definitions,
proofs, certificates and reproduction commands. External mathematical results
retain citations to their original publications.

The first source snapshot is archived as version **zenodo**, DOI
[10.5281/zenodo.24336419](https://doi.org/10.5281/zenodo.24336419), at Git commit
**1c660bedf8cd3e52bad8e5d033535dcde6e06b6e**. It includes the research evidence
and stills; the six MP4 films are separate GitHub downloads. See
[archive scope and citation](release.md).

**The new manuscript is not contained in that earlier deposit.** Its DOI cites
the underlying evidence archive. Archive the reviewed manuscript and the exact
evidence version it uses together in a subsequent release.

| Proposed part | Repository source |
| --- | --- |
| Six maps and root-selection rule | [Definition](definition.md), [contact certificate](../research/fractal_handover/fractal_research_07/positive_contact_certificate.json) |
| Connectedness and intersections | [Phase 04](../research/fractal_handover/fractal_research_04/RESEARCH_04.md), [phase 06](../research/fractal_handover/fractal_research_06/RESEARCH_06.md) |
| Uniform dimension bounds | [Phase 05](../research/fractal_handover/fractal_research_05/RESEARCH_05.md) |
| Weak separation and Assouad dimension | [Phase 07](../research/fractal_handover/fractal_research_07/RESEARCH_07.md) |
| Two exact Hausdorff dimensions | [Phase 08](../research/fractal_research_08/RESEARCH_08.md) and its verification programs |
| Independent loops and persistence | [Phase 09](../research/fractal_research_09/RESEARCH_09.md), [phase 10](../research/fractal_research_10_topology/RESEARCH_10.md) |
| Relatives and novelty assessment | [Prior-art report](../research/fractal_research_11_prior_art/PRIOR_ART.md) |
| Figures and rendering | [Media](media.md), [source](../research/sixfold/README.md) |
| Reproducibility and AI contribution | [Reproduction](reproduce.md), [provenance](provenance.md), verification receipt |

## Review before submission

Review should cover exact parameter isolation, the compact-group and
separation arguments, applications of Hochman's and García's theorems, and
the topological conclusions from the linking construction.

Finite checks are reproducible with the [runner](../scripts/verify.py).
The surrounding analytic arguments require mathematical assessment. Track
corrections in the repository and describe material changes in the changelog.

Archive the completed technical note with the evidence it uses. If the paper
uses changes after the first source snapshot, cite a subsequent archived
version containing those changes. Record its Git commit and version DOI.
The [release checklist](release.md) tracks that step.
