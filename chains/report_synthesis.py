import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from prompts.research_prompts import (
    sales_recommendation_prompt,
    account_brief_prompt,
)

from models.schemas import (
    SalesRecommendation,
    AccountBrief,
)

from research.web_research import (
    research_recent_articles,
    format_search_results,
)

load_dotenv(override=True)

model = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="openai/gpt-oss-20b",
    temperature=0,
)


def run_sales_recommendation(
    product_name: str,
    product_category: str,
    value_proposition: str,
    target_customer: str,
    company_name: str,
    company_analysis,
    competitor_analysis,
    leadership_analysis,
    annual_report_analysis,
):

    recent_articles = research_recent_articles(
        company_name
    )

    recent_developments = format_search_results(
        recent_articles
    )

    chain = sales_recommendation_prompt | model

    raw_response = chain.invoke(
        {
            "product_name": product_name,
            "product_category": product_category,
            "value_proposition": value_proposition,
            "target_customer": target_customer,
            "company_name": company_name,
            "company_analysis": company_analysis.model_dump_json(
                indent=2
            ),
            "competitor_analysis": competitor_analysis.model_dump_json(
                indent=2
            ),
            "leadership_analysis": leadership_analysis.model_dump_json(
                indent=2
            ),
            "annual_report_analysis": annual_report_analysis.model_dump_json(
                indent=2
            ),
            "recent_developments": recent_developments,
        }
    )

    recommendation = SalesRecommendation(
        recommended_cyber2safe_service=product_name,
        opportunity_summary=raw_response.content,
        why_it_fits=raw_response.content,
        recommended_sales_angle=raw_response.content,
        likely_buyer=(
            "Cybersecurity, IT, Risk, HR, or "
            "Learning and Development leadership"
        ),
        suggested_outreach_message=raw_response.content,
    )

    return recommendation, recent_articles


def run_account_brief(
    company_name: str,
    company_analysis,
    competitor_analysis,
    leadership_analysis,
    annual_report_analysis,
    sales_recommendation,
    recent_articles,
):

    recent_developments = format_search_results(
        recent_articles
    )

    chain = account_brief_prompt | model

    raw_response = chain.invoke(
        {
            "company_name": company_name,
            "company_analysis": company_analysis.model_dump_json(
                indent=2
            ),
            "competitor_analysis": competitor_analysis.model_dump_json(
                indent=2
            ),
            "leadership_analysis": leadership_analysis.model_dump_json(
                indent=2
            ),
            "annual_report_analysis": annual_report_analysis.model_dump_json(
                indent=2
            ),
            "recent_developments": recent_developments,
            "sales_recommendation": sales_recommendation.model_dump_json(
                indent=2
            ),
        }
    )

    all_links = []

    source_groups = [
        company_analysis.source_links,
        competitor_analysis.source_links,
        leadership_analysis.source_links,
        annual_report_analysis.source_links,
        [
            article.get("url")
            for article in recent_articles
            if article.get("url")
        ],
    ]

    for group in source_groups:
        for link in group:
            if link and link not in all_links:
                all_links.append(link)

    return AccountBrief(
        company_name=company_name,
        company_strategy=company_analysis.company_strategy,
        competitor_analysis=competitor_analysis.competitor_summary,
        leadership_summary=leadership_analysis.leadership_summary,
        annual_report_insights=" ".join(
            annual_report_analysis.cybersecurity_relevant_insights
        ),
        recent_developments=recent_developments,
        recommended_cyber2safe_service=(
            sales_recommendation.recommended_cyber2safe_service
        ),
        sales_opportunity=raw_response.content,
        recommended_sales_angle=(
            sales_recommendation.recommended_sales_angle
        ),
        suggested_outreach_message=(
            sales_recommendation.suggested_outreach_message
        ),
        source_links=all_links,
    )