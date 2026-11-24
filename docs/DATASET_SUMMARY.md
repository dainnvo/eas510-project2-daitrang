# Measured ESConv dataset summary

Generated from `results/full/dataset_summary.json`; no conversation text is reproduced here.

Source: https://github.com/thu-coai/Emotional-Support-Conversation, commit `f262d062ad74cb39b17ea476facc81568ddcba24`.

- Conversations: **1,300**
- Messages: **38,365** (19,989 seeker; 18,376 supporter)
- Eligible classification examples: **17,693**
- Excluded supporter targets: **683**, all lacking prior nonempty context
- Empty source messages: 0; missing supporter labels: 0
- Exact duplicate full dialogs beyond the first: 0
- Messages per conversation: min 16, max 120, mean 29.5115

## JSON structure

The root is a list. Each item is a conversation object. Its `dialog` is an ordered list of message objects with `speaker`, `content`, and `annotation`. Supporter annotations contain `strategy`; some seeker annotations contain `feedback`. Neither strategy annotations nor feedback become input features.

Conversation fields: `experience_type`, `emotion_type`, `problem_type`, `situation`, `survey_score`, `dialog`, `seeker_question1`, `seeker_question2`, `supporter_question1`, `supporter_question2`.

Only preceding dialog message roles and content enter classifier inputs. Situation descriptions, experience/emotion/problem metadata, surveys, and question responses are excluded.

## Strategy counts

Labels below preserve actual JSON spelling, including `Question` and `Others`. Brackets in upstream `strategy.json` are formatting, not part of the target strings.

| Strategy | Raw supporter messages | Eligible targets | Train | Validation | Reserved test |
|---|---:|---:|---:|---:|---:|
| Question | 3,801 | 3,336 | 2,324 | 533 | 479 |
| Restatement or Paraphrasing | 1,089 | 1,085 | 778 | 153 | 154 |
| Reflection of feelings | 1,436 | 1,434 | 996 | 236 | 202 |
| Self-disclosure | 1,713 | 1,713 | 1,173 | 278 | 262 |
| Affirmation and Reassurance | 2,827 | 2,817 | 2,008 | 425 | 384 |
| Providing Suggestions | 2,954 | 2,948 | 2,041 | 438 | 469 |
| Information | 1,215 | 1,214 | 852 | 177 | 185 |
| Others | 3,341 | 3,146 | 2,210 | 482 | 454 |

## Conversation-grouped split

Seed 510; sorted IDs, local seeded shuffle, rounded 70% training and 15% validation, remainder test. No stratification or participant grouping. All examples from each conversation share its partition.

| Partition | Conversations | Examples |
|---|---:|---:|
| train | 910 | 12,382 |
| validation | 195 | 2,722 |
| test | 195 | 2,589 |

Test labels are counted for data description only; no test predictions or metrics were computed.

## Raw problem-category values

These are descriptive metadata, not features. There are 13 raw strings; the two parent-conflict variants and inconsistent capitalization are retained rather than silently harmonized.

| Raw value | Conversations |
|---|---:|
| job crisis | 280 |
| problems with friends | 179 |
| ongoing depression | 351 |
| breakup with partner | 239 |
| academic pressure | 156 |
| conflict with parents | 10 |
| Procrastination | 13 |
| Alcohol Abuse | 12 |
| Issues with Parents | 8 |
| Sleep Problems | 28 |
| Appearance Anxiety | 12 |
| School Bullying | 2 |
| Issues with Children | 10 |

## Preliminary validation recall

Recall shows how often a true class was recovered. Very low recalls remain an important limitation despite the overall improvement.

| Strategy | Majority recall | Logistic Regression recall |
|---|---:|---:|
| Question | 1.0000 | 0.4784 |
| Restatement or Paraphrasing | 0.0000 | 0.0261 |
| Reflection of feelings | 0.0000 | 0.0042 |
| Self-disclosure | 0.0000 | 0.0216 |
| Affirmation and Reassurance | 0.0000 | 0.2353 |
| Providing Suggestions | 0.0000 | 0.5114 |
| Information | 0.0000 | 0.0056 |
| Others | 0.0000 | 0.4938 |

The bundled 80-excerpt greeting demo is separately summarized in `results/sample/dataset_summary.json`. Its target contents are deliberately blanked, and repeated short contexts are expected. Its metrics demonstrate execution only.
