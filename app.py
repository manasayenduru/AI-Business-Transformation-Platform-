import os
from reportlab.lib import styles
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from datetime import datetime

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

st.set_page_config(
page_title="AI Business Transformation Platform",
page_icon="🤖",
layout="wide"
)
st.markdown("""
<style>

/* Main App */
.main {
background-color: #F5F7FA;
}

/* Sidebar */
section[data-testid="stSidebar"] {
background: linear-gradient(180deg,#0F172A,#1E3A8A);
color:white;
}

/* Sidebar text */
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p {
color: white;
}

/* Dropdown selected value */
section[data-testid="stSidebar"] div[data-baseweb="select"] span {
color: #111827 !important;
}

/* Dropdown background */
section[data-testid="stSidebar"] div[data-baseweb="select"] {
background: white !important;
border-radius: 8px;
}


/* Dashboard Cards */
div[data-testid="metric-container"]{
background:white;
border-radius:15px;
padding:20px;
box-shadow:0px 3px 10px rgba(0,0,0,0.15);
border-left:6px solid #2563EB;
}

/* Buttons */
.stButton>button{
background:#2563EB;
color:white;
border-radius:10px;
height:50px;
font-weight:bold;
border:none;
}

.stButton>button:hover{
background:#1D4ED8;
}

/* Headers */
h1,h2,h3{
color:#1E293B;
}
<style>

/* all your existing CSS */

/* Fix dropdown text */
section[data-testid="stSidebar"] div[data-baseweb="select"] * {
color: #111827 !important;
}

section[data-testid="stSidebar"] input {
color: #111827 !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
            # 🚀 AI Business Transformation Platform
            ### Intelligent consulting powered by Google Gemini 
            """)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.info("🤖 AI Readiness")
with col2:
    st.info("📈 ROI Analysis")
with col3:
    st.info("🗺️ Roadmap")
with col4:
    st.info("📄 Executive Report")
st.sidebar.image(
"https://img.icons8.com/color/96/artificial-intelligence.png",
width=110
)

st.sidebar.markdown("## AI Consultant")
st.sidebar.markdown("---")

st.sidebar.header("Project Inputs")

industry = st.sidebar.selectbox(
"Industry",
["General Business", "Healthcare", "Retail", "Banking", "Insurance", "Manufacturing", "Customer Support", "Human Resources"]
)

company_size = st.sidebar.selectbox(
"Company Size",
["Startup", "Small Business", "Mid-size Company", "Enterprise"]
)

business_goal = st.sidebar.selectbox(
"Primary Business Goal",
["Reduce Costs", "Improve Customer Experience", "Increase Productivity", "Automate Manual Work", "Improve Decision Making", "Increase Revenue"]
)

ai_maturity = st.sidebar.selectbox(
"Current AI Maturity",
["No AI usage", "Basic AI tool usage", "Some workflow automation", "Advanced AI adoption"]
)


def calculate_ai_readiness(company_size, ai_maturity, business_goal):
    score = 30

    company_scores = {
        "Startup": 10,
        "Small Business": 15,
        "Mid-size Company": 20,
        "Enterprise": 25
    }

    maturity_scores = {
        "No AI usage": 5,
        "Basic AI tool usage": 20,
        "Some workflow automation": 30,
        "Advanced AI adoption": 40
    }

    goal_scores = {
        "Reduce Costs": 8,
        "Improve Customer Experience": 10,
        "Increase Productivity": 10,
        "Automate Manual Work": 10,
        "Improve Decision Making": 10,
        "Increase Revenue": 8
    }

    score += company_scores.get(company_size, 10)
    score += maturity_scores.get(ai_maturity, 5)
    score += goal_scores.get(business_goal, 5)

    return min(score, 100)


def get_readiness_level(score):
    if score < 50:
        return "Beginner"
    elif score < 75:
        return "Developing"
    else:
        return "Advanced"


def estimate_roi(company_size, business_goal):
    savings_map = {
        "Startup": 25000,
        "Small Business": 60000,
        "Mid-size Company": 180000,
        "Enterprise": 450000
    }

    roi_map = {
        "Reduce Costs": 220,
        "Improve Customer Experience": 180,
        "Increase Productivity": 200,
        "Automate Manual Work": 240,
        "Improve Decision Making": 160,
        "Increase Revenue": 210
    }

    return savings_map.get(company_size, 50000), roi_map.get(business_goal, 180)


def estimate_timeline(company_size):
    timeline_map = {
        "Startup": "6–8 weeks",
        "Small Business": "8–10 weeks",
        "Mid-size Company": "10–14 weeks",
        "Enterprise": "14–20 weeks"
    }

    return timeline_map.get(company_size, "8–12 weeks")
