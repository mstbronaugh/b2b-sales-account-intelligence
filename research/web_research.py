import re
import socket
import ipaddress
from typing import List, Dict
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS


# ============================================================
# SETTINGS
# ============================================================

REQUEST_TIMEOUT = 15

# Keep retrieved pages small enough to avoid excessive
# LLM token usage.
MAX_PAGE_CHARACTERS = 4000

# Limit the number of search results collected.
MAX_RESULTS_PER_SEARCH = 3

# Only retrieve full content from the strongest few results.
MAX_FULL_PAGES_PER_SEARCH = 2

HEADERS = {
    "User-Agent": (
        "Cyber2Safe-B2B-Research/1.0 "
        "(educational cybersecurity sales research project)"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,"
        "application/xml;q=0.9,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


# ============================================================
# SSRF PROTECTION
# ============================================================

def is_safe_ip(ip_address: str) -> bool:
    """
    Allow only public IP addresses.
    """

    try:
        ip = ipaddress.ip_address(ip_address)

        if ip.is_private:
            return False

        if ip.is_loopback:
            return False

        if ip.is_link_local:
            return False

        if ip.is_reserved:
            return False

        if ip.is_multicast:
            return False

        if ip.is_unspecified:
            return False

        return True

    except ValueError:
        return False


def is_safe_hostname(hostname: str) -> bool:
    """
    Reject local or internal hostnames and verify that
    resolved IP addresses are public.
    """

    if not hostname:
        return False

    hostname = hostname.lower().strip()

    blocked_hostnames = {
        "localhost",
        "localhost.localdomain",
        "metadata",
        "metadata.google.internal",
    }

    if hostname in blocked_hostnames:
        return False

    if hostname.endswith(".local"):
        return False

    if hostname.endswith(".internal"):
        return False

    try:
        address_info = socket.getaddrinfo(
            hostname,
            None,
        )

        resolved_ips = {
            result[4][0]
            for result in address_info
        }

        if not resolved_ips:
            return False

        for resolved_ip in resolved_ips:
            if not is_safe_ip(resolved_ip):
                return False

        return True

    except socket.gaierror:
        return False

    except Exception:
        return False


def is_valid_public_url(url: str) -> bool:
    """
    Validate URLs before the application makes an
    outbound request.
    """

    if not url:
        return False

    try:
        parsed = urlparse(url)

        if parsed.scheme not in (
            "http",
            "https",
        ):
            return False

        if not parsed.hostname:
            return False

        # Reject URLs containing embedded credentials.
        if parsed.username or parsed.password:
            return False

        if not is_safe_hostname(
            parsed.hostname
        ):
            return False

        return True

    except Exception:
        return False


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text: str) -> str:
    """
    Remove unnecessary whitespace from webpage text.
    """

    if not text:
        return ""

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


# ============================================================
# FETCH WEBPAGE
# ============================================================

def fetch_page_content(url: str) -> str:
    """
    Retrieve readable public webpage content.

    Redirect destinations are validated before they
    are requested.

    Retrieved content is intentionally limited to reduce
    downstream LLM token usage.
    """

    if not is_valid_public_url(url):
        return ""

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=False,
        )

        redirect_count = 0

        while (
            response.is_redirect
            or response.is_permanent_redirect
        ):
            redirect_count += 1

            if redirect_count > 5:
                return ""

            redirect_url = response.headers.get(
                "Location"
            )

            if not redirect_url:
                return ""

            redirect_url = requests.compat.urljoin(
                response.url,
                redirect_url,
            )

            # Validate every redirect destination.
            if not is_valid_public_url(
                redirect_url
            ):
                return ""

            response = requests.get(
                redirect_url,
                headers=HEADERS,
                timeout=REQUEST_TIMEOUT,
                allow_redirects=False,
            )

        response.raise_for_status()

        content_type = response.headers.get(
            "Content-Type",
            "",
        ).lower()

        if (
            "text/html" not in content_type
            and "application/xhtml+xml"
            not in content_type
        ):
            return ""

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        # Remove content that normally provides little
        # useful research evidence.
        for element in soup(
            [
                "script",
                "style",
                "noscript",
                "svg",
                "form",
                "iframe",
            ]
        ):
            element.decompose()

        main_content = (
            soup.find("main")
            or soup.find("article")
            or soup.body
            or soup
        )

        text = main_content.get_text(
            separator=" ",
            strip=True,
        )

        text = clean_text(text)

        return text[:MAX_PAGE_CHARACTERS]

    except requests.RequestException:
        return ""

    except Exception:
        return ""


