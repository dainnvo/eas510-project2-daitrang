# Strategy prediction for structured emotional support

**Dai Trang Vo — EAS 510 Project 2 — interim working report, November 23, 2026**

This is a record of completed milestone-one work. It is not the completed final report and does not yet satisfy the final 2,500–3,500-word requirement. Results below are validation results. The reserved test set has not been evaluated.

## Question and scope

Can a simple text classifier use recent conversation history to predict the strategy label of the next ESConv supporter message better than a training-majority baseline? This is the classification component of the approved therapy-support chatbot proposal. Predicting recorded strategy choices is a narrower task than choosing an optimal strategy or delivering effective support. Response generation, a chat interface, CBT materials, and the proposed comparison on 30 fictional scenarios have not been implemented.

## Background and data

Liu et al. (2021) introduced ESConv and a framework for emotional-support conversations [1]. The official CoAI repository [2] supplies the current dataset and eight support-strategy categories. This milestone implements a new small classification pipeline using standard sklearn library APIs; it does not adapt their neural generation models.

The downloaded `ESConv.json` is pinned to commit `f262d062ad74cb39b17ea476facc81568ddcba24`, with integrity hashes saved in [acquisition.json](data/source/acquisition.json). The separate `FailedESConv.json` collection is excluded. The source contains **1,300 conversations and 38,365 messages**, including 19,989 seeker and 18,376 supporter messages. Each conversation contains ordered dialog plus situation, emotion, topic, survey, and related fields. Each message has a role, content, and annotation. Supporter `strategy` is the prediction target; other annotations are not features.

The source has no empty messages or missing supporter strategy labels and no exact duplicate full transcripts under the implemented check. The eight labels retain their actual spelling: Question; Restatement or Paraphrasing; Reflection of feelings; Self-disclosure; Affirmation and Reassurance; Providing Suggestions; Information; Others. The [measured summary](docs/DATASET_SUMMARY.md) records schema, raw/eligible class counts, topic values, and split counts. Raw category spellings are not silently normalized.

The official license is CC BY-NC 4.0, and its README specifies academic research use. Attribution, license text, and modifications are documented in [DATA_USAGE.md](DATA_USAGE.md). Full raw conversations and derived context files are local and ignored by Git. The included 80-excerpt sample contains only reviewed neutral greetings and actual next-message labels; response content and other text/metadata are removed. Its selection is deterministic and restricted to full-training conversations. This preserves a small real-data demonstration without bundling emotional disclosures. It is deliberately unrepresentative; repeated greeting contexts and absent classes make its scores unsuitable as model-quality evidence.

## Methodology

One observation is a labeled supporter response that has preceding context. Input text concatenates at most the six immediately preceding messages with role prefixes. The slice ends before the target message. Target content, future content, strategy annotations (including historical ones), feedback, situation, and surveys never enter features. The 683 initial supporter messages without preceding context are excluded, leaving **17,693 examples**. No remaining label is dropped or merged. This exclusion particularly changes the frequency of opening questions, so the majority is estimated after example construction.

Conversation IDs are sorted, shuffled using seed 510, and assigned to rounded 70% training / 15% validation / remaining test partitions. This produces **910/195/195 conversations** and **12,382/2,722/2,589 examples**. All targets from a conversation stay together. The audit verifies disjoint IDs and checks exact duplicate full transcripts. Participant separation cannot be guaranteed because no participant IDs are used. Near-duplicate language and common greetings are not removed. These are custom splits, so numbers should not be compared directly with papers using another dataset release or official split protocol.

The majority baseline counts training labels and predicts `Question` for every validation example. Ties would be resolved alphabetically. The alternative is a sklearn pipeline of TF-IDF and Logistic Regression [3,4]. TF-IDF lowercases text, tokenizes words of at least two characters, extracts unigrams/bigrams, retains up to 20,000 features, uses logarithmic term frequency and smoothed IDF, and L2-normalizes vectors. The [pipeline guide](docs/PIPELINE_GUIDE.md) provides the exact equations. Vocabulary and IDF are fit on training text only, creating a sparse 12,382-by-20,000 matrix. Validation calls only `predict`.

Logistic Regression uses multinomial classification with L2 regularization (`l1_ratio=0`, `C=1`), `lbfgs`, no class weighting, tolerance `1e-4`, and a maximum of 1,000 iterations. The full run converged in 95 iterations. No hyperparameter search was conducted. All explicit settings and source/split choices are saved in [config.json](results/full/config.json); defaults of the pinned sklearn release also apply. The implementation sets Python/NumPy seeds, estimator seed, and one computation thread.

Accuracy measures overall agreement, macro F1 weights the eight classes equally, and weighted F1 is supplementary. Undefined scores are zero. Macro F1 is the development selection criterion because class frequencies differ. These measures assess imitation of dataset annotations, not empathy or patient benefit. Multiple support strategies can be reasonable at one point, so a mismatch is not necessarily a harmful response.

## Completed experiments and results

