# Therapy-support chatbot

**Dai Trang Vo (daitrang), EAS 510 Project 2 - November 23, 2026**

[GitHub repository](https://github.com/dainnvo/eas510-project2-daitrang)

My project explores whether predicting a support strategy before generating a reply can help organize an emotional-support conversation. The current implementation prepares ESConv and compares a majority-class baseline with Logistic Regression. The response generator, CBT materials, and chat interface are still planned work.

This repository contains the project code, a small runnable sample, data documentation, and results from completed experiments.

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

## How the classifier works

Each example predicts the strategy label of a supporter response using up to six earlier messages, marked with speaker roles. The target response, future messages, strategy annotations, situation descriptions, and surveys are excluded from the input. Of 18,376 supporter messages, 683 have no earlier context, leaving 17,693 examples.

Conversations are shuffled with seed 510 and divided into training, validation, and test sets. Every example from a conversation stays in the same split. The sets contain 910/195/195 conversations and 12,382/2,722/2,589 examples, respectively. The code checks for overlapping conversation IDs and exact duplicate full conversations across splits.

The baseline always predicts the most common training label, `Question`. Logistic Regression uses a sparse TF-IDF representation of lowercased words and adjacent word pairs, keeping up to 20,000 features. For a feature count `c > 0`, term frequency is `1 + ln(c)`; smoothed IDF is `ln((1 + N)/(1 + df)) + 1`, where `N` is the number of training examples and `df` is the number containing the feature. Their product is L2-normalized. Vocabulary and IDF are fitted only on training text. The classifier uses L2 regularization, `C=1`, and `lbfgs`, without class weighting. All settings are in [config.py](config.py).

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

## Current limitations and next steps

Logistic Regression improves overall validation scores, but recall is below 3% for four strategies. More than one strategy can be reasonable in a conversation, so matching the dataset label does not fully measure helpfulness. These results do not establish response quality or clinical effectiveness.

My next steps are to review validation errors, compare Linear SVM or a small change to class weights or context length, and settle the model choices before evaluating the test set. After that, I plan to connect the classifier to a response generator, build a simple interface, and compare strategy-guided and generic-prompt responses on the same 30 fictional scenarios. Linux testing and review of reliable CBT sources are also still needed.

## Sources and AI assistance

ESConv comes from [Liu et al. (2021), Towards Emotional Support Dialog Systems](https://aclanthology.org/2021.acl-long.269/) and the [official CoAI repository](https://github.com/thu-coai/Emotional-Support-Conversation). Dataset permissions and sample modifications are documented in [DATA_USAGE.md](DATA_USAGE.md). sklearn provides [TF-IDF](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html), [Logistic Regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html), and metrics; no ESConv model code was copied.

I developed the proposal and chose the project direction. I used OpenAI Codex to help implement the code, inspect ESConv and its terms, run experiments and tests, and draft and edit the documentation. Checks completed with Codex included file-hash verification, dataset inspection, leakage tests, a fresh-environment sample run, and recalculation of metrics from saved predictions. These checks do not replace my own review and understanding of the work.
