# Therapy-support chatbot: first checkpoint

**Dai Trang Vo (daitrang), EAS 510 Project 2 - November 23, 2026**

This checkpoint implements support-strategy classification using ESConv. It includes data inspection, conversation-level splits, a majority baseline, and TF-IDF + Logistic Regression. Response generation, CBT retrieval, and the chat interface are not implemented.

Checkpoint deliverable: [one-page interim update](interim_update.pdf), with [editable text](interim_update.md). Methods, limitations, and AI disclosure are in [report.md](report.md).

## Run

Tested on Windows 11 with **Python 3.14.7**, CPU only. Pinned dependencies require Python 3.12 or later; Python 3.14 matches the tested environment.

PowerShell, from this folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

If activation is blocked, use `.\.venv\Scripts\python.exe` instead of `python` for installation and execution.

Linux/macOS setup uses `python3 -m venv .venv` and `source .venv/bin/activate`, followed by the same installation/run commands. Linux has not yet been verified.

The default run fits and evaluates both models on the bundled 80-excerpt greeting sample. After installation, it needs no network, API, credentials, or GPU. The sample is deliberately narrow and repetitive; its scores demonstrate execution only.

For the full experiment, first read [DATA_USAGE.md](DATA_USAGE.md), then run:

```bash
python data/download.py
python main.py --full
```

Acquisition downloads about 9 MB from the official repository at a pinned commit and verifies checksums. Full and derived conversation text stays local and is excluded from Git. `python data/make_sample.py` recreates the bundled greeting excerpts from full-training conversations.

## Measured results

These are **validation** results; higher is better. The test set remains reserved.

| Data | Model | Validation examples | Accuracy | Macro F1 |
|---|---|---:|---:|---:|
| Greeting sample | Majority | 12 | 0.750000 | 0.107143 |
| Greeting sample | TF-IDF + Logistic Regression | 12 | 0.750000 | 0.107143 |
| Full ESConv | Majority | 2,722 | 0.195812 | 0.040937 |
| Full ESConv | TF-IDF + Logistic Regression | 2,722 | 0.304555 | 0.190134 |

Each mode writes to `results/sample/` or `results/full/`:

- `dataset_summary.json`: schema, counts, labels, cleaning, and split counts.
- `metrics.json`: accuracy, macro/weighted F1, per-class scores, and confusion matrices.
- `validation_predictions.csv`: IDs, true labels, and predictions, without message text.
- `config.json`, `run.json`, `splits.json`: settings, environment, and exact conversation partitions.

Past-only examples are also saved locally under ignored `data/processed/`. Settings are in `config.py`. Reruns replace the corresponding results. On the pinned environment, expect displayed metrics to agree within `1e-5`; platforms/solvers can affect predictions, so investigate larger differences. Timing and environment metadata vary.

A fresh Windows clone reproduced the offline sample in **7.34 seconds**, using **114.10 MiB** peak process memory; [verification evidence](results/verification.json) records that run. The full pipeline took about 6 seconds after imports. Neither measurement establishes Linux performance.

## Check correctness

```bash
python -m unittest discover -s tests -v
```

Six checks cover target/future exclusion, context truncation, conversation separation, duplicate-transcript rejection, training-only vocabulary, and majority behavior.

## Submission status

The checkpoint PDF and local repository are prepared for student review. A GitHub repository URL still needs to be created/provided by the student. Nothing has been uploaded or submitted. The final report and remaining chatbot features are due in the later milestone.
