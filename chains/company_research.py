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

load_dotenv(override=True)

model = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="groq/compound-mini",
    temperature=0,
)


def run_company_research(
    company_name: str,
    company_url: str,
) -> CompanyResearch:

    company_data = research_company(company_url)
    strategy_results = research_strategy(company_name)
    job_results = research_job_postings(company_name)

    chain = company_research_prompt | model

    raw_response = chain.invoke(
        {
            "company_name": company_name,
            "company_url": company_url,
            "website_text": company_data.get(
                "website_text",
                "No website information retrieved.",
            ),
            "strategy_research": format_search_results(
                strategy_results
            ),
            "job_research": format_search_results(
                job_results
            ),
        }
    )

    source_links = [company_url]

    for result in strategy_results + job_results:
        url = result.get("url")

        if url and url not in source_links:
            source_links.append(url)

    return CompanyResearch(
        company_name=company_name,
        company_strategy=raw_response.content,
        business_priorities=[],
        cybersecurity_signals=[],
        relevant_job_posting_signals=[],
        source_links=source_links,
    )
