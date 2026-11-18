# Sources for a future paper

The repository is the working record from which the paper can be developed.
The paper should identify one archived version and refer to its definitions,
proofs, certificates and reproduction commands. External mathematical results
retain citations to their original publications.

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

The first settled release should archive the note and evidence together.
Record its Git commit and Zenodo version DOI in the paper.
The [release checklist](release.md) tracks that step.
