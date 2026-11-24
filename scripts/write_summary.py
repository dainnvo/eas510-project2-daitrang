"""Render an aggregate data summary from evidence produced by main.py --full."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import config

s = json.loads((ROOT / "results/full/dataset_summary.json").read_text(encoding="utf-8"))
metrics = json.loads((ROOT / "results/full/metrics.json").read_text(encoding="utf-8"))["models"]
lines = ["# Measured ESConv dataset summary", "",
         "Generated from `results/full/dataset_summary.json`; no conversation text is reproduced here.", "",
         f"Source: {config.SOURCE_REPOSITORY}, commit `{config.SOURCE_COMMIT}`.", "",
         f"- Conversations: **{s['conversations']:,}**",
         f"- Messages: **{s['messages']:,}** ({s['speaker_counts']['seeker']:,} seeker; {s['speaker_counts']['supporter']:,} supporter)",
         f"- Eligible classification examples: **{s['examples_after_cleaning']:,}**",
         f"- Excluded supporter targets: **{sum(s['excluded_supporter_targets'].values()):,}**, all lacking prior nonempty context",
         f"- Empty source messages: {s['empty_message_contents']}; missing supporter labels: {s['supporters_without_strategy']}",
         f"- Exact duplicate full dialogs beyond the first: {s['exact_duplicate_dialogs_beyond_first']}",
         f"- Messages per conversation: min {s['messages_per_conversation']['min']}, max {s['messages_per_conversation']['max']}, mean {s['messages_per_conversation']['mean']:.4f}",
         "", "## JSON structure", "",
         "The root is a list. Each item is a conversation object. Its `dialog` is an ordered list of message objects with `speaker`, `content`, and `annotation`. Supporter annotations contain `strategy`; some seeker annotations contain `feedback`. Neither strategy annotations nor feedback become input features.", "",
         "Conversation fields: " + ", ".join(f"`{k}`" for k in s['conversation_field_counts']) + ".", "",
         "Only preceding dialog message roles and content enter classifier inputs. Situation descriptions, experience/emotion/problem metadata, surveys, and question responses are excluded.", "",
         "## Strategy counts", "",
         "Labels below preserve actual JSON spelling, including `Question` and `Others`. Brackets in upstream `strategy.json` are formatting, not part of the target strings.", "",
         "| Strategy | Raw supporter messages | Eligible targets | Train | Validation | Reserved test |",
         "|---|---:|---:|---:|---:|---:|"]
for label in config.LABELS:
    counts = [s['raw_supporter_strategy_counts'][label], s['eligible_strategy_counts'][label]] + [
        s['split_strategy_counts'][group].get(label, 0) for group in ('train', 'validation', 'test')]
    lines.append("| " + label + " | " + " | ".join(f"{n:,}" for n in counts) + " |")
lines += ["", "## Conversation-grouped split", "", "Seed 510; sorted IDs, local seeded shuffle, rounded 70% training and 15% validation, remainder test. No stratification or participant grouping. All examples from each conversation share its partition.", "",
          "| Partition | Conversations | Examples |", "|---|---:|---:|"]
for group in ('train', 'validation', 'test'):
    lines.append(f"| {group} | {s['split_conversation_counts'][group]:,} | {s['split_example_counts'][group]:,} |")
lines += ["", "Test labels are counted for data description only; no test predictions or metrics were computed.", "",
          "## Raw problem-category values", "", "These are descriptive metadata, not features. There are 13 raw strings; the two parent-conflict variants and inconsistent capitalization are retained rather than silently harmonized.", "",
          "| Raw value | Conversations |", "|---|---:|"]
for name, n in s['problem_type_counts'].items():
    lines.append(f"| {name} | {n} |")
lines += ["", "## Preliminary validation recall", "", "Recall shows how often a true class was recovered. Very low recalls remain an important limitation despite the overall improvement.", "",
          "| Strategy | Majority recall | Logistic Regression recall |", "|---|---:|---:|"]
for label in config.LABELS:
    lines.append(f"| {label} | {metrics['majority']['per_class'][label]['recall']:.4f} | {metrics['logistic_tfidf']['per_class'][label]['recall']:.4f} |")
lines += ["", "The bundled 80-excerpt greeting demo is separately summarized in `results/sample/dataset_summary.json`. Its target contents are deliberately blanked, and repeated short contexts are expected. Its metrics demonstrate execution only.", ""]
(ROOT / "docs/DATASET_SUMMARY.md").write_text("\n".join(lines), encoding="utf-8")
print("Wrote docs/DATASET_SUMMARY.md")
