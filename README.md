# Therapy-support chatbot: first checkpoint

**Dai Trang Vo (daitrang), EAS 510 Project 2 - November 23, 2026**

My project explores whether predicting a support strategy before generating a reply can help organize an emotional-support conversation. For this first checkpoint, I focused on preparing ESConv and comparing a majority-class baseline with Logistic Regression. The response generator, CBT materials, and chat interface are still planned work.

The [one-page interim update](interim_update.pdf) describes my current progress and next steps. Its [editable version](interim_update.md) is also included. The [checkpoint report](report.md) explains the methods, results, limitations, and AI assistance.

## Run

The project has been tested on Windows 11 with **Python 3.14.7**, using only the CPU. The packages in `requirements.txt` need Python 3.12 or later. Python 3.14 matches the environment used for the saved results.

PowerShell, from this folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

If activation is blocked, use `.\.venv\Scripts\python.exe` instead of `python` for installation and execution.

Linux/macOS setup uses `python3 -m venv .venv` and `source .venv/bin/activate`, followed by the same installation/run commands. Linux has not yet been verified.

The default run trains and evaluates both models on 80 short greeting excerpts included in the repository. It works offline after installation and does not need an API or GPU. These simple, repeated greetings make the sample useful for checking that the code runs, but not for judging how well the classifier handles emotional-support conversations.

For the full experiment, first read [DATA_USAGE.md](DATA_USAGE.md), then run:

```bash
python data/download.py
python main.py --full
```

The download script obtains about 9 MB from a fixed version of the official repository and checks the file hashes. Full conversations and processed message text stay in local folders excluded from Git. To recreate the greeting sample from the full training partition, run `python data/make_sample.py`.

## Measured results

Both models were evaluated on the same **validation** examples. Higher scores are better. The test set has not been evaluated.

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

The input examples are saved locally under `data/processed/`, which Git ignores. Model settings and seeds are in `config.py`. Running an experiment again replaces its saved results. With the same package versions, scores should agree within `1e-5`. Different platforms or numerical solvers can affect predictions, while runtime naturally varies.

A fresh copy of the repository reproduced the offline sample on Windows in **7.34 seconds**, with peak memory use of **114.10 MiB**. The details are saved in [verification.json](results/verification.json). The full experiment took about 6 seconds after importing the libraries. Linux testing is still needed.

## Check correctness

```bash
python -m unittest discover -s tests -v
```

The six tests check that target and future messages stay out of the input, the context window is applied correctly, conversations stay in separate splits, duplicate full transcripts cannot cross splits, the vocabulary is fitted only on training text, and the majority predictor behaves as expected.

## Submission status

This repository contains the work completed for the first checkpoint. It is still local, so the GitHub link has not been added yet. I plan to finish the remaining experiments, chatbot features, and final report before December 7.
