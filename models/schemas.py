from typing import List
from pydantic import BaseModel, Field


# ============================================================
# COMPANY RESEARCH
# ============================================================

class CompanyResearch(BaseModel):
    company_name: str = ""
    company_url: str = ""

    company_strategy: str = ""

    business_priorities: List[str] = Field(
        default_factory=list
    )

    cybersecurity_signals: List[str] = Field(
        default_factory=list
    )

    technology_signals: List[str] = Field(
        default_factory=list
    )

    job_signals: List[str] = Field(
        default_factory=list
    )

    source_links: List[str] = Field(
        default_factory=list
    )


# ============================================================
# COMPETITOR RESEARCH
# ============================================================

class CompetitorResearch(BaseModel):
    competitors: List[str] = Field(
        default_factory=list
    )

    competitor_summary: str = ""

    competitive_differences: List[str] = Field(
        default_factory=list
    )

    source_links: List[str] = Field(
        default_factory=list
    )


# ============================================================
# LEADERSHIP RESEARCH
# ============================================================

class LeadershipResearch(BaseModel):
    leadership_summary: str = ""

    key_leaders: List[str] = Field(
        default_factory=list
    )

    source_links: List[str] = Field(
        default_factory=list
    )


# ============================================================
# ANNUAL REPORT RESEARCH
# ============================================================

class AnnualReportResearch(BaseModel):
    annual_report_summary: str = ""

    cybersecurity_relevant_insights: List[str] = Field(
        default_factory=list
    )

    source_links: List[str] = Field(
        default_factory=list
    )


# ============================================================
# ANNUAL REPORT INSIGHTS
# ============================================================
# Compatibility schema used by leadership_strategy.py.
# This keeps the existing AnnualReportResearch model while
# supporting the AnnualReportInsights name expected elsewhere
# in the application.

class AnnualReportInsights(BaseModel):
    annual_report_summary: str = ""

    cybersecurity_relevant_insights: List[str] = Field(
        default_factory=list
    )

    source_links: List[str] = Field(
        default_factory=list
    )


# ============================================================
# SALES RECOMMENDATION
# ============================================================

class SalesRecommendation(BaseModel):

    recommended_cyber2safe_service: str = Field(
        description=(
            "The Cyber2Safe service recommended by the AI. "
            "Must be Cyber2Safe Cybersecurity Assessment, "
            "Cyber2Safe Cybersecurity Awareness Training, "
            "or Insufficient Public Evidence for a Specific Recommendation."
        )
    )

    opportunity_summary: str = Field(
        description=(
            "A concise explanation of the verified sales opportunity."
        )
    )

    why_it_fits: List[str] = Field(
        default_factory=list,
        description=(
            "Verified evidence explaining why the recommended "
            "Cyber2Safe service is relevant."
        ),
    )

    likely_buyer: str = Field(
        default="",
        description=(
            "A verified or appropriately generic potential buyer. "
            "Do not invent an executive."
        ),
    )

    recommended_sales_angle: str = Field(
        description=(
            "A concise consultative sales angle based on "
            "verified public information."
        )
    )

    suggested_outreach_message: str = Field(
        description=(
            "A short professional outreach message based on "
            "verified public information."
        )
    )


# ============================================================
# FINAL ACCOUNT BRIEF
# ============================================================

class AccountBrief(BaseModel):
    company_name: str = ""

    company_strategy: str = ""

    competitor_analysis: str = ""

    leadership_summary: str = ""

    annual_report_insights: str = ""

    recent_developments: str = ""

    recommended_cyber2safe_service: str = ""

    sales_opportunity: str = ""

    recommended_sales_angle: str = ""

    suggested_outreach_message: str = ""

    source_links: List[str] = Field(
        default_factory=list
    )