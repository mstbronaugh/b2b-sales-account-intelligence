# Cyber2Safe B2B Sales Intelligence

Cyber2Safe B2B Sales Intelligence is an AI-powered research assistant designed to support B2B cybersecurity sales prospecting.

The application researches a prospective organization using publicly available information and transforms the research into actionable sales intelligence for Cyber2Safe.

## What the Application Does

The system can:

- Research a prospective company's strategy and business priorities
- Identify cybersecurity-relevant business signals
- Research and compare a supplied competitor
- Generate a side-by-side competitor analysis
- Research relevant company leadership
- Review available annual report and 10-K information
- Review recent public developments
- Recommend a Cyber2Safe service based on retrieved evidence
- Generate a sales angle and suggested outreach
- Display verified public sources

## AI Architecture

The project uses a multi-agent workflow with specialized components for:

1. Company research
2. Competitor analysis
3. Leadership research
4. Annual report and 10-K research
5. Sales recommendation and account intelligence

LangChain coordinates the AI workflow and prompt structure.

Groq provides API access to the large language model used to analyze the retrieved information and generate the account intelligence.

Streamlit provides the interactive web interface.

## Responsible AI Approach

The system is designed to reduce unsupported AI-generated claims.

Prompts instruct the model to:

- Use retrieved public information
- Avoid inventing company facts
- Avoid assuming missing information represents a weakness
- Clearly identify unavailable information
- Separate verified information from sales recommendations
- Avoid inventing cybersecurity vulnerabilities, breaches, or compliance failures

## Cyber2Safe Services

The application evaluates opportunities for two Cyber2Safe services:

### Cybersecurity Assessment

A practical review of an organization's cybersecurity practices with recommendations for areas that may require improvement.

### Cybersecurity Awareness Training

Educational training focused on practical cybersecurity awareness and human-centered cyber risk.

## Technology

- Python
- LangChain
- Groq API
- Streamlit
- Pydantic
- UV
- Git/GitHub

## Example Workflow

User Input  
→ Prospect Research  
→ Competitor Research  
→ Leadership Research  
→ Public Filing Research  
→ AI Analysis  
→ Cyber2Safe Recommendation  
→ B2B Account Brief

## Project Purpose

This project demonstrates how generative AI and structured research workflows can support cybersecurity-focused B2B sales intelligence while maintaining evidence-based output and reducing unsupported model assumptions.