import sys
from pathlib import Path

# Make the project root available to the test file.
ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from models.schemas import (
    CompanyResearch,
    CompetitorResearch,
    LeadershipResearch,
    AnnualReportResearch,
    SalesRecommendation,
    AccountBrief,
)


# ============================================================
# COMPANY RESEARCH SCHEMA TEST
# ============================================================

def test_company_research_schema():

    company = CompanyResearch(
        company_name="Test Company",
        company_url="https://example.com",
        company_strategy="Test strategy",
        business_priorities=["Priority 1"],
        cybersecurity_signals=["Security signal"],
        technology_signals=["Technology signal"],
        job_signals=["Job signal"],
        source_links=["https://example.com"],
    )

    assert company.company_name == "Test Company"
    assert company.company_url == "https://example.com"
    assert len(company.business_priorities) == 1
    assert len(company.cybersecurity_signals) == 1
    assert len(company.technology_signals) == 1
    assert len(company.job_signals) == 1
    assert len(company.source_links) == 1


# ============================================================
# COMPETITOR RESEARCH SCHEMA TEST
# ============================================================

def test_competitor_research_schema():

    competitor = CompetitorResearch(
        competitors=["https://cfisa.com"],
        competitor_summary="Verified competitor comparison.",
        competitive_differences=[
            "Verified difference"
        ],
        source_links=["https://cfisa.com"],
    )

    assert len(competitor.competitors) == 1

    assert (
        competitor.competitors[0]
        == "https://cfisa.com"
    )

    assert competitor.competitor_summary != ""

    assert (
        len(
            competitor.competitive_differences
        )
        == 1
    )

    assert len(competitor.source_links) == 1


# ============================================================
# LEADERSHIP RESEARCH SCHEMA TEST
# ============================================================

def test_leadership_research_schema():

    leadership = LeadershipResearch(
        leadership_summary="Leadership information",
        key_leaders=["Security Leader"],
        source_links=[
            "https://example.com/leadership"
        ],
    )

    assert leadership.leadership_summary != ""

    assert len(leadership.key_leaders) == 1

    assert len(leadership.source_links) == 1


# ============================================================
# ANNUAL REPORT SCHEMA TEST
# ============================================================

def test_annual_report_schema():

    report = AnnualReportResearch(
        annual_report_summary=(
            "Annual report summary"
        ),
        cybersecurity_relevant_insights=[
            "Cybersecurity risk disclosed"
        ],
        source_links=[
            "https://example.com/report"
        ],
    )

    assert report.annual_report_summary != ""

    assert (
        len(
            report.cybersecurity_relevant_insights
        )
        == 1
    )

    assert len(report.source_links) == 1


# ============================================================
# STRUCTURED SALES RECOMMENDATION TEST
# ============================================================

def test_sales_recommendation_schema():

    recommendation = SalesRecommendation(
        recommended_cyber2safe_service=(
            "Cyber2Safe Cybersecurity Awareness Training"
        ),
        opportunity_summary=(
            "Verified public information supports "
            "a training discussion."
        ),
        why_it_fits=[
            (
                "The organization publicly discusses "
                "cybersecurity training."
            )
        ],
        likely_buyer=(
            "Cybersecurity or Training Leader"
        ),
        recommended_sales_angle=(
            "Discuss Cyber2Safe awareness training "
            "as a complementary educational service."
        ),
        suggested_outreach_message=(
            "Hello, I would like to discuss "
            "Cyber2Safe cybersecurity awareness training."
        ),
    )

    assert (
        recommendation.recommended_cyber2safe_service
        == "Cyber2Safe Cybersecurity Awareness Training"
    )

    assert recommendation.opportunity_summary != ""

    assert len(recommendation.why_it_fits) == 1

    assert recommendation.likely_buyer != ""

    assert (
        recommendation.recommended_sales_angle
        != ""
    )

    assert (
        recommendation.suggested_outreach_message
        != ""
    )


# ============================================================
# AI RECOMMENDATION IS PRESERVED TEST
# ============================================================

def test_recommendation_preserves_ai_selected_service():

    product_input = (
        "Determine Best Cyber2Safe Service"
    )

    recommendation = SalesRecommendation(
        recommended_cyber2safe_service=(
            "Cyber2Safe Cybersecurity Assessment"
        ),
        opportunity_summary=(
            "Assessment opportunity"
        ),
        why_it_fits=[
            "Verified evidence"
        ],
        likely_buyer=(
            "Cybersecurity Leader"
        ),
        recommended_sales_angle=(
            "Assessment discussion"
        ),
        suggested_outreach_message=(
            "Hello"
        ),
    )

    # This proves the recommendation is not simply
    # copied from the user's product selection.

    assert (
        recommendation.recommended_cyber2safe_service
        != product_input
    )

    assert (
        recommendation.recommended_cyber2safe_service
        == "Cyber2Safe Cybersecurity Assessment"
    )


# ============================================================
# ACCOUNT BRIEF SCHEMA TEST
# ============================================================

def test_account_brief_schema():

    brief = AccountBrief(
        company_name="Test Company",
        company_strategy="Test strategy",
        competitor_analysis=(
            "Competitor analysis"
        ),
        leadership_summary=(
            "Leadership summary"
        ),
        annual_report_insights=(
            "Annual report insights"
        ),
        recent_developments=(
            "Recent developments"
        ),
        recommended_cyber2safe_service=(
            "Cyber2Safe Cybersecurity Assessment"
        ),
        sales_opportunity=(
            "Verified sales opportunity"
        ),
        recommended_sales_angle=(
            "Consultative sales angle"
        ),
        suggested_outreach_message=(
            "Professional outreach"
        ),
        source_links=[
            "https://example.com",
            "https://cfisa.com",
        ],
    )

    assert brief.company_name == "Test Company"

    assert (
        brief.recommended_cyber2safe_service
        == "Cyber2Safe Cybersecurity Assessment"
    )

    assert brief.sales_opportunity != ""

    assert (
        brief.recommended_sales_angle
        != ""
    )

    assert len(brief.source_links) == 2


# ============================================================
# DEFAULT EMPTY LIST TEST
# ============================================================

def test_schema_default_lists_are_empty():

    company = CompanyResearch()

    assert company.business_priorities == []

    assert company.cybersecurity_signals == []

    assert company.technology_signals == []

    assert company.job_signals == []

    assert company.source_links == []


# ============================================================
# MISSING COMPETITOR TEST
# ============================================================

def test_competitor_can_be_empty():

    competitor = CompetitorResearch(
        competitor_summary=(
            "No competitor was provided "
            "for comparison."
        )
    )

    assert competitor.competitors == []

    assert (
        competitor.competitive_differences
        == []
    )

    assert competitor.source_links == []