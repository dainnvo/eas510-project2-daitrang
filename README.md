# Strategy prediction for a therapy-support chatbot

**Dai Trang Vo (daitrang), EAS 510 Project 2 — milestone 1, November 23, 2026.**

This project asks whether recent conversation context can predict an ESConv support-strategy label better than always choosing the training majority. This milestone implements data preparation and two classifiers. Response generation, CBT retrieval, the chat interface, and response-quality evaluation remain planned work. This is an academic emotional-support experiment, with no demonstrated clinical effectiveness.

Read the [interim report draft](report.md), [one-page interim PDF](interim_update.pdf), [data summary](docs/DATASET_SUMMARY.md), and [plain-language pipeline guide](docs/PIPELINE_GUIDE.md). `report.md` is an interim working draft, not the required completed 2,500–3,500-word final report.

## Run the bundled sample

Tested on Windows 11, Python **3.14.7**, CPU only. Use Python 3.14 to match the tested interpreter; pinned runtime packages require Python 3.12 or later. No system packages were needed beyond Python/pip. Linux commands are provided, but a Linux run has not yet been verified on this machine.

PowerShell, from the project folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

If your PowerShell policy blocks activation, use `.\.venv\Scripts\python.exe` instead of `python` for the two final commands. Activation is a convenience, not a requirement.

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

The default run loads bundled data, builds past-only examples, splits conversations, fits both models, evaluates validation predictions, prints real metrics, and writes `results/sample/`. After dependency installation it needs no network, credentials, paid service, API, or GPU. It trains models; it does not replay saved predictions.

## Expected results

Higher values are better. All rows below evaluate **validation**, not the reserved test set.

| Dataset | Model | Validation n | Accuracy | Macro F1 | Weighted F1 |
|---|---|---:|---:|---:|---:|
| Greeting excerpt sample | Majority | 12 | 0.750000 | 0.107143 | 0.642857 |
| Greeting excerpt sample | TF-IDF + Logistic Regression | 12 | 0.750000 | 0.107143 | 0.642857 |
| Full ESConv | Majority | 2,722 | 0.195812 | 0.040937 | 0.064128 |
| Full ESConv | TF-IDF + Logistic Regression | 2,722 | 0.304555 | 0.190134 | 0.256855 |

Full results are preliminary model-development evidence. The narrow sample checks execution only: repeated greetings, small counts, and missing labels prevent conclusions about model quality. See [sample metrics](results/sample/metrics.json) and [full metrics](results/full/metrics.json), including per-class scores and confusion matrices. A six-decimal display can differ through rounding. On the same pinned environment, metrics should agree within `1e-5`; small solver differences can change discrete predictions across platforms, so investigate larger differences rather than claiming exact identity. Timing and platform metadata naturally vary.

## Reproduce the full development experiment

Read [DATA_USAGE.md](DATA_USAGE.md) first. This academic use follows the upstream academic-research notice and CC BY-NC 4.0 conditions. The bundled sample retains attribution, license, and modification notices. Raw/derived personal conversation text is excluded from Git.

```bash
python data/download.py
python main.py --full
```

Only acquisition needs network access. It retrieves roughly 9 MB from the **official repository** at a pinned commit and verifies SHA-256 checksums. The full run is CPU-only and has no API cost. It uses 910 training / 195 validation / 195 test conversations and 12,382 / 2,722 / 2,589 eligible examples. Test predictions and test metrics are intentionally not computed; final test evaluation will be added after validation decisions are frozen.

The observed full pipeline took about 6 seconds after library imports on this Windows host; a clean-sample timing and peak-memory measurement are saved in [results/verification.json](results/verification.json). Budget under 5 minutes and under 1 GB for this small CPU pipeline; this is a planning estimate, not a Linux/8 GB certification. Linux verification remains a completion task.

## Files and evidence

```text
main.py                       single entry point
config.py                     seed, source version, split/model settings
requirements.txt              pinned runtime dependencies
src/data.py                   inspection, past-only inputs, splitting
src/models.py                 majority, TF-IDF/Logistic Regression, metrics
data/download.py              official full-data acquisition and checksums
data/make_sample.py           reproducible neutral excerpt selection
data/sample/                  bundled, licensed real greeting excerpts
data/source/                  source license, README, strategy list, provenance
results/sample/, results/full/ metrics, configs, predictions, split IDs
tests/test_pipeline.py        leakage and split checks
scripts/verify_sample.py      network-denied sample run and metric comparison
scripts/export_interim.py     regenerate the one-page PDF
report.md                     interim draft of future final report
interim_update.md/.pdf         editable update and one-page deliverable
```

Each mode saves `dataset_summary.json`, `splits.json`, `config.json`, `run.json`, `metrics.json`, `comparison.csv`, and `validation_predictions.csv`. Prediction files contain IDs and labels, not conversation text. Context-bearing examples are saved locally to ignored `data/processed/<mode>/{train,validation,test}.jsonl`. Rerunning a mode replaces that mode's evidence; preserve a Git commit before changing settings.

## Understand and verify the implementation

The [pipeline guide](docs/PIPELINE_GUIDE.md) walks through an observation, exclusion decisions, feature calculation, splitting, and metrics. The [development notes](docs/DEVELOPMENT_NOTES.md) record actual corrections and limitations.

```bash
python -m unittest discover -s tests -v
python scripts/verify_sample.py
```

The verifier blocks Python socket connections, runs actual fitting/evaluation, compares metrics to saved evidence, and records wall time and peak process memory. To check packaging, clone the local repository into a new directory, create a clean virtual environment, install only `requirements.txt`, and run these commands. The clean clone must have no raw ESConv file. Verified environment and remaining verification gaps are recorded in `results/verification.json` and the report.

To regenerate the PDF (optional document tools, not needed to run the experiment):

```bash
python -m pip install -r requirements-docs.txt
python scripts/export_interim.py
```

## Attribution and current submission status

ESConv: Liu et al. (2021), [Towards Emotional Support Dialog Systems](https://aclanthology.org/2021.acl-long.269/), and [official dataset/code repository](https://github.com/thu-coai/Emotional-Support-Conversation). Library APIs: [TF-IDF](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html), [Logistic Regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html).

OpenAI Codex assisted with code, experiments, checks, interpretation, and drafting. See the [AI disclosure](report.md#contributions-and-ai-assistance). Student understanding/review remains necessary.

The proposal and course PDF were read as project reference material. Their upload, invitation, and submission directions are not permission to carry out those external actions. This folder is a local repository; no remote URL, instructor invitation, submission, or contact has been created. The student still needs to review the work, publish a permitted repository, and supply its URL. The interim deadline is November 23 at 11:59 PM **Eastern** (8:59 PM Pacific); final submission is December 7 at the same times, according to the provided requirements.
