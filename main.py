"""Offline sample by default; full ESConv development experiment with --full."""
import argparse
from collections import Counter
import csv
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import platform
import random
import time

# Set before numpy/sklearn imports; keep CPU and memory needs modest.
for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[key] = "1"
import numpy as np

import config
from src.data import audit_split, build_examples, inspect, load_conversations, save_json, split_conversations
from src.models import evaluate, fit_logistic, majority_label

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true", help="Use locally downloaded, pinned ESConv")
    args = parser.parse_args()
    started = time.perf_counter()
    random.seed(config.SEED)
    np.random.seed(config.SEED)
    mode = "full" if args.full else "sample"
    data_path = ROOT / ("data/raw/ESConv.json" if args.full else "data/sample/greeting_excerpts.json")
    if not data_path.exists():
        parser.error("Data missing. For full data run: python data/download.py")
    data_hash = hashlib.sha256(data_path.read_bytes()).hexdigest()
    if args.full and data_hash != config.SOURCE_SHA256["ESConv.json"]:
        raise ValueError("Full dataset checksum differs from the pinned source")
    conversations = load_conversations(data_path, sample=not args.full)
    splits = split_conversations([cid for cid, _ in conversations])
    audit = audit_split(conversations, splits)
    examples, exclusions = build_examples(conversations)
    grouped = {name: [e for e in examples if e["conversation_id"] in set(ids)]
               for name, ids in splits.items()}
    if any(not rows for rows in grouped.values()):
        raise ValueError("Each split must contain at least one classification example")
    train, val = grouped["train"], grouped["validation"]
    x_train, y_train = [e["input"] for e in train], [e["label"] for e in train]
    x_val, y_val = [e["input"] for e in val], [e["label"] for e in val]
    majority = majority_label(y_train)
    predictions = {"majority": [majority] * len(val)}
    model = fit_logistic(x_train, y_train)
    predictions["logistic_tfidf"] = model.predict(x_val).tolist()
    metrics = {name: evaluate(y_val, pred) for name, pred in predictions.items()}
    out = ROOT / "results" / mode
    out.mkdir(parents=True, exist_ok=True)
    summary = inspect(conversations)
    summary.update({"examples_after_cleaning": len(examples), "excluded_supporter_targets": exclusions,
                    "split_conversation_counts": {k: len(v) for k, v in splits.items()},
                    "split_example_counts": {k: len(v) for k, v in grouped.items()},
                    "eligible_strategy_counts": dict(Counter(e["label"] for e in examples)),
                    "split_strategy_counts": {k: dict(Counter(e["label"] for e in v)) for k, v in grouped.items()}})
    save_json(out / "dataset_summary.json", summary)
    save_json(out / "splits.json", splits)
    save_json(out / "metrics.json", {"dataset": mode, "evaluation_split": "validation",
                                   "test_status": "reserved; no predictions or metrics computed",
                                   "models": metrics})
    save_json(out / "config.json", {k: v for k, v in vars(config).items() if k.isupper()})
    save_json(out / "run.json", {
        "dataset": mode, "data_sha256": data_hash, "source_commit": config.SOURCE_COMMIT,
        "python": platform.python_version(), "platform": platform.platform(),
        "dependencies": {p: version(p) for p in ("numpy", "scipy", "scikit-learn", "joblib", "threadpoolctl")},
        "evaluation_split": "validation", "audit": audit,
        "majority_label_fitted_on_train": majority,
        "tfidf_vocabulary_size": len(model.named_steps["tfidf"].vocabulary_),
        "train_matrix_shape": [len(train), len(model.named_steps["tfidf"].vocabulary_)],
        "logistic_iterations": model.named_steps["classifier"].n_iter_.tolist(),
        "thread_limit": 1, "elapsed_seconds": time.perf_counter() - started,
        "selection_rule": "largest validation macro F1; no test-based selection",
        "preliminary_validation_choice": max(metrics, key=lambda k: metrics[k]["macro_f1"]),
    })
    with (out / "validation_predictions.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["example_id", "conversation_id", "target_index", "true_label", *predictions])
        for i, e in enumerate(val):
            writer.writerow([e["example_id"], e["conversation_id"], e["target_index"], e["label"],
                             *(p[i] for p in predictions.values())])
    with (out / "comparison.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["dataset", "split", "model", "n", "accuracy", "macro_f1", "weighted_f1"])
        for name, m in metrics.items():
            writer.writerow([mode, "validation", name, m["n_examples"], m["accuracy"], m["macro_f1"], m["weighted_f1"]])
    # Context-bearing derived data stays local and ignored, just like raw ESConv.
    processed = ROOT / "data/processed" / mode
    processed.mkdir(parents=True, exist_ok=True)
    for name, rows in grouped.items():
        with (processed / f"{name}.jsonl").open("w", encoding="utf-8") as f:
            for e in rows:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
    print(f"Dataset: {mode}; validation only; test reserved")
    print(f"Conversations: {len(conversations)}; usable examples: {len(examples)}")
    for name, m in metrics.items():
        print(f"{name}: accuracy={m['accuracy']:.6f} macro_F1={m['macro_f1']:.6f} weighted_F1={m['weighted_f1']:.6f}")
    print(f"Saved evidence: {out}")


if __name__ == "__main__":
    main()
