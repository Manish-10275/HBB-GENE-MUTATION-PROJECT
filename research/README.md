# HBB Mutation Analyzer — Scientific Research & Benchmark Layer

## Overview
This directory contains the independent scientific evaluation framework, benchmark manifests, statistical evaluation harness, and experimental reproducibility protocols for the **HBB Gene Mutation Analyzer**.

The primary scientific inquiry evaluated by this framework is:
> *"How accurately and consistently does the HBB Mutation Analyzer interpret known HBB variants across HGVS parsing, reference coordinate resolution, molecular consequence prediction, and evidence retrieval?"*

---

## Directory Architecture

```
research/
├── README.md                      # This document
├── manifest/
│   ├── hbb_benchmark_manifest.json# Master verified dataset (N = 65)
│   ├── development.json           # Development split (N = 12)
│   ├── validation.json            # Validation split (N = 17)
│   ├── frozen_test.json           # Frozen held-out test split (N = 36)
│   └── frozen_test.sha256         # Cryptographic SHA-256 seal for frozen_test.json
├── evaluation/
│   ├── run_benchmark.py           # Main evaluation harness
│   ├── metrics.py                 # Diagnostic & information retrieval metrics
│   ├── consequence_agreement.py   # Consequence comparator & normalizer
│   └── report.py                  # Markdown & JSON publication report generator
├── results/
│   ├── benchmark_results.json     # Machine-readable per-variant evaluation logs
│   ├── metrics.json               # Computed summary metrics
│   ├── BENCHMARK_REPORT.md        # Comprehensive human-readable benchmark report
│   └── tables/                    # Formatted publication tables
├── provenance/
│   └── SOURCES.md                 # Primary ground truth provenance documentation
└── paper/
    └── RESULTS_TEMPLATE.md        # Pre-formatted manuscript results section
```

---

## Benchmark Split Strategy

To prevent data leakage and circular validation:
- **Development Set ($D_{dev}$, $N = 12$):** Used for code development, parser debugging, and regression testing.
- **Validation Set ($D_{val}$, $N = 17$):** Used for threshold calibration and ranking algorithm tuning.
- **Frozen Test Set ($D_{test}$, $N = 36$):** **Cryptographically sealed with SHA-256**. Contains 23 clinical variants spanning all classes and 13 structured negative controls. The evaluation harness validates this signature prior to execution; any modification aborts with `FrozenDatasetIntegrityError`.

---

## Reproducible Benchmark Execution

To execute the benchmark against the frozen test set:
```bash
python research/evaluation/run_benchmark.py --split test --mode offline
```

To evaluate the entire master dataset:
```bash
python research/evaluation/run_benchmark.py --split all --mode offline
```

To evaluate in online mode (with live NCBI ClinVar E-utilities retrieval):
```bash
python research/evaluation/run_benchmark.py --split test --mode online
```
