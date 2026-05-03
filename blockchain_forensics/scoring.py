"""Confidence scoring for clusters."""

from typing import Dict


def score_clusters(evidence_counts: Dict[str, int]) -> Dict[str, float]:
    """Score clusters using a simple capped linear scale.

    Score = min(1.0, evidence / 5). This rewards repeated input co-occurrence
    without claiming absolute certainty.
    """
    scores: Dict[str, float] = {}
    for cluster_id, evidence in evidence_counts.items():
        score = evidence / 5.0
        if score > 1.0:
            score = 1.0
        scores[cluster_id] = round(score, 2)
    return scores
