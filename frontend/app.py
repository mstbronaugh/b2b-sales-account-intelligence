import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from agents.research_agent import run_research_workflow


def clean_output(text):
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
    "Research a prospective company and identify opportunities "
    "for Cyber2Safe cybersecurity assessments and awareness training."
)


# ============================================================
# INPUT FORM
# ============================================================

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
            "https://www.competitor.com"
        ),
    )

    submitted = st.form_submit_button(
        "Generate Account Intelligence"
    )


# ============================================================
# RUN RESEARCH
# ============================================================

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
            "Researching company strategy, competitors, leadership, "
            "public filings, and Cyber2Safe sales opportunities..."
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
                company_analysis = results["company_analysis"]
                competitor_analysis = results["competitor_analysis"]
                leadership_analysis = results["leadership_analysis"]
                annual_report_analysis = results["annual_report_analysis"]
                recent_articles = results["recent_articles"]

                st.success(
                    "Account intelligence research complete."
                )


                # ====================================================
                # COMPANY
                # ====================================================

                st.header("One-Page Account Brief")

                st.subheader(brief.company_name)

                st.markdown("### Company Strategy")

                st.markdown(
                    clean_output(
                        company_analysis.company_strategy
                    )
                )


                # ====================================================
                # COMPETITOR ANALYSIS
                # ====================================================

                st.markdown("### Competitor Analysis")

                competitor_text = clean_output(
                    competitor_analysis.competitor_summary
                ).strip()

                if competitor_urls and competitor_text:

                    st.markdown(
                        competitor_text
                    )

                elif competitor_urls:

                    st.info(
                        "No verified competitor comparison was "
                        "available from the retrieved public information."
                    )

                else:

                    st.info(
                        "No competitor was provided for comparison."
                    )


                # ====================================================
                # LEADERSHIP
                # ====================================================

                st.markdown("### Leadership")

                leadership_text = clean_output(
                    leadership_analysis.leadership_summary
                ).strip()

                unavailable_leadership = (
                    not leadership_text
                    or "couldn't locate" in leadership_text.lower()
                    or "could not locate" in leadership_text.lower()
                    or "not allowed to invent" in leadership_text.lower()
                    or "i'm sorry" in leadership_text.lower()
                )

                if unavailable_leadership:

                    st.info(
                        "No verified leadership information was "
                        "retrieved from the available public sources."
                    )

                else:

                    st.markdown(
                        leadership_text
                    )


                # ====================================================
                # ANNUAL REPORT
                # ====================================================

                st.markdown(
                    "### Annual Report / 10-K Insights"
                )

                annual_insights = (
                    annual_report_analysis
                    .cybersecurity_relevant_insights
                )

                if annual_insights:

                    st.markdown(
                        clean_output(
                            "\n\n".join(
                                annual_insights
                            )
                        )
                    )

                else:

                    st.info(
                        "No public annual report or 10-K filing "
                        "was retrieved. This may occur when "
                        "researching a privately held company."
                    )


                # ====================================================
                # RECENT DEVELOPMENTS
                # ====================================================

                st.markdown("### Recent Developments")

                if recent_articles:

                    for article in recent_articles[:5]:

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

                            st.markdown(
                                f"**{title}**"
                            )

                        if snippet:

                            st.write(
                                clean_output(snippet)
                            )

                else:

                    st.info(
                        "No recent public developments were retrieved."
                    )


                # ====================================================
                # CYBER2SAFE OPPORTUNITY
                # ====================================================

                st.markdown("---")

                st.header("Cyber2Safe Opportunity")

                #
                # IMPORTANT:
                # Display the AI recommendation, NOT the form selection.
                #

                recommended_service = getattr(
                    sales,
                    "recommended_cyber2safe_service",
                    "",
                )

                if recommended_service:

                    st.write(
                        "**Recommended Service:** "
                        f"{recommended_service}"
                    )

                else:

                    st.write(
                        "**Recommended Service:** "
                        "See AI recommendation below."
                    )


                # ====================================================
                # SALES OPPORTUNITY
                # ====================================================

                st.markdown("### Sales Opportunity")

                opportunity = getattr(
                    sales,
                    "opportunity_summary",
                    "",
                )

                if opportunity:

                    st.markdown(
                        clean_output(
                            opportunity
                        )
                    )

                else:

                    st.info(
                        "No specific sales opportunity was identified "
                        "from the verified public information."
                    )


                # ====================================================
                # SALES ANGLE
                # ====================================================

                st.markdown(
                    "### Recommended Sales Angle"
                )

                sales_angle = getattr(
                    sales,
                    "recommended_sales_angle",
                    "",
                )

                if sales_angle:

                    st.markdown(
                        clean_output(
                            sales_angle
                        )
                    )

                else:

                    st.info(
                        "No specific sales angle was generated."
                    )


                # ====================================================
                # OUTREACH
                # ====================================================

                st.markdown("### Suggested Outreach")

                outreach = getattr(
                    sales,
                    "suggested_outreach_message",
                    "",
                )

                if outreach:

                    st.markdown(
                        clean_output(
                            outreach
                        )
                    )

                else:

                    st.info(
                        "No outreach message was generated."
                    )


                # ====================================================
                # SOURCES
                # ====================================================

                st.markdown("---")

                st.header("Verified Public Sources")

                source_links = []

                if getattr(
                    brief,
                    "source_links",
                    None,
                ):

                    source_links.extend(
                        brief.source_links
                    )

                if getattr(
                    competitor_analysis,
                    "source_links",
                    None,
                ):

                    source_links.extend(
                        competitor_analysis.source_links
                    )

                unique_sources = []

                for source in source_links:

                    if (
                        source
                        and source not in unique_sources
                    ):

                        unique_sources.append(
                            source
                        )

                if unique_sources:

                    for source in unique_sources:

                        st.markdown(
                            f"- [{source}]({source})"
                        )

                else:

                    st.info(
                        "No public source links were retrieved."
                    )


                # ====================================================
                # TECHNICAL DETAILS
                # ====================================================

                st.markdown("---")

                with st.expander(
                    "Detailed Company Research"
                ):

                    st.json(
                        company_analysis.model_dump()
                    )


                with st.expander(
                    "Detailed Competitor Research"
                ):

                    if competitor_urls:

                        st.markdown(
                            competitor_text
                        )

                    else:

                        st.write(
                            "No competitor was provided."
                        )


                with st.expander(
                    "Detailed Leadership Research"
                ):

                    st.json(
                        leadership_analysis.model_dump()
                    )


                with st.expander(
                    "Detailed Annual Report Research"
                ):

                    st.json(
                        annual_report_analysis.model_dump()
                    )


                with st.expander(
                    "Recent Articles"
                ):

                    if recent_articles:

                        for article in recent_articles:

                            st.json(
                                article
                            )

                    else:

                        st.write(
                            "No recent public articles were retrieved."
                        )


            except Exception as error:

                st.error(
                    "The account research could not be completed."
                )

                with st.expander(
                    "Technical Details"
                ):

                    st.write(
                        str(error)
                    )
