from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup


def duckduckgo_search(query: str, max_results: int = 5):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_results)
        return [r["href"] for r in results]


def scrape_page_text(url: str, max_chars: int = 4000) -> str:
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception:
        return ""

    soup = BeautifulSoup(resp.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = " ".join(soup.stripped_strings)
    return text[:max_chars]
