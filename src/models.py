"""Training-only majority class and TF-IDF + multinomial Logistic Regression.

Uses sklearn APIs, not code copied from the ESConv model implementations.
References: https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction
"""
from collections import Counter
import warnings

from sklearn.exceptions import ConvergenceWarning
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.pipeline import Pipeline

import config


def majority_label(y):
    counts = Counter(y)
    # Explicit alphabetical tie-breaking makes this independent of row order.
    return sorted(counts, key=lambda label: (-counts[label], label))[0]


def fit_logistic(texts, labels):
    model = Pipeline([("tfidf", TfidfVectorizer(**config.TFIDF)),
                      ("classifier", LogisticRegression(**config.LOGISTIC))])
    with warnings.catch_warnings():
        warnings.simplefilter("error", ConvergenceWarning)
        model.fit(texts, labels)
    return model


def evaluate(y_true, y_pred):
    return {"n_examples": len(y_true), "accuracy": accuracy_score(y_true, y_pred),
            "macro_f1": f1_score(y_true, y_pred, labels=config.LABELS,
                                  average="macro", zero_division=0),
            "weighted_f1": f1_score(y_true, y_pred, labels=config.LABELS,
                                     average="weighted", zero_division=0),
            "per_class": classification_report(y_true, y_pred, labels=config.LABELS,
                                                 output_dict=True, zero_division=0),
            "confusion_matrix_labels": config.LABELS,
            "confusion_matrix": confusion_matrix(y_true, y_pred, labels=config.LABELS).tolist()}
