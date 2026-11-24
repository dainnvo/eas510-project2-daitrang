# EAS 510 Project 2: Interim Update

Dai Trang Vo (daitrang) | November 23, 2026 | Draft for student review

## Question and completed progress

Can recent conversation context predict the next ESConv support-strategy label better than a majority-class predictor? I now have a runnable classification milestone, rather than a completed chatbot. The implementation downloads ESConv from its official CoAI repository at a pinned commit, verifies checksums, and records its schema, counts, labels, and usage conditions. The source contains 1,300 conversations and 38,365 messages. CC BY-NC 4.0 and the upstream academic-research notice are documented in DATA_USAGE.md.

Each example uses up to six messages before a labeled supporter response; target/future responses and annotations never enter the input. Excluding 683 context-free opening responses leaves 17,693 examples. A seeded conversation split produces 910/195/195 conversations and 12,382/2,722/2,589 examples for training/validation/test. Vocabulary and IDF are fitted only on training data. A majority baseline and TF-IDF word-unigram/bigram Logistic Regression both run through main.py. An offline 80-greeting real-data excerpt demo excludes personal disclosures; its scores test execution only. Six leakage/split/model checks pass. Dataset summaries, metrics, and configurations are in results/full/ and results/sample/.

## Preliminary results

On the same 2,722 full-data validation examples, majority prediction obtains accuracy 0.195812 and macro F1 0.040937. Logistic Regression obtains accuracy 0.304555 and macro F1 0.190134. Macro F1 weights all eight strategies equally. The test set remains reserved. These results show improved annotation prediction under this split, not improved empathy or clinical usefulness. Configurations, per-class metrics, confusion matrices, split IDs, and prediction labels are saved. Sample validation accuracy is 0.750000 for both models and is not model-quality evidence.

## Challenges and limitations

Class imbalance remains difficult: Logistic Regression recall is below 3% for four strategies. Several labels may be reasonable for one context. A floating-point split-allocation issue was corrected and both experiments rerun. The small bundled greeting sample is repetitive and unrepresentative. Testing is on Windows/Python 3.14.7; Linux verification remains pending. Response generation, CBT retrieval, the chat interface, and response-quality evaluation are not implemented. No test-set result or clinical benefit is claimed.

## Plan through December 7

November 24–29: inspect validation errors, compare Linear SVM or a modest class-weight/context refinement, and verify Linux execution. November 30–December 3: implement strategy-conditioned generation and a simple interface if feasible; compare against the same generator with a generic support prompt on 30 fictional scenarios using a predefined rubric. December 4–7: freeze model choices, evaluate the reserved test set once, finish the report and reproducibility checks, and document limitations. Prioritize defensible comparisons; request approval if a substantial scope reduction becomes necessary.

Local repository: eas510-project2-daitrang; a remote URL still needs to be created by the student. Codex assisted with implementation, experiments, checks, and drafting; student review is pending. No submission or contact was made. Sources: Liu et al. (ACL 2021), aclanthology.org/2021.acl-long.269/; github.com/thu-coai/Emotional-Support-Conversation.
