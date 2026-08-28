from pydantic import BaseModel, Field
from typing import List, Optional


class SalesIntake(BaseModel):
    product_name: str = Field(
        description="Name of the product or service being sold"
    )

    company_url: str = Field(
        description="Website URL of the prospective company"
    )

    product_category: str = Field(
        description="Category of the product or service"
    )

    competitor_urls: List[str] = Field(
        default_factory=list,
        description="URLs for known competitors"
    )

    value_proposition: str = Field(
        description="Core value proposition of the product or service"
    )

    target_customer: str = Field(
        description="Description of the ideal target customer"
    )


class CompanyResearch(BaseModel):
    company_name: str
    company_strategy: str
    business_priorities: List[str]
    cybersecurity_signals: List[str]
    relevant_job_posting_signals: List[str]
    source_links: List[str]


class CompetitorResearch(BaseModel):
    competitors: List[str]
    competitor_summary: str
    competitive_differences: List[str]
    source_links: List[str]


class LeadershipResearch(BaseModel):
    key_leaders: List[str]
    leadership_summary: str
    likely_decision_makers: List[str]
    source_links: List[str]


class AnnualReportInsights(BaseModel):
    filing_type: str
    key_risks: List[str]
    strategic_priorities: List[str]
    cybersecurity_relevant_insights: List[str]
    source_links: List[str]


class ArticleResearch(BaseModel):
    recent_articles: List[str]
    key_recent_developments: List[str]
    source_links: List[str]


class SalesRecommendation(BaseModel):
    recommended_cyber2safe_service: str = Field(
        description="Recommend either Cyber2Safe Assessment or Cyber2Safe Training"
    )

    opportunity_summary: str
    why_it_fits: str
    recommended_sales_angle: str
    likely_buyer: str
    suggested_outreach_message: str


class AccountBrief(BaseModel):
    company_name: str
    company_strategy: str
    competitor_analysis: str
    leadership_summary: str
    annual_report_insights: str
    recent_developments: str
    recommended_cyber2safe_service: str
    sales_opportunity: str
    recommended_sales_angle: str
    suggested_outreach_message: str
    source_links: List[str]
    