def create_pdf(
        report_text,
        readiness_score,
        roi,
        savings,
        timeline):

        pdf_file = "AI_Consulting_Report.pdf"

        doc = SimpleDocTemplate(pdf_file)
        styles = getSampleStyleSheet()

        title = styles["Title"]
        title.alignment = TA_CENTER

        heading = styles["Heading1"]

        body = styles["BodyText"]

        story = []

        story.append(
            Paragraph(
                "<font color='#1E3A8A'><b>AI Business Transformation Report</b></font>",
                title
            )
        )

        story.append(Spacer(1,20))

        story.append(
                Paragraph(
                    f"<b>Generated:</b> {datetime.now().strftime('%d %B %Y')}",
                    body
                )
        )

        story.append(Spacer(1,20))

        data = [
        ["Metric","Value"],
        ["AI Readiness",f"{readiness_score}/100"],
        ["Estimated ROI",f"{roi}%"],
        ["Annual Savings",f"${savings:,.0f}"],
        ["Timeline",timeline]
        ]

        table = Table(data)

        table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),HexColor("#2563EB")),
        ("TEXTCOLOR",(0,0),(-1,0),white),
        ("GRID",(0,0),(-1,-1),1,HexColor("#DDDDDD")),
        ("BACKGROUND",(0,1),(-1,-1),HexColor("#F8FAFC")),
        ("BOTTOMPADDING",(0,0),(-1,0),12)
        ]))

        story.append(table)

        story.append(Spacer(1,25))

        story.append(
        Paragraph("Executive AI Recommendation", heading)
        )

        story.append(Spacer(1,10))

        report = report_text.replace("\n","<br/>")

        story.append(
        Paragraph(report, body)
        )

        doc.build(story)
        return pdf_file

st.subheader("Describe the Business Challenge")

business_problem = st.text_area(
    "Business Problem",
    placeholder="Example: A retail company receives over 25,000 customer inquiries each month across email, chat, and phone. Customer response times exceed 24 hours, operational costs continue to raise, and customer satisfaction scores have declined. The company wants to leverage AI to automate repetitive support requests, improve customer experience, and reduce operational costs.",
    height=150
)

generate = st.button("Generate AI Consulting Report")

if generate:
    if not api_key:
        st.error("Gemini API key not found. Please check your .env file.")
    elif business_problem.strip() == "":
        st.warning("Please enter a business problem.")
    else:
        readiness_score = calculate_ai_readiness(company_size, ai_maturity, business_goal)
        readiness_level = get_readiness_level(readiness_score)
        estimated_savings, estimated_roi = estimate_roi(company_size, business_goal)
        timeline = estimate_timeline(company_size)

        st.subheader("📊 Executive AI Dashboard")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="🤖 AI Readiness", 
                value=f"{readiness_score}/100",
                delta=readiness_level
            )
            
        with col2:
            st.metric(
                label="💰 Estimated ROI",
                value=f"{estimated_roi}%"
            )
            
        with col3:
            st.metric(
                label="💵 Annual Savings",
                value=f"${estimated_savings:,}"
            )

        with col4:
            st.metric(
                label="📅 Timeline",
                value=timeline
            )

        st.progress(readiness_score / 100)
        st.info(f"""
                ### 🎯 Executive Summary
                **Industry:** {industry}
                **Company Size:** {company_size}
                **Business Goal:** {business_goal}
                **AI Maturity:** {ai_maturity}
                """)

        col5, col6 = st.columns(2)

        with col5:
            st.metric("Estimated Annual Savings", f"${estimated_savings:,}")

        with col6:
            st.metric("Primary Business Goal", business_goal)

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-3.1-flash-lite")

        prompt = f"""
You are a professional AI Business Transformation Consultant.

Create a detailed executive consulting report based on the following inputs.

Industry: {industry}
Company Size: {company_size}
Primary Business Goal: {business_goal}
Current AI Maturity: {ai_maturity}
AI Readiness Score: {readiness_score}/100
Readiness Level: {readiness_level}
Estimated Annual Savings: ${estimated_savings}
Estimated ROI: {estimated_roi}%
Estimated Implementation Timeline: {timeline}

Business Problem:
{business_problem}

Generate the response using this structure:

# Executive Summary
Summarize the business challenge and AI transformation opportunity.

# Current State Analysis
Explain current pain points and operational impact.

# AI Readiness Assessment
Explain what the readiness score means.

# AI Use Case Opportunities
List 4 to 6 practical AI use cases.

# Recommended AI Solution
Recommend the best-fit AI solution.

# Implementation Roadmap
Break into Phase 1, Phase 2, and Phase 3.

# ROI and Business Impact
Explain expected savings, ROI, productivity improvement, and customer/business impact.

# KPIs to Measure Success
List measurable KPIs.

# Risks and Mitigation
Explain risks and how to reduce them.

# Final Executive Recommendation
Give a concise executive-style recommendation.
"""

        with st.spinner("Generating AI consulting report..."):
            response = model.generate_content(prompt)

        st.success("AI consulting report generated successfully.")
        st.markdown(response.text)
        pdf_file = create_pdf(
            response.text,
            readiness_score,
            estimated_roi,
            estimated_savings,
            timeline
        )
        with open(pdf_file, "rb") as pdf:
            st.download_button(
                label="📄 Download Executive PDF Report",
                data=pdf.read(),
                file_name="AI_Consulting_Report.pdf",
                mime="application/pdf"
            )
        gauge = go.Figure(
        go.Indicator(
        mode="gauge+number",
        value=readiness_score,
        title={"text": "AI Readiness Score"},
        gauge={
        "axis": {"range": [0, 100]},
        "bar": {"color": "royalblue"},
        "steps": [
        {"range": [0, 40], "color": "#ffcccc"},
        {"range": [40, 70], "color": "#fff2cc"},
        {"range": [70, 100], "color": "#d9ead3"},
        ],
        },
        )
        )
        st.plotly_chart(gauge, use_container_width=True)
        st.markdown("---")
        st.subheader("📊 AI Transformation Metrics")

        chart_data = pd.DataFrame({
        "Category": [
        "Current Efficiency",
        "After AI",
        "Customer Satisfaction",
        "Automation",
        "Decision Speed"
        ],
        "Score": [
        45,
        85,
        90,
        80,
        88
        ]
        })

        st.bar_chart(
        chart_data.set_index("Category")
        )

        st.markdown("---")

