# Checkpoint report: support-strategy classification

**Dai Trang Vo - EAS 510 Project 2 - November 23, 2026**

This report describes my progress at the first checkpoint. I will expand it for the final submission.

## Question and data

For this checkpoint, my main question is whether recent conversation text can predict the next support-strategy label better than always choosing the most common training label. This is the first part of my plan to use a predicted strategy to guide a chatbot's response.

The official [ESConv repository](https://github.com/thu-coai/Emotional-Support-Conversation) accompanies [Liu et al. (2021)](https://aclanthology.org/2021.acl-long.269/). The downloaded version contains **1,300 conversations, 38,365 messages, and eight strategy labels**. The source commit, URLs, and hashes are recorded in [acquisition.json](data/source/acquisition.json); permissions and sample modifications are in [DATA_USAGE.md](DATA_USAGE.md).

The [dataset summary](results/full/dataset_summary.json) records the fields, label counts, and missing values found in the file. The inspection found no empty messages, missing supporter labels, or exact duplicate full conversations. However, 683 supporter messages appear at the start of a conversation, with no earlier message to use as input. Removing these leaves **17,693 examples**.

The small sample included in the repository contains 80 neutral greetings from ESConv, together with the original strategy label of the next response. Response text, later messages, and conversation metadata have been removed. All excerpts come from full-training conversations; [selection.json](data/sample/selection.json) records how they were chosen. I use this sample to demonstrate the code without including personal disclosures. Its repeated greetings and missing classes mean its scores cannot represent performance on the full dataset.

## Method

Each example represents the point just before a supporter replies. The input contains up to six earlier messages, marked with the speaker's role. In the code, the slice is `dialog[max(0, i - 6):i]`, where `i` is the target response's index. Because the slice stops before `i`, it excludes the response being predicted. Future messages, strategy annotations, situation descriptions, and surveys are also excluded. Earlier supporter replies can be part of the observed history, but their labels are not included.

The split is made by conversation because several examples can share messages from the same conversation. Sorted conversation IDs are shuffled with seed 510, then divided into roughly 70% training, 15% validation, and 15% test. This gives **910/195/195 conversations** and **12,382/2,722/2,589 examples**, respectively. Each conversation stays in one split, and the code rejects exact duplicate full conversations across splits. It does not establish whether the same participant appears in different conversations.

The baseline always predicts **Question**, the most common label in the training set. If two labels had equal counts, alphabetical order would break the tie. I chose this simple reference to see whether the text model learns anything beyond class frequency.

The comparison model uses sklearn TF-IDF and multinomial Logistic Regression. TF-IDF converts the messages into numerical features using individual words and pairs of adjacent words. Text is lowercased, tokens must contain at least two characters, and up to 20,000 training features are kept. Stop words are retained. For a word count `c > 0`, term frequency is `1 + ln(c)`. Smoothed IDF is `ln((1 + N)/(1 + df)) + 1`, where `N` is the number of training examples and `df` is the number containing that feature. The product is L2-normalized. Vocabulary and IDF are fitted on training text only and reused for validation.

Logistic Regression uses L2 regularization (`l1_ratio=0`, `C=1`), `lbfgs`, no class weighting, tolerance `1e-4`, and at most 1,000 iterations. The full run converged in 95 iterations. There was no hyperparameter search. [config.py](config.py) contains seeds and settings.

## Actual results

The table below compares both models on the same 2,722 validation examples. Higher scores are better.

| Model | Accuracy | Macro F1 | Weighted F1 |
|---|---:|---:|---:|
| Majority | 0.195812 | 0.040937 | 0.064128 |
| TF-IDF + Logistic Regression | 0.304555 | 0.190134 | 0.256855 |

Accuracy is overall label agreement. Macro F1 weights all eight classes equally; weighted F1 weights by class frequency. Undefined class scores are zero. [Saved metrics](results/full/metrics.json) include per-class scores and confusion matrices; [prediction rows](results/full/validation_predictions.csv) allow independent recomputation.

Logistic Regression improves accuracy by 10.87 percentage points. However, it still misses most examples of Reflection of feelings, Information, Self-disclosure, and Restatement or Paraphrasing, with recall below 3% for each. This tells me that the overall improvement does not extend equally to all strategies. Also, several strategies could be reasonable in one situation, so agreement with the recorded label does not fully measure the quality of support. The test set has not been evaluated, and there is no response-quality or clinical evaluation yet.

On the greeting sample, both models obtain validation accuracy 0.750000 and macro F1 0.107143 on 12 examples. Those results check pipeline execution only.

## Checks, challenges, and completion plan

All six automated tests pass, including the checks for target/future exclusion and conversation separation. A fresh copy of the repository reproduced the sample on Windows with Python 3.14.7, network connections disabled, and only the listed runtime dependencies installed. [verification.json](results/verification.json) records the tested commit and measurements. Accuracy and macro F1 were also recomputed directly from the saved predictions. Linux testing is still needed.

One issue during development was the split calculation. Floating-point rounding initially produced 909 training conversations instead of 910. The allocation was corrected, and both experiments and the sample were rebuilt. The saved results use the corrected split. Class imbalance remains a challenge, and uncertainty intervals and a closer review of individual errors are still needed.

My next step is to review validation errors and compare a Linear SVM or a small change to class weights or context length. I will settle the model choices before evaluating the test set. After that, I plan to connect the predicted strategy to a response generator and build a simple interface. The planned response comparison uses the same 30 fictional scenarios for the strategy-guided and generic-prompt versions, with a rubric defined before scoring. I also need to review reliable CBT sources, check Linux execution, and finish the final report by December 7. If the remaining scope becomes unrealistic, I will discuss any substantial change with the instructor.

## Contributions and AI Assistance

I developed the proposal and chose the project direction. I used OpenAI Codex to help implement the code, inspect ESConv and its terms, run experiments and tests, and draft and edit the writeups. Checks completed with Codex included file-hash verification, inspection of dataset counts, leakage tests, a fresh-environment sample run, and recalculation of metrics from saved predictions. These checks do not replace my own review and understanding of the work before submission. sklearn provides [TF-IDF](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html), [Logistic Regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html), and the metrics. No ESConv model code was copied.
