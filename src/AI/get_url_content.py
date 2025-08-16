import re
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from urllib3.poolmanager import PoolManager

def fetch_html(url: str, max_retries: int = 3, timeout: int = 20):
    """
    Fetch HTML content of a given URL with retry mechanism.
    Returns BeautifulSoup object or None on failure.
    """
    print(f"[INFO] Fetching: {url}")
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }

    session = requests.Session()
    retry = Retry(
        total=max_retries,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=("HEAD", "GET"),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    try:
        resp = session.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")
    except requests.RequestException as e:
        print(f"[ERROR] Request failed: {e}")
        return None


def extract_text(url: str) -> str | None:
    """
    Extract human-readable text from the main content area of a webpage.
    Returns plain text or None on failure.
    """
    soup = fetch_html(url)
    if soup is None:
        return None
    main = soup.find("main") or soup.find("article") or soup.body
    return main.get_text(separator="\n", strip=True) if main else ""


def crawl_ollama_servers(base_url: str = "https://freeollama.oneplus1.top/?page=",
                         page_size: int = 100):
    """
    Crawl all pages of the given base_url and collect Ollama server addresses
    along with their deployed models.
    Returns a dict: {"list": [...]}
    """
    page = 1
    results = []

    while True:
        url = f"{base_url}{page}&page_size={page_size}"
        content = extract_text(url)
        if not content:
            print(f"[WARN] No content on page {page}; stopping.")
            break

        # Regex to capture server address and models
        pattern = re.compile(
            r"服务器地址\s+复制\s+(\d+(?:\.\d+){3}:\d+)\s+已部署模型([\s\S]*?)(?=检查服务)",
            re.MULTILINE,
        )
        matches = pattern.findall(content)
        if not matches:
            print(f"[INFO] No more data found on page {page}; stopping.")
            break

        for addr, models_blob in matches:
            models = [
                {"model": m.strip()}
                for m in models_blob.strip().splitlines()
                if m.strip()
            ]
            results.append({
                "OllamaUrl": {"url": addr},
                "OllamaModels": models,
            })

        page += 1

    return {"list": results}


if __name__ == "__main__":
    data = crawl_ollama_servers()
    print(data)