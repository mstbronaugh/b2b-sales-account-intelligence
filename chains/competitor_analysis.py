import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from prompts.research_prompts import competitor_prompt
from models.schemas import CompetitorResearch
from research.web_research import research_competitors

load_dotenv(override=True)

model = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="openai/gpt-oss-20b",
    temperature=0,
)


def run_competitor_analysis(
    company_name: str,
    competitor_urls: list[str],
) -> CompetitorResearch:

    if not competitor_urls:
        return CompetitorResearch(
            competitors=[],
            competitor_summary="No competitor URLs were provided.",
            competitive_differences=[],
            source_links=[],
        )

    competitor_data = research_competitors(
        competitor_urls
    )

    formatted_research = []

    for competitor in competitor_data:
        formatted_research.append(
            f"""
Competitor URL:
{competitor.get("url", "")}

Public Website Information:
{competitor.get("website_text", "")}
"""
        )

    chain = competitor_prompt | model

    raw_response = chain.invoke(
        {
            "company_name": company_name,
            "competitor_research": "\n".join(
                formatted_research
            ),
        }
    )

    source_links = [
        competitor.get("url")
        for competitor in competitor_data
        if competitor.get("url")
    ]

    return CompetitorResearch(
        competitors=competitor_urls,
        competitor_summary=raw_response.content,
        competitive_differences=[],
        source_links=source_links,
    )