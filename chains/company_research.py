import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from prompts.research_prompts import company_research_prompt
from models.schemas import CompanyResearch
from research.web_research import (
    research_company,
    research_strategy,
    research_job_postings,
    format_search_results,
)


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv(override=True)


# ============================================================
# MODEL
# ============================================================

model = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="groq/compound-mini",
    temperature=0,
)


# ============================================================
# COMPANY RESEARCH WORKFLOW
# ============================================================

def run_company_research(
    company_name: str,
    company_url: str,
) -> CompanyResearch:
    """
    Research the prospect company using:

    1. The company's public website
    2. Public strategy research
    3. Public cybersecurity and technology job research

    Retrieved public evidence is then supplied to the
    company research LLM chain.
    """

    # --------------------------------------------------------
    # RETRIEVE COMPANY WEBSITE
    # --------------------------------------------------------

    company_data = research_company(
        company_url
    )

    # research_company() now returns cleaned website text
    # directly as a string.
    if company_data:
        website_text = company_data
    else:
        website_text = (
            "No website information retrieved."
        )

    # --------------------------------------------------------
    # STRATEGY RESEARCH
    # --------------------------------------------------------

    strategy_results = research_strategy(
        company_name
    )

    # --------------------------------------------------------
    # JOB / TECHNOLOGY RESEARCH
    # --------------------------------------------------------

    job_results = research_job_postings(
        company_name
    )

    # --------------------------------------------------------
    # FORMAT RETRIEVED EVIDENCE
    # --------------------------------------------------------

    strategy_research = format_search_results(
        strategy_results
    )

    job_research = format_search_results(
        job_results
    )

    # --------------------------------------------------------
    # RUN LLM RESEARCH CHAIN
    # --------------------------------------------------------

    chain = (
        company_research_prompt
        | model
    )

    raw_response = chain.invoke(
        {
            "company_name": company_name,
            "company_url": company_url,
            "website_text": website_text,
            "strategy_research": strategy_research,
            "job_research": job_research,
        }
    )

    # --------------------------------------------------------
    # COLLECT SOURCE LINKS
    # --------------------------------------------------------

    source_links = []

    if company_url:
        source_links.append(
            company_url
        )

    combined_results = (
        strategy_results
        + job_results
    )

    for result in combined_results:

        if not isinstance(
            result,
            dict,
        ):
            continue

        url = result.get(
            "url"
        )

        if (
            url
            and url not in source_links
        ):
            source_links.append(
                url
            )

    # --------------------------------------------------------
    # BUILD STRUCTURED RESULT
    # --------------------------------------------------------

    return CompanyResearch(
        company_name=company_name,
        company_url=company_url,
        company_strategy=raw_response.content,
        business_priorities=[],
        cybersecurity_signals=[],
        technology_signals=[],
        job_signals=[],
        source_links=source_links,
    )