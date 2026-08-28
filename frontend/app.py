import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from agents.research_agent import run_research_workflow


def clean_output(text):
    """Clean formatting returned by the AI before displaying it."""
    if not text:
        return ""

    return (
        str(text)
        .replace("<br>", "\n\n")
        .replace("<br/>", "\n\n")
        .replace("<br />", "\n\n")
    )


st.set_page_config(
    page_title="Cyber2Safe B2B Sales Intelligence",
    page_icon="🔎",
    layout="wide",
)


st.title("Cyber2Safe B2B Sales Intelligence")

st.write(
    "Research prospective companies and identify opportunities "
    "for Cyber2Safe cybersecurity assessments and awareness training."
)


with st.form("sales_research_form"):

    st.subheader("Prospect Information")

    company_name = st.text_input(
        "Prospective Company Name *",
        placeholder="Enter the company you want to research",
    )

    company_url = st.text_input(
        "Company URL *",
        placeholder="https://www.company.com",
    )

    st.subheader("Cyber2Safe Offering")

    product_name = st.selectbox(
        "Product Name *",
        [
            "Determine Best Cyber2Safe Service",
            "Cyber2Safe Cybersecurity Assessment",
            "Cyber2Safe Cybersecurity Awareness Training",
        ],
    )

    product_category = st.selectbox(
        "Product Category *",
        [
            "Cybersecurity Services",
            "Cybersecurity Assessment",
            "Cybersecurity Awareness Training",
        ],
    )

    value_proposition = st.text_area(
        "Value Proposition *",
        value=(
            "Cyber2Safe helps organizations identify cybersecurity "
            "risk through practical assessments and helps employees "
            "reduce human-centered cyber risk through cybersecurity "
            "awareness training."
        ),
    )

    target_customer = st.text_area(
        "Target Customer *",
        value=(
            "Small businesses, churches, nonprofits, and organizations "
            "that need practical cybersecurity assessments or employee "
            "cybersecurity awareness training."
        ),
    )

    competitor_input = st.text_area(
        "Competitor URLs",
        placeholder=(
            "Optional: Enter one competitor URL per line.\n"
            "https://www.competitor1.com\n"
            "https://www.competitor2.com"
        ),
    )

    product_documents = st.file_uploader(
        "Optional Product Documents",
        accept_multiple_files=True,
        type=["pdf", "txt", "docx"],
    )

    submitted = st.form_submit_button(
        "Generate Account Intelligence"
    )


