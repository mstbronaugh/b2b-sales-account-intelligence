from agents.research_agent import run_research_workflow


def main():
    print("Cyber2Safe B2B Sales Intelligence")
    print("---------------------------------")

    results = run_research_workflow(
        product_name="Determine Best Cyber2Safe Service",
        company_name="Lantego",
        company_url="https://www.lantego.com",
        product_category="Cybersecurity Services",
        competitor_urls=[
            "https://cfisa.com",
            "https://secureabc.com",
        ],
        value_proposition=(
            "Cyber2Safe provides practical cybersecurity assessments "
            "and cybersecurity awareness training to help organizations "
            "identify security risks and strengthen employee awareness."
        ),
        target_customer=(
            "Small businesses, churches, nonprofits, and organizations "
            "that need practical cybersecurity assessments or employee "
            "cybersecurity awareness training."
        ),
    )

    brief = results["account_brief"]

    print("\nCompany:", brief.company_name)

    print("\nCompany Strategy:")
    print(brief.company_strategy)

    print("\nCompetitor Analysis:")
    print(brief.competitor_analysis)

    print("\nLeadership:")
    print(brief.leadership_summary)

    print("\nAnnual Report / 10-K Insights:")
    print(brief.annual_report_insights)

    print("\nRecommended Cyber2Safe Service:")
    print(brief.recommended_cyber2safe_service)

    print("\nSales Opportunity:")
    print(brief.sales_opportunity)

    print("\nRecommended Sales Angle:")
    print(brief.recommended_sales_angle)

    print("\nSuggested Outreach:")
    print(brief.suggested_outreach_message)

    print("\nVerified Public Sources:")
    for source in brief.source_links:
        print(source)


if __name__ == "__main__":
    main()