Both models were trained on the same training set and evaluated on the same **2,722 full-data validation examples**. Higher is better. No test predictions or test metrics were computed.

| Model | Accuracy | Macro F1 | Weighted F1 |
|---|---:|---:|---:|
| Training-majority Question | 0.195812 | 0.040937 | 0.064128 |
| TF-IDF + Logistic Regression | 0.304555 | 0.190134 | 0.256855 |

The absolute accuracy improvement is about **10.87 percentage points**; macro F1 rises by about **0.1492**. Under this fixed validation setup, contextual text features provide a stronger classifier than a constant prediction. However, Logistic Regression recalls only about 0.42% of Reflection of feelings examples, 0.56% of Information, 2.16% of Self-disclosure, and 2.61% of Restatement or Paraphrasing. Its aggregate improvement does not mean all strategies are learned adequately. [Full metrics](results/full/metrics.json) preserve per-class precision/recall/F1 and a labeled confusion matrix; [prediction rows](results/full/validation_predictions.csv) permit recomputation without redistributing message text.

On the bundled greeting demo, both models obtain accuracy **0.750000**, macro F1 **0.107143**, and weighted F1 **0.642857** on 12 validation examples. The models predict the majority for this small set; no benefit is established by this demonstration. These numbers are labeled separately in [sample metrics](results/sample/metrics.json).

## Verification, limitations, and actual challenges

Six automated checks cover past-only construction, context truncation/exclusion, conversation separation, duplicate full-transcript rejection, training-only vocabulary, and majority behavior. The sample runs through actual fitting and evaluation with socket connections disabled; [verification evidence](results/verification.json) records the clean-environment check and resource use. The tested platform is Windows 11/Python 3.14.7. Linux/8 GB verification remains pending because WSL is not configured. A Windows clean clone does not prove Linux execution.

An initial allocation using `floor` exposed binary floating-point rounding: 70% of 1,300 became 909 rather than 910. Rounded allocation corrected this; both experiments and the bundled sample were rebuilt, and the retained evidence uses the corrected split. [Development notes](docs/DEVELOPMENT_NOTES.md) record this correction and the inspection decisions.

Other limitations include class imbalance, possible valid alternative labels, no uncertainty intervals, no participant-disjoint evaluation, and no manual error analysis of validation contexts yet. The context representation loses word order beyond bigrams and does not explicitly encode conversation stages. No trained model checkpoint is saved yet; the small models are refit by the reproducible commands. The current entry point reserves the test set and does not yet implement final test scoring. No generation, retrieval, user interface, safety evaluation, or comparison of chatbot responses has been completed.

## Completion plan and interim conclusion

Before December 7: review errors and class imbalance; compare a Linear SVM and/or a modest class-weight/context refinement on the same validation partition; freeze the chosen design; then add and run final test evaluation once. Investigate a strategy-conditioned generator and compare it with the same generator under a generic emotional-support prompt. Implement a small interface if feasible, and evaluate the proposed 30 fictional scenarios with a predefined rubric covering empathy, clarity, actionable guidance, and information accuracy. Reliable psychology sources must be reviewed before any CBT material is incorporated. Classification metrics will remain separate from response-quality judgments.

Prioritize trustworthy experiments and a reproducible final report over feature breadth. If generation resources or scope become infeasible, discuss any substantial scope adjustment with the instructor; no approval is assumed. Also complete Linux verification, student review, repository publication/access, and the final 2,500–3,500-word report. No external steps were performed by this implementation session.

The defensible interim finding is that a simple contextual text classifier improves validation annotation prediction over a constant baseline, while several strategy recalls remain poor. Whether this improves emotional-support responses is still an open question.

## References

1. Liu, S., Zheng, C., Demasi, O., Sabour, S., Li, Y., Yu, Z., Jiang, Y., & Huang, M. (2021). [Towards Emotional Support Dialog Systems](https://aclanthology.org/2021.acl-long.269/). ACL-IJCNLP, 3469–3483.
2. CoAI Group. [Emotional-Support-Conversation](https://github.com/thu-coai/Emotional-Support-Conversation), pinned commit listed above, retrieved November 23, 2026. [Source license](data/source/LICENSE).
3. scikit-learn developers. [TfidfVectorizer documentation](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html), version 1.9.1.
4. scikit-learn developers. [LogisticRegression documentation](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html), version 1.9.1.

## Contributions and AI Assistance

The student supplied the approved proposal, requirements, project direction, and netid. OpenAI Codex read those documents, created this milestone's Python implementation, selected a neutral real-data sample, inspected the official source/license, ran the experiments and automated checks, and drafted the documentation and interim update. No ESConv neural-model code was copied. sklearn supplied the feature extraction, estimator, and metric implementations.

Codex checked source hashes, inspected actual JSON counts, tested target/future exclusion and group boundaries, ran both real experiments, and performed clean-environment sample verification. These are executed checks, not a claim of independent human review. The student still needs to inspect the code, reproduce the results, understand the choices, and revise/approve the narrative before submission. No assignment was submitted and no one was contacted.
