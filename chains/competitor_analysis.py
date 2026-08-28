import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from prompts.research_prompts import competitor_prompt
from models.schemas import CompetitorResearch
from research.web_research import research_competitors

load_dotenv(override=True)

model = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="groq/compound-mini",
    temperature=0,
)


def run_competitor_analysis(
    company_name: str,
    company_analysis,
    competitor_urls: list[str],
) -> CompetitorResearch:

    if not competitor_urls:
        return CompetitorResearch(
            competitors=[],
            competitor_summary=(
                "No competitor was provided for comparison."
            ),
            competitive_differences=[],
            source_links=[],
        )

    competitor_data = research_competitors(
        competitor_urls
    )

    competitor_sections = []

    for index, competitor in enumerate(
        competitor_data,
        start=1,
    ):
        url = competitor.get("url", "")
        website_text = competitor.get(
            "website_text",
            "",
        ).strip()

        if not website_text:
            website_text = (
                "Not found in retrieved public information."
            )

        competitor_sections.append(
            f"""
COMPETITOR {index}

URL:
{url}

RETRIEVED PUBLIC INFORMATION:
{website_text}
"""
        )

    prospect_research = (
        company_analysis.model_dump_json(
            indent=2
        )
    )

    chain = competitor_prompt | model

    raw_response = chain.invoke(
        {
            "company_name": company_name,
            "company_research": prospect_research,
            "competitor_research": "\n".join(
                competitor_sections
            ),
        }
    )

    comparison_text = raw_response.content.strip()

    if not comparison_text:
        comparison_text = (
            "No verified competitor comparison was available "
            "from the retrieved public information."
        )

    source_links = []

    for competitor in competitor_data:
        url = competitor.get("url")

        if url and url not in source_links:
            source_links.append(url)

    return CompetitorResearch(
        competitors=competitor_urls,
        competitor_summary=comparison_text,
        competitive_differences=[],
        source_links=source_links,
    )
