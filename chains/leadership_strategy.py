import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from prompts.research_prompts import (
    leadership_prompt,
    annual_report_prompt,
)

from models.schemas import (
    LeadershipResearch,
    AnnualReportInsights,
)

from research.web_research import (
    research_leadership,
    research_annual_report,
    format_search_results,
)

load_dotenv(override=True)

model = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="groq/compound-mini",
    temperature=0,
)


def run_leadership_research(
    company_name: str,
) -> LeadershipResearch:

    leadership_results = research_leadership(
        company_name
    )

    chain = leadership_prompt | model

    raw_response = chain.invoke(
        {
            "company_name": company_name,
            "leadership_research": format_search_results(
                leadership_results
            ),
        }
    )

    source_links = [
        result.get("url")
        for result in leadership_results
        if result.get("url")
    ]

    return LeadershipResearch(
        key_leaders=[],
        leadership_summary=raw_response.content,
        likely_decision_makers=[],
        source_links=source_links,
    )


def run_annual_report_research(
    company_name: str,
) -> AnnualReportInsights:

    annual_report_results = research_annual_report(
        company_name
    )

    research_text = format_search_results(
        annual_report_results
    )

    source_links = [
        result.get("url")
        for result in annual_report_results
        if result.get("url")
    ]

    if not annual_report_results:
        return AnnualReportInsights(
            filing_type="No filing retrieved",
            key_risks=[],
            strategic_priorities=[],
            cybersecurity_relevant_insights=[],
            source_links=[],
        )

    chain = annual_report_prompt | model

    raw_response = chain.invoke(
        {
            "company_name": company_name,
            "annual_report_research": research_text,
        }
    )

    return AnnualReportInsights(
        filing_type="Annual Report / 10-K Research",
        key_risks=[],
        strategic_priorities=[],
        cybersecurity_relevant_insights=[
            raw_response.content
        ],
        source_links=source_links,
    )