# ============================================================
# COMPANY WEBSITE
# ============================================================

def fetch_company_website(
    company_url: str,
) -> str:
    """
    Retrieve the prospect company's public website.
    """

    content = fetch_page_content(
        company_url
    )

    if content:
        return content

    return (
        "The company website could not be retrieved."
    )


# ============================================================
# DUCKDUCKGO SEARCH
# ============================================================

def search_web(
    query: str,
    max_results: int = MAX_RESULTS_PER_SEARCH,
) -> List[Dict]:
    """
    Search DuckDuckGo for relevant public sources.
    """

    results = []

    try:
        with DDGS() as ddgs:
            search_results = ddgs.text(
                query,
                max_results=max_results,
            )

            for item in search_results:
                title = item.get(
                    "title",
                    "",
                )

                url = (
                    item.get("href")
                    or item.get("url")
                    or ""
                )

                snippet = (
                    item.get("body")
                    or item.get("snippet")
                    or ""
                )

                if not url:
                    continue

                if not is_valid_public_url(
                    url
                ):
                    continue

                results.append(
                    {
                        "title": title,
                        "url": url,
                        "snippet": snippet,
                        "page_content": "",
                    }
                )

    except Exception:
        return []

    return results


# ============================================================
# OPEN SEARCH RESULTS
# ============================================================

def enrich_search_results(
    results: List[Dict],
    max_pages: int = MAX_FULL_PAGES_PER_SEARCH,
) -> List[Dict]:
    """
    Open selected search-result webpages and attach
    their actual page content.

    The number of full pages is intentionally limited
    to control token usage.
    """

    enriched_results = []

    pages_opened = 0

    for result in results:
        enriched = dict(result)

        url = enriched.get(
            "url",
            "",
        )

        if (
            url
            and pages_opened < max_pages
        ):
            page_content = fetch_page_content(
                url
            )

            enriched["page_content"] = (
                page_content
            )

            if page_content:
                pages_opened += 1

        enriched_results.append(
            enriched
        )

    return enriched_results


# ============================================================
# SEARCH AND RETRIEVE
# ============================================================

def search_and_retrieve(
    query: str,
    max_results: int = MAX_RESULTS_PER_SEARCH,
    max_pages: int = MAX_FULL_PAGES_PER_SEARCH,
) -> List[Dict]:
    """
    Search for public sources and retrieve selected
    full webpages.
    """

    results = search_web(
        query=query,
        max_results=max_results,
    )

    return enrich_search_results(
        results,
        max_pages=max_pages,
    )


# ============================================================
# FORMAT RESULTS FOR LLM
# ============================================================

def format_search_results(
    results: List[Dict],
) -> str:
    """
    Format retrieved evidence for downstream LLM analysis.

    Full source content is preferred over search snippets.
    Search snippets are retained as fallback evidence.
    """

    if not results:
        return (
            "No public search results were retrieved."
        )

    formatted = []

    for number, result in enumerate(
        results,
        start=1,
    ):
        if not isinstance(result, dict):
            continue

        title = result.get(
            "title",
            "",
        )

        url = result.get(
            "url",
            "",
        )

        snippet = result.get(
            "snippet",
            "",
        )

        page_content = result.get(
            "page_content",
            "",
        )

        if page_content:
            evidence = (
                "FULL SOURCE PAGE CONTENT:\n"
                f"{page_content}"
            )

        elif snippet:
            evidence = (
                "SEARCH RESULT SNIPPET ONLY:\n"
                f"{snippet}"
            )

        else:
            evidence = (
                "No readable source content "
                "was retrieved."
            )

        formatted.append(
            f"""
SOURCE {number}

Title:
{title}

URL:
{url}

Evidence:
{evidence}
""".strip()
        )

    if not formatted:
        return (
            "No usable public research evidence "
            "was retrieved."
        )

    return "\n\n".join(
        formatted
    )


