# Checkpoint report: support-strategy classification

**Dai Trang Vo - EAS 510 Project 2 - November 23, 2026**

This is a checkpoint record, not the completed final report.

## Question and data

Can recent conversation text predict the next support-strategy annotation better than always predicting the training majority?

The official [ESConv repository](https://github.com/thu-coai/Emotional-Support-Conversation) accompanies [Liu et al. (2021)](https://aclanthology.org/2021.acl-long.269/). The downloaded version contains **1,300 conversations, 38,365 messages, and eight strategy labels**. The source commit, URLs, and hashes are recorded in [acquisition.json](data/source/acquisition.json); permissions and sample modifications are in [DATA_USAGE.md](DATA_USAGE.md).

The [full dataset summary](results/full/dataset_summary.json) records schema, raw/eligible label counts, and missingness. There are no empty source messages, missing supporter labels, or exact duplicate full transcripts under the implemented check. Excluding 683 opening supporter messages without prior context leaves **17,693 examples**.

The bundled sample contains 80 real neutral opening greetings and their original next-response strategy labels. Response content, later messages, and metadata are removed. Selection uses only full-training conversations; [selection.json](data/sample/selection.json) records the procedure. Repeated greetings and missing classes make this sample unsuitable for model-quality conclusions.

## Method

One example predicts the label of a supporter message at index `i`. Input is `dialog[max(0, i - 6):i]`, with speaker prefixes. The exclusive upper bound excludes the target response. Future messages, annotations, situation descriptions, and surveys never become inputs. An earlier supporter response is valid observed history; its annotation is excluded.

Conversation IDs are sorted and shuffled with seed 510. Rounded 70% training / 15% validation / remaining test allocation gives **910/195/195 conversations** and **12,382/2,722/2,589 examples**. Every conversation stays in one partition. Exact duplicate full transcripts across partitions are rejected. Participant separation is not established.

The baseline predicts the most common training label, **Question**, with alphabetical tie-breaking. The alternative uses sklearn TF-IDF and multinomial Logistic Regression. TF-IDF lowercases text, extracts word unigrams/bigrams from tokens of at least two characters, and retains up to 20,000 training features without stop-word removal. For count `c > 0`, term frequency is `1 + ln(c)`; smoothed IDF is `ln((1 + N)/(1 + df)) + 1`. Their product is L2-normalized. Vocabulary and IDF are learned from training text only, then reused for validation.

Logistic Regression uses L2 regularization (`l1_ratio=0`, `C=1`), `lbfgs`, no class weighting, tolerance `1e-4`, and at most 1,000 iterations. The full run converged in 95 iterations. There was no hyperparameter search. [config.py](config.py) contains seeds and settings.

## Actual results

Both models use the same 2,722 validation examples. Higher is better.

| Model | Accuracy | Macro F1 | Weighted F1 |
|---|---:|---:|---:|
| Majority | 0.195812 | 0.040937 | 0.064128 |
| TF-IDF + Logistic Regression | 0.304555 | 0.190134 | 0.256855 |

Accuracy is overall label agreement. Macro F1 weights all eight classes equally; weighted F1 weights by class frequency. Undefined class scores are zero. [Saved metrics](results/full/metrics.json) include per-class scores and confusion matrices; [prediction rows](results/full/validation_predictions.csv) allow independent recomputation.

Logistic Regression improves accuracy by 10.87 percentage points, but recall remains below 3% for Reflection of feelings, Information, Self-disclosure, and Restatement or Paraphrasing. This is evidence of improved annotation prediction under this split, not improved empathy or clinical effectiveness. Multiple strategies may be reasonable for one context. No test predictions or test metrics have been computed.

On the greeting sample, both models obtain validation accuracy 0.750000 and macro F1 0.107143 on 12 examples. Those results check pipeline execution only.

## Checks, challenges, and completion plan

Six automated checks pass, including target/future exclusion and conversation separation. A fresh Windows/Python 3.14.7 clone reproduced the sample with network connections disabled and only pinned runtime dependencies installed; [verification.json](results/verification.json) preserves the tested commit and measurements. Accuracy and macro F1 were independently recomputed from saved prediction rows. Linux verification remains pending.

An initial floating-point allocation issue produced 909 training conversations. Rounded allocation corrected this to 910, and both experiments and the sample were rebuilt. Current evidence uses the corrected split. Other limitations include class imbalance, no uncertainty intervals, and no manual context-level error analysis yet.

Before December 7: inspect validation errors; compare Linear SVM or a modest class-weight/context refinement; freeze choices before adding final test scoring. Implement strategy-conditioned generation and a simple interface if feasible, then compare with a generic support prompt on the same 30 fictional scenarios using a predefined rubric. CBT sources must be reviewed before use. Finish Linux verification and the required final report. Generation, CBT retrieval, the interface, and response-quality evaluation are currently unfinished; substantial scope changes require instructor approval.

## Contributions and AI Assistance

The student supplied the proposal, requirements, project direction, and netid. OpenAI Codex created the milestone code, inspected the official dataset/terms, ran experiments and checks, and drafted the documentation/update. sklearn provides [TF-IDF](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html), [Logistic Regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html), and metrics; no ESConv model code was copied. The student still needs to review, reproduce, understand, and approve the work before submission.