if submitted:

    if not company_name.strip():

        st.error(
            "Please enter the prospective company name."
        )

    elif not company_url.strip():

        st.error(
            "Please enter the company URL."
        )

    else:

        competitor_urls = [
            url.strip()
            for url in competitor_input.splitlines()
            if url.strip()
        ]

        with st.spinner(
            "Researching the company, leadership, competitors, "
            "annual reports, recent developments, and "
            "Cyber2Safe sales opportunity..."
        ):

            try:

                results = run_research_workflow(
                    product_name=product_name,
                    company_name=company_name,
                    company_url=company_url,
                    product_category=product_category,
                    competitor_urls=competitor_urls,
                    value_proposition=value_proposition,
                    target_customer=target_customer,
                )

                brief = results["account_brief"]
                sales = results["sales_recommendation"]

                st.success(
                    "Account intelligence research complete."
                )

                st.header("One-Page Account Brief")

                st.subheader(brief.company_name)

                st.markdown("### Company Strategy")

                st.markdown(
                    clean_output(
                        brief.company_strategy
                    )
                )

                st.markdown("### Competitor Analysis")

                if competitor_urls:

                    st.markdown(
                        clean_output(
                            brief.competitor_analysis
                        )
                    )

                else:

                    st.info(
                        "No competitor URLs were provided "
                        "for this research."
                    )

                st.markdown("### Leadership")

                if brief.leadership_summary.strip():

                    st.markdown(
                        clean_output(
                            brief.leadership_summary
                        )
                    )

                else:

                    st.info(
                        "No public leadership information "
                        "was retrieved."
                    )

                st.markdown(
                    "### Annual Report / 10-K Insights"
                )

                if brief.annual_report_insights.strip():

                    st.markdown(
                        clean_output(
                            brief.annual_report_insights
                        )
                    )

                else:

                    st.info(
                        "No public annual report or 10-K "
                        "filing was retrieved. This may occur "
                        "when researching a privately held company."
                    )

                st.markdown("### Recent Developments")

                if (
                    brief.recent_developments.strip()
                    and "No public search results"
                    not in brief.recent_developments
                ):

                    st.markdown(
                        clean_output(
                            brief.recent_developments
                        )
                    )

                else:

                    st.info(
                        "No recent public developments "
                        "were retrieved."
                    )

                st.markdown("---")

                st.header("Cyber2Safe Opportunity")

                st.write(
                    "**Recommended Service:** "
                    f"{brief.recommended_cyber2safe_service}"
                )

                st.markdown("### Sales Opportunity")

                st.markdown(
                    clean_output(
                        brief.sales_opportunity
                    )
                )

                st.markdown(
                    "### Recommended Sales Angle"
                )

                st.markdown(
                    clean_output(
                        brief.recommended_sales_angle
                    )
                )

                st.markdown("### Suggested Outreach")

                st.markdown(
                    clean_output(
                        brief.suggested_outreach_message
                    )
                )

                st.markdown("---")

                st.header("Verified Public Sources")

                if brief.source_links:

                    for source in brief.source_links:

                        st.markdown(
                            f"- [{source}]({source})"
                        )

                else:

                    st.info(
                        "No public source links were retrieved."
                    )

                st.markdown("---")

                with st.expander(
                    "Detailed Sales Recommendation"
                ):

                    st.write(
                        "**Recommended Service:** "
                        f"{sales.recommended_cyber2safe_service}"
                    )

                    st.markdown("**Why It Fits**")

                    st.markdown(
                        clean_output(
                            sales.why_it_fits
                        )
                    )

                    st.write(
                        "**Likely Buyer:** "
                        f"{sales.likely_buyer}"
                    )

                    st.markdown(
                        "**Recommended Sales Angle**"
                    )

                    st.markdown(
                        clean_output(
                            sales.recommended_sales_angle
                        )
                    )

                with st.expander(
                    "Company Research"
                ):

                    st.json(
                        results[
                            "company_analysis"
                        ].model_dump()
                    )

                with st.expander(
                    "Competitor Research"
                ):

                    if competitor_urls:

                        st.json(
                            results[
                                "competitor_analysis"
                            ].model_dump()
                        )

                    else:

                        st.write(
                            "No competitor URLs were provided."
                        )

                with st.expander(
                    "Leadership Research"
                ):

                    st.json(
                        results[
                            "leadership_analysis"
                        ].model_dump()
                    )

                with st.expander(
                    "Annual Report Research"
                ):

                    st.json(
                        results[
                            "annual_report_analysis"
                        ].model_dump()
                    )

                with st.expander(
                    "Recent Articles"
                ):

                    recent_articles = results[
                        "recent_articles"
                    ]

                    if recent_articles:

                        for article in recent_articles:

                            title = article.get(
                                "title",
                                "Article",
                            )

                            url = article.get(
                                "url",
                                "",
                            )

                            snippet = article.get(
                                "snippet",
                                "",
                            )

                            if url:

                                st.markdown(
                                    f"**[{title}]({url})**"
                                )

                            else:

                                st.write(
                                    f"**{title}**"
                                )

                            if snippet:

                                st.write(
                                    clean_output(snippet)
                                )

                    else:

                        st.write(
                            "No recent public articles "
                            "were retrieved."
                        )

            except Exception as error:

                st.error(
                    "The account research could not "
                    "be completed."
                )

                with st.expander(
                    "Technical Details"
                ):

                    st.write(str(error))