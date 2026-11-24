# EAS 510 Project 2: Interim Update

Dai Trang Vo (daitrang) | November 23, 2026

## Progress

My project explores whether choosing a support strategy before generating a reply can help organize an emotional-support conversation. For this checkpoint, I focused on the classification step: predicting the next supporter response's strategy from earlier messages. The pipeline now loads ESConv from a fixed version of the official repository, checks file hashes, and records the dataset's fields and labels. ESConv contains 1,300 conversations and 38,365 messages. Its license and academic-use conditions are documented in DATA_USAGE.md.

Each input uses up to six messages before the target response. The response itself, future messages, and annotations are excluded. Removing 683 opening responses without earlier context leaves 17,693 examples. The training, validation, and test sets contain 910, 195, and 195 conversations, respectively, with every conversation kept in one split. Both the majority baseline and TF-IDF Logistic Regression run through main.py. A small greeting sample also allows an offline run without including personal disclosures. All six automated checks pass. Dataset summaries, settings, and results are saved under results/.

## Preliminary results

On the same 2,722 validation examples, the majority baseline has accuracy 0.195812 and macro F1 0.040937. Logistic Regression reaches accuracy 0.304555 and macro F1 0.190134. Macro F1 gives equal weight to all eight strategies. This improvement suggests that the text features help predict the recorded labels, although it does not show whether generated responses would be more helpful. The test set has not been evaluated. Both models reach 0.750000 accuracy on the small greeting sample, which is only a check that the pipeline runs.

## Challenges

The classifier still misses most examples of four strategies, with recall below 3% for each. Class imbalance may contribute to this, and I need to look more closely at the errors. Also, more than one strategy can be reasonable in a conversation, so matching one recorded label has limitations. The code has been tested on Windows with Python 3.14.7; Linux testing is still needed. Response generation, CBT retrieval, the interface, and response-quality evaluation are not implemented yet.

## Plan through December 7

During November 24–29, I plan to review validation errors, try Linear SVM or a small change to class weights or context length, and check Linux execution. During November 30–December 3, I aim to connect the classifier to a response generator and build a simple interface. The response comparison will use the same 30 fictional scenarios for strategy-guided and generic-prompt versions, with a rubric defined before scoring. During December 4–7, I will settle the model choices, evaluate the test set once, and finish the report and reproducibility checks. If the remaining scope becomes unrealistic, I will discuss any substantial change with the instructor.

Repository: https://github.com/dainnvo/eas510-project2-daitrang

I used OpenAI Codex for help with implementation, experiments, checks, and writing. Sources: Liu et al. (ACL 2021), aclanthology.org/2021.acl-long.269/; github.com/thu-coai/Emotional-Support-Conversation.
