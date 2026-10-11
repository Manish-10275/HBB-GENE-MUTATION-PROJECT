# Table 3: ClinVar Evidence Retrieval Performance

| Retrieval Metric | Result | Target Standard | Provenance / Clinical Utility |
| :--- | :---: | :---: | :--- |
| **ClinVar Hit@1 (Rank-1 Exact Match)** | `100.0%` | >= 85.0% | Exact Variation ID prioritized at Rank 0 |
| **ClinVar Recall@5 (Candidate Inclusion)** | `100.0%` | >= 90.0% | True Variation ID in top candidate window |
| **False Match Rate** | `0.0%` | <= 5.0% | False positive exact-match prevention |
| **Mean Retrieved Records** | `1.0` | 1 - 5 | Progressive search bounding |