# ============================================================
# COMPANY STRATEGY
# ============================================================

def research_company_strategy(
    company_name: str,
) -> List[Dict]:
    """
    Research strategy, priorities, growth,
    technology, and cybersecurity.
    """

    query = (
        f'"{company_name}" '
        "company strategy business priorities "
        "growth technology cybersecurity"
    )

    return search_and_retrieve(
        query
    )


# ============================================================
# JOB POSTINGS
# ============================================================

def research_job_postings(
    company_name: str,
) -> List[Dict]:
    """
    Research cybersecurity and technology job postings.
    """

    query = (
        f'"{company_name}" jobs careers '
        "cybersecurity security information technology "
        "risk compliance"
    )

    return search_and_retrieve(
        query
    )


# ============================================================
# LEADERSHIP
# ============================================================

def research_leadership(
    company_name: str,
) -> List[Dict]:
    """
    Research publicly available company leadership.
    """

    query = (
        f'"{company_name}" leadership '
        "CEO CIO CTO CISO cybersecurity "
        "information technology HR training"
    )

    return search_and_retrieve(
        query
    )


# ============================================================
# ANNUAL REPORT / 10-K
# ============================================================

def research_annual_report(
    company_name: str,
) -> List[Dict]:
    """
    Research annual reports, 10-K filings,
    cybersecurity risks, and technology priorities.
    """

    query = (
        f'"{company_name}" '
        '"annual report" OR "10-K" '
        "cybersecurity risk technology"
    )

    return search_and_retrieve(
        query
    )


# ============================================================
# RECENT DEVELOPMENTS
# ============================================================

def research_recent_articles(
    company_name: str,
) -> List[Dict]:
    """
    Research recent public company developments.
    """

    query = (
        f'"{company_name}" '
        "news cybersecurity technology "
        "growth partnership expansion"
    )

    return search_and_retrieve(
        query
    )


# ============================================================
# COMPETITOR RESEARCH
# ============================================================

def research_competitor_url(
    competitor_url: str,
) -> Dict:
    """
    Retrieve a competitor website supplied by the user.
    """

    if not is_valid_public_url(
        competitor_url
    ):
        return {
            "title": competitor_url,
            "url": competitor_url,
            "snippet": "",
            "page_content": "",
        }

    page_content = fetch_page_content(
        competitor_url
    )

    return {
        "title": competitor_url,
        "url": competitor_url,
        "snippet": "",
        "page_content": page_content,
    }


def research_competitors(
    competitor_urls: List[str],
) -> List[Dict]:
    """
    Retrieve public content for multiple competitors.
    """

    results = []

    for competitor_url in competitor_urls:
        competitor_url = (
            competitor_url.strip()
        )

        if not competitor_url:
            continue

        if not is_valid_public_url(
            competitor_url
        ):
            continue

        result = research_competitor_url(
            competitor_url
        )

        results.append(
            result
        )

    return results


# ============================================================
# COMPATIBILITY FUNCTIONS
# ============================================================
# These preserve the function names used by the original
# Cyber2Safe research chains.


def research_company(
    company_url: str,
) -> str:
    """
    Original function name used by the company chain.
    """

    return fetch_company_website(
        company_url
    )


def research_strategy(
    company_name: str,
):
    """
    Original function name used for strategy research.
    """

    return research_company_strategy(
        company_name
    )


def research_jobs(
    company_name: str,
):
    """
    Original function name used for job research.
    """

    return research_job_postings(
        company_name
    )


def research_leaders(
    company_name: str,
):
    """
    Original function name used for leadership research.
    """

    return research_leadership(
        company_name
    )


def research_annual_reports(
    company_name: str,
):
    """
    Original function name used for annual-report research.
    """

    return research_annual_report(
        company_name
    )


def research_recent_news(
    company_name: str,
):
    """
    Original function name used for recent-development research.
    """

    return research_recent_articles(
        company_name
    )