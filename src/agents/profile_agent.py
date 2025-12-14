from pathlib import Path
import yaml
from typing import List

from src.schemas.profile import Profile, Education
from src.tools.pdf import extract_text_from_pdf


class ProfileAgent:
    """
    ProfileAgent is responsible for constructing a validated Profile
    object from raw user inputs (YAML + CV PDF).
    """

    def __init__(self, profile_dir: Path):
        self.profile_dir = profile_dir
        self.cv_path = profile_dir / "cv.pdf"
        self.yaml_path = profile_dir / "profile.yaml"

    def load_yaml(self) -> dict:
        if not self.yaml_path.exists():
            raise FileNotFoundError(f"Missing profile.yaml at {self.yaml_path}")

        with open(self.yaml_path, "r") as f:
            return yaml.safe_load(f)

    def load_cv_text(self) -> str:
        if not self.cv_path.exists():
            raise FileNotFoundError(f"Missing cv.pdf at {self.cv_path}")

        return extract_text_from_pdf(self.cv_path)

    def infer_skills_from_cv(self, cv_text: str, seed_skills: List[str]) -> List[str]:
        """
        VERY lightweight skill enrichment.
        No LLM. No hallucination.
        """
        cv_text_lower = cv_text.lower()
        enriched = set(seed_skills)

        COMMON_SKILLS = [
            "python", "pytorch", "machine learning", "deep learning",
            "gan", "diffusion", "data analysis", "linux"
        ]

        for skill in COMMON_SKILLS:
            if skill in cv_text_lower:
                enriched.add(skill)

        return sorted(enriched)

    def build_profile(self) -> Profile:
        yaml_data = self.load_yaml()
        cv_text = self.load_cv_text()
        print(yaml_data)
        education = Education(
            degree=yaml_data["education"]["degree"],
            field=yaml_data["education"]["field"],
            institution=yaml_data["education"]["institution"],
            thesis_title=yaml_data["education"].get("thesis_title"),
            thesis_keywords=yaml_data["education"].get("thesis_keywords", []),
        )

        skills = self.infer_skills_from_cv(
            cv_text=cv_text,
            seed_skills=yaml_data.get("skills", [])
        )

        profile = Profile(
            name=yaml_data["name"],
            education=education,
            research_interests=yaml_data["research_interests"],
            skills=skills,
            preferences=yaml_data.get("preferences", {}),
        )

        return profile
