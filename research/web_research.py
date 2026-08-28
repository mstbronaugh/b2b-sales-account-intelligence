import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, unquote

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
    )
}

TIMEOUT = 12


def clean_text(text: str) -> str:
    """
    Remove excessive spaces and blank lines from scraped text.
    """
    return " ".join(text.split())


def fetch_page_text(url: str, max_chars: int = 12000) -> str:
    """
    Download a public webpage and return readable text.

    Returns an empty string if the page cannot be retrieved.
    """
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT,
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(
            [
                "script",
                "style",
                "nav",
                "footer",
                "noscript",
                "svg",
            ]
        ):
            tag.decompose()

        text = clean_text(soup.get_text(" "))

        return text[:max_chars]

    except requests.RequestException:
        return ""


def clean_search_url(url: str) -> str:
    """
    Convert DuckDuckGo redirect URLs into normal destination URLs.
    """
    try:
        parsed = urlparse(url)

        if "duckduckgo.com" in parsed.netloc:
            query = parse_qs(parsed.query)

            if "uddg" in query:
                return unquote(query["uddg"][0])

        return url

    except Exception:
        return url


def search_web(query: str, max_results: int = 5) -> list[dict]:
    """
    Search the public web using DuckDuckGo's HTML results.

    Returns:
    [
        {
            "title": "...",
            "url": "...",
            "snippet": "..."
        }
    ]
    """
    search_url = "https://html.duckduckgo.com/html/"

    try:
        response = requests.get(
            search_url,
            params={"q": query},
            headers=HEADERS,
            timeout=TIMEOUT,
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        results = []

        for result in soup.select(".result"):
            link = result.select_one(".result__a")

            if not link:
                continue

            title = clean_text(link.get_text(" ", strip=True))
            url = clean_search_url(link.get("href", ""))

            snippet_element = result.select_one(".result__snippet")

            snippet = (
                clean_text(
                    snippet_element.get_text(" ", strip=True)
                )
                if snippet_element
                else ""
            )

            if url.startswith("http"):
                results.append(
                    {
                        "title": title,
                        "url": url,
                        "snippet": snippet,
                    }
                )

            if len(results) >= max_results:
                break

        return results

    except requests.RequestException:
        return []


def research_company(company_url: str) -> dict:
    """
    Retrieve the company's public website text.
    """
    website_text = fetch_page_text(company_url)

    return {
        "company_url": company_url,
        "website_text": website_text,
    }


def research_leadership(company_name: str) -> list[dict]:
    """
    Search for executives and leadership information.
    """
    queries = [
        f"{company_name} leadership executive team",
        f"{company_name} CEO CIO CISO leadership",
    ]

    results = []

    for query in queries:
        results.extend(search_web(query, max_results=4))

    return remove_duplicate_results(results)


def research_strategy(company_name: str) -> list[dict]:
    """
    Search for company strategy, priorities, expansion,
    digital initiatives, and business developments.
    """
    queries = [
        f"{company_name} company strategy priorities",
        f"{company_name} digital transformation strategy",
        f"{company_name} growth priorities press release",
    ]

    results = []

    for query in queries:
        results.extend(search_web(query, max_results=4))

    return remove_duplicate_results(results)


def research_competitors(
    competitor_urls: list[str],
) -> list[dict]:
    """
    Retrieve public information from competitor websites.
    """
    competitors = []

    for url in competitor_urls:
        text = fetch_page_text(url, max_chars=7000)

        competitors.append(
            {
                "url": url,
                "website_text": text,
            }
        )

    return competitors


def research_annual_report(company_name: str) -> list[dict]:
    """
    Search for annual reports, investor reports, and SEC 10-K filings.
    """
    queries = [
        f"{company_name} annual report",
        f"{company_name} 10-K site:sec.gov",
        f"{company_name} investor relations annual report",
    ]

    results = []

    for query in queries:
        results.extend(search_web(query, max_results=4))

    return remove_duplicate_results(results)


def research_recent_articles(company_name: str) -> list[dict]:
    """
    Search for recent public articles and company developments.
    """
    queries = [
        f"{company_name} latest news",
        f"{company_name} cybersecurity news",
        f"{company_name} expansion technology news",
    ]

    results = []

    for query in queries:
        results.extend(search_web(query, max_results=5))

    return remove_duplicate_results(results)


def research_job_postings(company_name: str) -> list[dict]:
    """
    Search public job postings for signals about technology,
    cybersecurity, growth, and operational priorities.
    """
    queries = [
        f"{company_name} cybersecurity jobs",
        f"{company_name} information security jobs",
        f"{company_name} technology jobs",
    ]

    results = []

    for query in queries:
        results.extend(search_web(query, max_results=4))

    return remove_duplicate_results(results)


def remove_duplicate_results(
    results: list[dict],
) -> list[dict]:
    """
    Remove duplicate web results based on URL.
    """
    unique_results = []
    seen_urls = set()

    for result in results:
        url = result.get("url")

        if not url or url in seen_urls:
            continue

        seen_urls.add(url)
        unique_results.append(result)

    return unique_results


def format_search_results(
    results: list[dict],
    max_items: int = 8,
) -> str:
    """
    Convert search results into text that can be passed
    safely into the language model.
    """
    if not results:
        return "No public search results were retrieved."

    sections = []

    for result in results[:max_items]:
        sections.append(
            f"""
Title: {result.get("title", "")}
URL: {result.get("url", "")}
Public Search Snippet: {result.get("snippet", "")}
"""
        )

    return "\n".join(sections)


def collect_source_links(
    *result_groups: list[dict],
) -> list[str]:
    """
    Collect unique source URLs for the final account brief.
    """
    links = []
    seen = set()

    for group in result_groups:
        for item in group:
            url = item.get("url")

            if url and url not in seen:
                seen.add(url)
                links.append(url)

    return links