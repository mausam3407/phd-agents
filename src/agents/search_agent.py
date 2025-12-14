import hashlib
from typing import List

from schemas.profile import Profile
from schemas.position import PhDPosition
from tools.web import duckduckgo_search, scrape_page_text


class SearchAgent:
    """
    Discovers PhD positions from the web using free search + scraping.
    """

    def __init__(self, max_results_per_query: int = 5):
        self.max_results = max_results_per_query

    def build_queries(self, profile: Profile) -> List[str]:
        base_terms = [
            "PhD position",
            "doctoral position",
            "PhD vacancy",
        ]

        topics = profile.research_interests[:3]
        queries = []

        for topic in topics:
            for base in base_terms:
                queries.append(f"{base} {topic}")

        return queries

    def url_to_id(self, url: str) -> str:
        return hashlib.md5(url.encode()).hexdigest()

    def discover(self, profile: Profile) -> List[PhDPosition]:
        queries = self.build_queries(profile)
        positions: List[PhDPosition] = []
        seen_urls = set()

        for query in queries:
            urls = duckduckgo_search(query, self.max_results)

            for url in urls:
                if url in seen_urls:
                    continue
                seen_urls.add(url)

                page_text = scrape_page_text(url)
                if not page_text:
                    continue

                try:
                    position = PhDPosition(
                        id=self.url_to_id(url),
                        title=query,
                        description=page_text,
                        url=url,
                    )
                    positions.append(position)
                except Exception:
                    continue

        return positions
