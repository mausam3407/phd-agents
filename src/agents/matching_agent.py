from typing import List
from schemas.profile import Profile
from schemas.position import PhDPosition
from dataclasses import dataclass

from tools.embeddings import embed_texts, cosine_similarity


@dataclass
class MatchResult:
    position: PhDPosition
    score: float
    explanation: List[str]


class MatchingAgent:
    """
    MatchingAgent ranks PhD positions against a candidate profile
    using embeddings + deterministic rules.
    """

    def __init__(self, min_score: float = 0.3):
        self.min_score = min_score

    def build_profile_text(self, profile: Profile) -> str:
        """
        Convert structured profile into a semantic text block.
        """
        parts = [
            profile.education.field,
            profile.education.thesis_title or "",
            " ".join(profile.education.thesis_keywords),
            " ".join(profile.research_interests),
            " ".join(profile.skills),
        ]
        return " ".join(parts)

    def build_position_text(self, position: PhDPosition) -> str:
        return " ".join([
            position.title,
            position.description,
            " ".join(position.requirements),
            position.supervisor or "",
            position.institution or "",
        ])

    def rule_based_checks(self, profile: Profile, position: PhDPosition) -> List[str]:
        """
        Hard constraints + soft signals.
        """
        reasons = []

        # Country preference
        preferred_countries = profile.preferences.get("countries")
        if preferred_countries and position.country:
            if position.country in preferred_countries:
                reasons.append(f"Located in preferred country: {position.country}")

        # Degree compatibility
        if "phd" not in position.title.lower():
            reasons.append("Position may not explicitly be a PhD role")

        # Field overlap
        for keyword in profile.education.thesis_keywords:
            if keyword.lower() in position.description.lower():
                reasons.append(f"Thesis keyword '{keyword}' appears in position description")

        return reasons

    def match(
        self,
        profile: Profile,
        positions: List[PhDPosition]
    ) -> List[MatchResult]:

        profile_text = self.build_profile_text(profile)
        position_texts = [self.build_position_text(p) for p in positions]

        profile_emb = embed_texts([profile_text])[0]
        position_embs = embed_texts(position_texts)

        results: List[MatchResult] = []

        for pos, emb in zip(positions, position_embs):
            semantic_score = cosine_similarity(profile_emb, emb)

            if semantic_score < self.min_score:
                continue

            explanations = self.rule_based_checks(profile, pos)
            explanations.insert(0, f"Semantic similarity score: {semantic_score:.2f}")

            results.append(
                MatchResult(
                    position=pos,
                    score=float(round(semantic_score, 3)),
                    explanation=explanations
                )
            )

        # Sort best → worst
        results.sort(key=lambda x: x.score, reverse=True)
        return results
