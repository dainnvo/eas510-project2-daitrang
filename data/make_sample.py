"""Build a small, non-sensitive ESConv excerpt sample; no invented labels/text."""
from collections import Counter
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import config
from src.data import load_conversations, save_json, split_conversations

# Exact manually reviewed neutral greeting strings; no personal disclosures.
GREETING_ALLOWLIST = {"Hello", "hello", "Hi", "hi", "Hello.", "Hello?", "Hi there",
                      "Hi, how are you?", "Hi.", "Hi!", "Hey", "Hello!", "hi there",
                      "Hello there", "Good afternoon", "Good evening", "hello?",
                      "Hello there.", "Hi. How are you?", "HI", "Good morning"}


def main():
    conversations = load_conversations(ROOT / "data/raw/ESConv.json")
    full_train = set(split_conversations([cid for cid, _ in conversations])["train"])
    candidates = []
    for cid, record in conversations:
        dialog = record["dialog"]
        if (cid in full_train and len(dialog) >= 2 and dialog[0]["speaker"] == "seeker"
                and dialog[0]["content"].strip() in GREETING_ALLOWLIST
                and dialog[1]["speaker"] == "supporter"):
            candidates.append({
                "conversation_id": cid, "sample_excerpt": True,
                "dialog": [{"speaker": "seeker", "content": dialog[0]["content"], "annotation": {}},
                           {"speaker": "supporter", "content": "", "annotation": {
                               "strategy": dialog[1]["annotation"]["strategy"]}}]})
    if len(candidates) < config.SAMPLE_CONVERSATIONS:
        raise ValueError("Not enough eligible excerpts")
    random.Random(config.SEED).shuffle(candidates)
    sample = sorted(candidates[:config.SAMPLE_CONVERSATIONS], key=lambda r: r["conversation_id"])
    save_json(ROOT / "data/sample/greeting_excerpts.json", sample)
    save_json(ROOT / "data/sample/selection.json", {
        "source_commit": config.SOURCE_COMMIT, "seed": config.SEED,
        "eligible_conversations": len(candidates), "selected_conversations": len(sample),
        "source_partition": "full-data training conversations only",
        "greeting_allowlist": sorted(GREETING_ALLOWLIST),
        "strategy_counts": dict(Counter(r["dialog"][1]["annotation"]["strategy"] for r in sample)),
        "modifications": "Keep only neutral first seeker message and next strategy label; blank target content; remove all metadata and subsequent messages.",
        "purpose": "Offline pipeline check only; narrow real-data excerpt, not representative model-quality evidence."})
    print(f"Saved {len(sample)} real greeting excerpts from {len(candidates)} eligible training conversations")


if __name__ == "__main__":
    main()
