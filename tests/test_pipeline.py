"""Meaningful leakage safeguards on invented fixtures, not ESConv disclosures."""
import unittest

from src.data import audit_split, build_examples, split_conversations
from src.models import fit_logistic, majority_label


class LeakageTests(unittest.TestCase):
    def test_target_future_metadata_and_annotations_do_not_enter_input(self):
        record = {"situation": "SECRET_METADATA", "dialog": [
            {"speaker": "seeker", "content": "PAST_ONLY", "annotation": {"feedback": "SECRET_FEEDBACK"}},
            {"speaker": "supporter", "content": "SECRET_TARGET", "annotation": {"strategy": "Question"}},
            {"speaker": "seeker", "content": "SECRET_FUTURE"}]}
        rows, _ = build_examples([("a", record)])
        self.assertEqual(rows[0]["input"], "seeker: PAST_ONLY")
        record["dialog"][1]["content"] = "CHANGED_TARGET"
        record["dialog"][2]["content"] = "CHANGED_FUTURE"
        self.assertEqual(rows, build_examples([("a", record)])[0])

    def test_context_window_and_no_context_exclusion(self):
        dialog = [{"speaker": "supporter", "content": "first", "annotation": {"strategy": "Others"}},
                  {"speaker": "seeker", "content": "old"},
                  {"speaker": "seeker", "content": "recent"},
                  {"speaker": "supporter", "content": "target", "annotation": {"strategy": "Question"}}]
        rows, exclusions = build_examples([("a", {"dialog": dialog})], context_messages=1)
        self.assertEqual(exclusions, {"no_nonempty_prior_context": 1})
        self.assertEqual(rows[0]["input"], "seeker: recent")

    def test_every_conversation_stays_in_one_split(self):
        ids = [f"c{i}" for i in range(30)]
        split = split_conversations(ids)
        self.assertEqual(split, split_conversations(list(reversed(ids))))
        self.assertEqual(set().union(*(set(s) for s in split.values())), set(ids))
        self.assertFalse(set(split["train"]) & set(split["validation"]))
        self.assertFalse(set(split["test"]) & set(split["train"]))
        self.assertFalse(set(split["test"]) & set(split["validation"]))

    def test_duplicate_transcripts_across_groups_rejected(self):
        conv = {"dialog": [{"speaker": "seeker", "content": "same"}]}
        with self.assertRaises(ValueError):
            audit_split([("a", conv), ("b", conv)], {"train": ["a"], "validation": ["b"], "test": []})

    def test_preprocessing_does_not_learn_validation_only_word(self):
        model = fit_logistic(["trainingword hello", "different hello"], ["Others", "Question"])
        vectorizer = model.named_steps["tfidf"]
        transformed = vectorizer.transform(["validationsecret"])
        self.assertNotIn("validationsecret", vectorizer.vocabulary_)
        self.assertEqual(transformed.nnz, 0)

    def test_majority_uses_passed_training_labels_and_stable_ties(self):
        self.assertEqual(majority_label(["Others", "Question", "Question"]), "Question")
        self.assertEqual(majority_label(["Question", "Others"]), "Others")


if __name__ == "__main__":
    unittest.main()
