"""All experiment choices live here; change them before running, not after test use."""
SEED = 510
CONTEXT_MESSAGES = 6
TRAIN_FRACTION = 0.70
VALIDATION_FRACTION = 0.15
SAMPLE_CONVERSATIONS = 80
SOURCE_REPOSITORY = "https://github.com/thu-coai/Emotional-Support-Conversation"
SOURCE_COMMIT = "f262d062ad74cb39b17ea476facc81568ddcba24"
SOURCE_SHA256 = {
    "ESConv.json": "aa0556c5b330562ba009c1cd5137486bfa2a7255f33225a6524cd58f7efdd9af",
    "LICENSE": "82656a050544ab820c9aa7b61433f5181f8e80cacd042377140962a3e3eb5721",
    "README.md": "1bd60ad3126c01cd466561860c26b5e96e69c93f689ea2603421f5fcf6b43e61",
    "strategy.json": "79d335ea4d5b2e460cf2f1ffab100b2d7486624f9554de7927713e941458c73c",
}
LABELS = [
    "Question", "Restatement or Paraphrasing", "Reflection of feelings",
    "Self-disclosure", "Affirmation and Reassurance", "Providing Suggestions",
    "Information", "Others",
]
TFIDF = {
    "lowercase": True, "ngram_range": (1, 2), "min_df": 1,
    "max_features": 20000, "sublinear_tf": True, "smooth_idf": True,
    "norm": "l2", "stop_words": None,
    "token_pattern": r"(?u)\b\w\w+\b",
}
LOGISTIC = {"C": 1.0, "l1_ratio": 0.0, "fit_intercept": True,
            "solver": "lbfgs", "max_iter": 1000,
            "tol": 1e-4, "class_weight": None, "random_state": SEED}
