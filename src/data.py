"""ESConv inspection and strictly past-only classification examples."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import random

import config


def save_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_conversations(path, sample=False):
    records = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise ValueError("Expected a JSON list of conversations")
    return [(r["conversation_id"] if sample else f"esconv-{i:04d}", r)
            for i, r in enumerate(records)]


def split_conversations(ids):
    """Shuffle whole conversation IDs, never individual response examples."""
    ids = sorted(ids)
    if len(ids) != len(set(ids)) or len(ids) < 7:
        raise ValueError("Need unique IDs and at least seven conversations")
    random.Random(config.SEED).shuffle(ids)
    n_train = round(len(ids) * config.TRAIN_FRACTION)
    n_val = round(len(ids) * config.VALIDATION_FRACTION)
    return {"train": sorted(ids[:n_train]),
            "validation": sorted(ids[n_train:n_train + n_val]),
            "test": sorted(ids[n_train + n_val:])}


def build_examples(conversations, context_messages=config.CONTEXT_MESSAGES):
    if context_messages < 1:
        raise ValueError("context_messages must be positive")
    examples, exclusions = [], Counter()
    for cid, record in conversations:
        dialog = record["dialog"]
        for i, target in enumerate(dialog):
            if target["speaker"] != "supporter":
                continue
            label = target.get("annotation", {}).get("strategy")
            if label not in config.LABELS:
                raise ValueError(f"Unknown/missing strategy at {cid}:{i}: {label!r}")
            # The exclusive upper bound i is essential: target/future content,
            # annotations, situation descriptions and surveys never enter X.
            start = max(0, i - context_messages)
            history = dialog[start:i]
            messages = [{"speaker": m["speaker"], "content": m.get("content", "").strip()}
                        for m in history if m.get("content", "").strip()]
            if not messages:
                exclusions["no_nonempty_prior_context"] += 1
                continue
            text = "\n".join(f"{m['speaker']}: {m['content']}" for m in messages)
            examples.append({"example_id": f"{cid}:{i}", "conversation_id": cid,
                             "target_index": i, "context_start_index": start,
                             "context_end_index_exclusive": i,
                             "input": text, "label": label})
    return examples, dict(exclusions)


def inspect(conversations):
    records = [r for _, r in conversations]
    messages = [m for r in records for m in r["dialog"]]
    supporters = [m for m in messages if m["speaker"] == "supporter"]
    fingerprints = Counter(hashlib.sha256(json.dumps(
        [(m["speaker"], m.get("content", "")) for m in r["dialog"]],
        ensure_ascii=False).encode()).hexdigest() for r in records)
    return {
        "conversations": len(records), "messages": len(messages),
        "conversation_field_counts": dict(Counter(k for r in records for k in r)),
        "message_field_counts": dict(Counter(k for m in messages for k in m)),
        "annotation_field_counts": dict(Counter(k for m in messages for k in m.get("annotation", {}))),
        "speaker_counts": dict(Counter(m["speaker"] for m in messages)),
        "raw_supporter_strategy_counts": dict(Counter(m.get("annotation", {}).get("strategy") for m in supporters)),
        "problem_type_counts": dict(Counter(r.get("problem_type", "not included") for r in records)),
        "empty_message_contents": sum(not m.get("content", "").strip() for m in messages),
        "supporters_without_strategy": sum(not m.get("annotation", {}).get("strategy") for m in supporters),
        "exact_duplicate_dialogs_beyond_first": sum(n - 1 for n in fingerprints.values()),
        "messages_per_conversation": {"min": min(len(r["dialog"]) for r in records),
                                      "max": max(len(r["dialog"]) for r in records),
                                      "mean": len(messages) / len(records)},
    }


def audit_split(conversations, splits):
    sets = {k: set(v) for k, v in splits.items()}
    if sets["train"] & sets["validation"] or sets["train"] & sets["test"] or sets["validation"] & sets["test"]:
        raise ValueError("A conversation appears in multiple splits")
    if set.union(*sets.values()) != {cid for cid, _ in conversations}:
        raise ValueError("Split IDs must cover exactly the available conversations")
    # Reject exact duplicate full transcripts across groups, if any.
    # Sample contains deliberately truncated greetings; those are not full transcripts.
    seen = {}
    for cid, r in conversations:
        if r.get("sample_excerpt"):
            continue
        key = json.dumps([(m["speaker"], m.get("content", "")) for m in r["dialog"]])
        group = next(k for k, ids in sets.items() if cid in ids)
        if key in seen and seen[key] != group:
            raise ValueError("Duplicate full transcript crosses split boundaries")
        seen[key] = group
    return {"conversation_overlap": 0, "duplicate_full_transcript_overlap": 0,
            "test_evaluated": False}
