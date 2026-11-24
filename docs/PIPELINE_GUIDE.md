# How to explain this milestone

## 1. What is one observation?

One observation is a decision point immediately before a labeled supporter message. `y` is that response's existing strategy label. `X` is text from at most six messages **before** that response, with `seeker:`/`supporter:` prefixes. We predict the annotation a supporter used, not the uniquely correct or clinically best strategy.

For this invented illustration:

```text
0 seeker: My assignment is difficult.
1 supporter: Which part is hardest?   [Question]
2 seeker: I do not know how to start.
3 supporter: Let's choose one task.  [Providing Suggestions]
```

The target at index 3 has input messages 0, 1, and 2, and label `Providing Suggestions`. Message 3 and its text never enter its input. The earlier supporter text at index 1 is valid observed history. Its **annotation** is excluded. Consecutive supporter messages can also be targets: the previous message is available history, but the current response is excluded.

The code uses `dialog[max(0, i - 6):i]`; Python's slice excludes the upper bound. This is the core leakage safeguard. It does not read the post-conversation survey, situation description, feedback, future messages, or any strategy annotation into the text features.

## 2. Why remove some targets?

683 supporter messages start their conversation and have no preceding message. The experiment excludes these because there is no context to classify. This changes label counts, especially Question, so both original and eligible counts are saved. No messages are empty in the full source, and every supporter has a known strategy. Labels retain exact upstream spelling/case. Unknown labels raise an error rather than silently disappearing. Individual messages are not merged into larger turns.

## 3. Why split conversations first?

Several examples reuse a conversation's context. Randomly splitting those examples could put almost identical history into training and validation. Instead, sort stable conversation IDs, shuffle once with seed 510, allocate rounded 70% training and 15% validation counts, and put the remainder in test. All examples inherit their conversation's split. The audit checks disjoint IDs and rejects exact duplicate full transcripts across splits. It does not establish that participants are disjoint; no participant IDs are available.

The bundled sample comes only from full-data training conversations, so demo fitting cannot expose full validation/test contexts. It then has its own sample split. Its repetitive neutral greetings are intentional and are not useful generalization evidence.

## 4. What does the baseline learn?

Count **training labels only**, choose the largest count, and predict that label everywhere in validation. Alphabetical order breaks any tie. Full-data training's majority is `Question`. It gets 533 of 2,722 validation labels correct (19.58%). This is the reference that a useful contextual classifier should improve on.

## 5. How does text become numbers?

Logistic Regression accepts a numeric matrix, not raw strings. `TfidfVectorizer` lowercases the text, extracts word tokens of at least two characters, and builds single-word and two-word features. Punctuation is discarded; role words remain. It keeps at most 20,000 features from training text only. No stop-word list or embeddings are used.

For a feature appearing `c > 0` times in a document, sublinear term frequency is `tf = 1 + ln(c)`; absent features have zero weight. With `N` training documents and feature document frequency `df`, smoothed inverse document frequency is `idf = ln((1 + N)/(1 + df)) + 1`. Multiply `tf * idf`, then divide the vector by its L2 length. This gives a sparse numeric row: frequent-in-this-context but rarer-across-training features tend to receive larger weights. Validation words unseen during fitting have no vocabulary column.

The fitted full training matrix has **12,382 rows × 20,000 columns**, stored sparsely. The sklearn `Pipeline` fits vocabulary and IDF on training data, then reuses them unchanged for validation.

## 6. What does Logistic Regression do?

It learns a weight for each feature and each class, plus class intercepts. A weighted sum of a document's features becomes a score for each strategy; multinomial softmax converts scores into relative probabilities, and the largest score supplies the prediction. With `lbfgs`, `l1_ratio=0`, and `C=1`, this run uses L2 regularization. It does not use class weighting. `max_iter=1000` is the ceiling, and a convergence warning fails the run; the actual iteration count is saved. No hyperparameter search has been performed.

## 7. Why these metrics?

Accuracy is the fraction of labels predicted correctly. F1 combines precision and recall for one label. Macro F1 averages all eight class F1 scores equally, so a model cannot look good solely by serving common classes. Weighted F1 weights by class frequency and is supplementary. Undefined class scores are explicitly zero. These are annotation-agreement metrics; none measures empathy, helpfulness, clinical safety, or response quality.

Compare both models on the same validation examples. Freeze design choices before evaluating the reserved test set. The current entry point deliberately computes no test metrics. The plan is to add final test evaluation once model selection is complete, not repeatedly tune against test results.

## 8. What can we conclude?

On this fixed validation split, TF-IDF/Logistic Regression improves macro F1 from 0.040937 to 0.190134 and accuracy from 0.195812 to 0.304555. This suggests contextual text has some predictive signal under this setup. Several rare strategies have near-zero recall, and no statistical uncertainty or participant-level generalization has been assessed. We cannot conclude the chatbot improves emotional support; response generation has not been implemented or evaluated.
