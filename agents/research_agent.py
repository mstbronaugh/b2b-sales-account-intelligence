from chains.company_research import run_company_research
from chains.competitor_analysis import run_competitor_analysis
from chains.leadership_strategy import (
    run_leadership_research,
    run_annual_report_research,
)
from chains.report_synthesis import (
    run_sales_recommendation,
    run_account_brief,
)


def run_research_workflow(
    product_name: str,
    company_name: str,
    company_url: str,
    product_category: str,
    competitor_urls: list[str],
    value_proposition: str,
    target_customer: str,
):
    company_analysis = run_company_research(
        company_name=company_name,
        company_url=company_url,
    )

    competitor_analysis = run_competitor_analysis(
        company_name=company_name,
        competitor_urls=competitor_urls,
    )

    leadership_analysis = run_leadership_research(
        company_name=company_name,
    )

    annual_report_analysis = run_annual_report_research(
        company_name=company_name,
    )

    sales_recommendation, recent_articles = (
        run_sales_recommendation(
            product_name=product_name,
            product_category=product_category,
            value_proposition=value_proposition,
            target_customer=target_customer,
            company_name=company_name,
            company_analysis=company_analysis,
            competitor_analysis=competitor_analysis,
            leadership_analysis=leadership_analysis,
            annual_report_analysis=annual_report_analysis,
        )
    )

    account_brief = run_account_brief(
        company_name=company_name,
        company_analysis=company_analysis,
        competitor_analysis=competitor_analysis,
        leadership_analysis=leadership_analysis,
        annual_report_analysis=annual_report_analysis,
        sales_recommendation=sales_recommendation,
        recent_articles=recent_articles,
    )

    return {
        "company_analysis": company_analysis,
        "competitor_analysis": competitor_analysis,
        "leadership_analysis": leadership_analysis,
        "annual_report_analysis": annual_report_analysis,
        "sales_recommendation": sales_recommendation,
        "recent_articles": recent_articles,
        "account_brief": account_brief,
    }