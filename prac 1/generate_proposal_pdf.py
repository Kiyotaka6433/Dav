import os
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, HRFlowable)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

OUTPUT_PDF = r"C:\Users\aryan\dav\prac 1\project_proposal_report.pdf"
OUTPUT_MD = r"C:\Users\aryan\dav\prac 1\project_proposal_report.md"

print("Building Practical 1 Project Proposal PDF...")

doc = SimpleDocTemplate(
    OUTPUT_PDF, pagesize=A4,
    leftMargin=1.8*cm, rightMargin=1.8*cm,
    topMargin=1.8*cm, bottomMargin=1.8*cm
)

styles = getSampleStyleSheet()

def S(name, parent, **kw):
    return ParagraphStyle(name, parent=parent, **kw)

# Palette
DARK_NAVY  = HexColor("#1A237E")
ROYAL_BLUE = HexColor("#0D47A1")
LIGHT_BLUE = HexColor("#E3F2FD")
ACCENT_ORANGE = HexColor("#E65100")
GREY_BG    = HexColor("#F5F5F5")
GREY_LINE  = HexColor("#D0D0D0")
DARK_TEXT  = HexColor("#212121")

title_style = S("P1Title", styles['Heading1'], fontSize=16, textColor=DARK_NAVY, alignment=TA_CENTER, fontName="Helvetica-Bold", leading=20, spaceAfter=4)
subtitle_style = S("P1SubTitle", styles['Heading2'], fontSize=12, textColor=ROYAL_BLUE, alignment=TA_CENTER, fontName="Helvetica-Bold", leading=16, spaceAfter=2)
info_style = S("P1Info", styles['Normal'], fontSize=9.5, textColor=HexColor("#424242"), alignment=TA_CENTER, fontName="Helvetica", leading=14)

sec_title = S("P1SecTitle", styles['Heading2'], fontSize=13, textColor=DARK_NAVY, fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=4, leading=16)
body_text = S("P1Body", styles['Normal'], fontSize=9.5, textColor=DARK_TEXT, fontName="Helvetica", leading=13.5, spaceAfter=4, alignment=TA_JUSTIFY)
body_bold = S("P1BodyBold", styles['Normal'], fontSize=9.5, textColor=DARK_NAVY, fontName="Helvetica-Bold", leading=13.5, spaceAfter=4)
bullet_item = S("P1Bullet", styles['Normal'], fontSize=9, textColor=DARK_TEXT, fontName="Helvetica", leading=13, leftIndent=12, spaceAfter=2)

th_style = S("P1TH", styles['Normal'], fontSize=8.5, textColor=white, fontName="Helvetica-Bold", alignment=TA_LEFT)
tb_style = S("P1TB", styles['Normal'], fontSize=8, textColor=DARK_TEXT, fontName="Helvetica", leading=10.5)
tb_bold  = S("P1TBB", styles['Normal'], fontSize=8, textColor=DARK_NAVY, fontName="Helvetica-Bold", leading=10.5)

story = []

# ── HEADER & TITLE ──
story.append(Paragraph("<b>Name:</b> Aryan & Project Team", S("hdr1", styles['Normal'], fontSize=10, textColor=DARK_TEXT, fontName="Helvetica-Bold")))
story.append(Paragraph("<b>Roll No:</b> 24BCE501 & 24BCE502", S("hdr2", styles['Normal'], fontSize=10, textColor=DARK_TEXT, fontName="Helvetica-Bold")))
story.append(Paragraph("<b>Subject:</b> Data Analysis and Visualization", S("hdr3", styles['Normal'], fontSize=10, textColor=DARK_TEXT, fontName="Helvetica-Bold")))
story.append(Spacer(1, 0.4*cm))

story.append(Paragraph("DATA ANALYTICS & VISUALIZATION PROJECT REPORT", title_style))
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph("Project Title", subtitle_style))
story.append(Paragraph("S&P 500 Financial & Fundamental Market Analytics using Open Financial Data", S("ptitle", styles['Normal'], fontSize=11, textColor=DARK_NAVY, alignment=TA_CENTER, fontName="Helvetica-Bold", leading=14)))
story.append(Spacer(1, 0.3*cm))
story.append(HRFlowable(width="100%", thickness=1.5, color=DARK_NAVY, spaceAfter=8))

# ── 1. INTRODUCTION ──
story.append(Paragraph("1. Introduction", sec_title))
story.append(Paragraph(
    "The rapid growth of algorithmic trading and quantitative finance has increased the demand for robust financial data analysis pipelines. "
    "Governments, regulatory bodies, and financial institutions rely heavily on accurate market datasets to monitor corporate health, "
    "evaluate systemic risk, and maintain fair capital markets.<br/><br/>"
    "The objective of this project is to analyze S&P 500 market pricing and corporate fundamental session data collected from open financial data portals. "
    "The dataset contains comprehensive information about stock pricing sessions, trading volumes, corporate balance sheets, income statements, cash flows, "
    "and GICS industry sector classifications. This analysis helps understand market behavior, corporate financial stability, and pricing efficiency.<br/><br/>"
    "The project aims to discover hidden patterns in corporate performance, identify market risks, eliminate look-ahead data leakage, and develop predictive models "
    "that support strategic portfolio planning and quantitative decision-making.",
    body_text
))

# ── 2. PROBLEM STATEMENT ──
story.append(Paragraph("2. Problem Statement", sec_title))
story.append(Paragraph(
    "With the increasing complexity of financial markets, historical data modeling faces severe technical challenges including look-ahead bias, "
    "stock split distortions, extreme class imbalance across industry sectors, and high feature collinearity. Improper data processing leads to "
    "flawed backtests, poor portfolio risk management, and failed predictive models.<br/><br/>"
    "The challenge is to clean, prune, and analyze financial market data to answer key questions such as:",
    body_text
))
story.append(Paragraph("• Which GICS sectors and sub-industries generate the highest revenue and net income?", bullet_item))
story.append(Paragraph("• How do corporate fundamental metrics impact daily stock price volatility and returns?", bullet_item))
story.append(Paragraph("• What factors cause high collinearity between balance sheet line items?", bullet_item))
story.append(Paragraph("• Can corporate filing lag (90-day window) be modeled without leaking future financial knowledge?", bullet_item))
story.append(Paragraph("• Can stock returns and sector classifications be accurately predicted using quantitative algorithms?", bullet_item))

# ── 3. OBJECTIVES ──
story.append(Paragraph("3. Objectives", sec_title))
story.append(Paragraph("The main objectives of this project are:", body_text))
story.append(Paragraph("• Analyze S&P 500 stock pricing and fundamental financial performance patterns.", bullet_item))
story.append(Paragraph("• Eliminate statistical look-ahead bias by enforcing a strict 90-day accounting filing lag.", bullet_item))
story.append(Paragraph("• Reduce feature dimensionality by pruning collinear and redundant balance sheet attributes (from 92 columns to 34 key features).", bullet_item))
story.append(Paragraph("• Compare financial metrics across GICS industry sectors.", bullet_item))
story.append(Paragraph("• Predict stock price returns and sector classifications using machine learning models.", bullet_item))
story.append(Paragraph("• Provide actionable quantitative recommendations for portfolio managers and quantitative analysts.", bullet_item))

story.append(PageBreak())

# ── 4. DATASET DESCRIPTION ──
story.append(Paragraph("4. Dataset Description", sec_title))
story.append(Paragraph(
    "The dataset consists of S&P 500 corporate financial records and daily trading sessions collected from open financial data platforms. "
    "The raw dataset originally contained over 851,000 price records and 1,780 fundamental quarterly filings across 92 attributes. "
    "Through feature selection and collinearity reduction, an optimized subset of **34 core attributes** was retained.<br/><br/>"
    "<b>Selected Key Dataset Attributes (30 Key Fields):</b>",
    body_text
))

# Table of 30 Key Attributes
attr_data = [
    [Paragraph("<b>Attribute</b>", th_style), Paragraph("<b>Category</b>", th_style), Paragraph("<b>Description & Rationale</b>", th_style)],
    [Paragraph("symbol", tb_bold), Paragraph("Metadata Key", tb_style), Paragraph("Unique ticker identifier for cross-table joins.", tb_style)],
    [Paragraph("Security", tb_bold), Paragraph("Metadata", tb_style), Paragraph("Official corporate company name.", tb_style)],
    [Paragraph("GICS Sector", tb_bold), Paragraph("Target Label", tb_style), Paragraph("Broad industry classification (11 primary sectors).", tb_style)],
    [Paragraph("GICS Sub Industry", tb_bold), Paragraph("Metadata", tb_style), Paragraph("Granular industry sub-category.", tb_style)],
    [Paragraph("date", tb_bold), Paragraph("Timestamp", tb_style), Paragraph("Daily stock trading session date.", tb_style)],
    [Paragraph("Period Ending", tb_bold), Paragraph("Timestamp", tb_style), Paragraph("Accounting report period end date.", tb_style)],
    [Paragraph("lagged_date", tb_bold), Paragraph("Timestamp", tb_style), Paragraph("Public filing date shifted by 90 days to prevent look-ahead bias.", tb_style)],
    [Paragraph("open", tb_bold), Paragraph("Price (USD)", tb_style), Paragraph("Split-adjusted opening market price.", tb_style)],
    [Paragraph("high", tb_bold), Paragraph("Price (USD)", tb_style), Paragraph("Split-adjusted highest intra-day price.", tb_style)],
    [Paragraph("low", tb_bold), Paragraph("Price (USD)", tb_style), Paragraph("Split-adjusted lowest intra-day price.", tb_style)],
    [Paragraph("close", tb_bold), Paragraph("Price (USD)", tb_style), Paragraph("Split-adjusted closing market price.", tb_style)],
    [Paragraph("volume", tb_bold), Paragraph("Trading Vol", tb_style), Paragraph("Total number of shares traded during session.", tb_style)],
    [Paragraph("Total Revenue", tb_bold), Paragraph("Income Stmt", tb_style), Paragraph("Total gross top-line corporate revenue.", tb_style)],
    [Paragraph("Cost of Revenue", tb_bold), Paragraph("Income Stmt", tb_style), Paragraph("Direct cost of goods and services sold.", tb_style)],
    [Paragraph("Gross Profit", tb_bold), Paragraph("Income Stmt", tb_style), Paragraph("Gross earnings before operating overhead.", tb_style)],
    [Paragraph("Operating Income", tb_bold), Paragraph("Income Stmt", tb_style), Paragraph("Core operational earnings (EBIT).", tb_style)],
    [Paragraph("Net Income", tb_bold), Paragraph("Income Stmt", tb_style), Paragraph("Bottom-line net profit after tax and interest.", tb_style)],
    [Paragraph("Research & Development", tb_bold), Paragraph("Income Stmt", tb_style), Paragraph("Total corporate R&D investment expenditure.", tb_style)],
    [Paragraph("Cash & Equivalents", tb_bold), Paragraph("Balance Sheet", tb_style), Paragraph("Highly liquid cash reserves.", tb_style)],
    [Paragraph("Net Receivables", tb_bold), Paragraph("Balance Sheet", tb_style), Paragraph("Outstanding customer payments owed.", tb_style)],
    [Paragraph("Inventory", tb_bold), Paragraph("Balance Sheet", tb_style), Paragraph("Valuation of unsold goods and materials.", tb_style)],
    [Paragraph("Total Current Assets", tb_bold), Paragraph("Balance Sheet", tb_style), Paragraph("Assets convertible to cash within 12 months.", tb_style)],
    [Paragraph("Total Assets", tb_bold), Paragraph("Balance Sheet", tb_style), Paragraph("Total corporate balance sheet asset valuation.", tb_style)],
    [Paragraph("Total Liabilities", tb_bold), Paragraph("Balance Sheet", tb_style), Paragraph("Total corporate debt and financial obligations.", tb_style)],
    [Paragraph("Total Equity", tb_bold), Paragraph("Balance Sheet", tb_style), Paragraph("Net book value of shareholder equity.", tb_style)],
    [Paragraph("Gross Margin", tb_bold), Paragraph("Ratio", tb_style), Paragraph("Percentage of revenue retained after direct costs.", tb_style)],
    [Paragraph("Operating Margin", tb_bold), Paragraph("Ratio", tb_style), Paragraph("Core operational efficiency margin percentage.", tb_style)],
    [Paragraph("Current Ratio", tb_bold), Paragraph("Ratio", tb_style), Paragraph("Short-term liquidity ratio (Current Assets / Liabilities).", tb_style)],
    [Paragraph("Earnings Per Share", tb_bold), Paragraph("Metric", tb_style), Paragraph("Net profit divided by total share count (EPS).", tb_style)],
    [Paragraph("Estimated Shares Out", tb_bold), Paragraph("Shares", tb_style), Paragraph("Total number of common shares outstanding.", tb_style)],
]

attr_table = Table(attr_data, colWidths=[4.0*cm, 3.0*cm, 10.4*cm])
attr_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), ROYAL_BLUE),
    ('GRID', (0,0), (-1,-1), 0.4, GREY_LINE),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, GREY_BG]),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(attr_table)
story.append(Spacer(1, 0.4*cm))

# ── 5. STAKEHOLDERS ──
story.append(Paragraph("5. Stakeholders", sec_title))
story.append(Paragraph("The findings of this project are valuable for multiple key stakeholders across finance and technology:", body_text))
story.append(Paragraph("<b>Quantitative Analysts (Quants):</b> Build leak-free algorithmic trading models and backtest quantitative factors.", bullet_item))
story.append(Paragraph("<b>Portfolio Managers:</b> Monitor sector exposure risk and optimize asset allocation across GICS industries.", bullet_item))
story.append(Paragraph("<b>Corporate Finance Officers:</b> Benchmark operational efficiency, profit margins, and debt leverage against sector peers.", bullet_item))
story.append(Paragraph("<b>Data Engineers:</b> Automate clean ETL ingestion pipelines while handling missingness and date alignment.", bullet_item))
story.append(Paragraph("<b>Individual / Retail Investors:</b> Access clean financial ratio summaries to identify undervalued equities.", bullet_item))
story.append(Paragraph("<b>Academic Researchers:</b> Study market efficiency, leptokurtic distribution shapes, and factor predictability.", bullet_item))

# ── 6. BUSINESS PROBLEM ──
story.append(Paragraph("6. Business Problem", sec_title))
story.append(Paragraph("The project addresses the following critical business and analytical questions:", body_text))
story.append(Paragraph("• Which GICS sectors demonstrate the highest profit margins and revenue growth?", bullet_item))
story.append(Paragraph("• Which balance sheet line items cause severe collinearity ($r > 0.99$) and require pruning?", bullet_item))
story.append(Paragraph("• What is the impact of accounting filing lag (90 days) on signal accuracy?", bullet_item))
story.append(Paragraph("• Which financial ratios best predict stock price volatility and returns?", bullet_item))
story.append(Paragraph("• Can machine learning models accurately classify company industry sectors based on balance sheet metrics?", bullet_item))

story.append(PageBreak())

# ── 7. DATA PREPROCESSING PLAN ──
story.append(Paragraph("7. Data Preprocessing Plan", sec_title))
story.append(Paragraph("The following preprocessing steps are executed:", body_text))
story.append(Paragraph("• Standardize ticker symbol keys across Securities, Fundamentals, and Prices.", bullet_item))
story.append(Paragraph("• Remove redundant index columns (e.g. <i>Unnamed: 0</i>, <i>CIK</i>, <i>SEC filings</i>).", bullet_item))
story.append(Paragraph("• Enforce a strict 90-day accounting filing lag (<i>lagged_date = Period Ending + 90 days</i>).", bullet_item))
story.append(Paragraph("• Prune collinear features ($r > 0.95$, such as dropping Total Liabilities & Equity in favor of Total Assets).", bullet_item))
story.append(Paragraph("• Execute an as-of join (<i>pd.merge_asof</i>) to match daily prices with the latest public fundamental records.", bullet_item))
story.append(Paragraph("• Preserve numeric nulls to prevent premature imputation bias.", bullet_item))

# ── 8. EXPLORATORY DATA ANALYSIS ──
story.append(Paragraph("8. Exploratory Data Analysis", sec_title))
story.append(Paragraph("The planned exploratory visualizations include:", body_text))
story.append(Paragraph("• GICS Sector classwise balance distribution analysis.", bullet_item))
story.append(Paragraph("• Missing value percentage distribution across fundamental metrics.", bullet_item))
story.append(Paragraph("• Historical split-adjusted price trajectories for major tickers.", bullet_item))
story.append(Paragraph("• Daily active trading ticker volume timelines.", bullet_item))
story.append(Paragraph("• Correlation matrix heatmaps evaluating collinearity among balance sheet metrics.", bullet_item))

# ── 9. MACHINE LEARNING OPPORTUNITIES ──
story.append(Paragraph("9. Machine Learning Opportunities", sec_title))
story.append(Paragraph("<b>Regression (Predict Stock Returns & Close Prices):</b>", body_bold))
story.append(Paragraph("• Algorithms: Linear Regression, Ridge/Lasso, Random Forest Regressor, XGBoost Regressor.", bullet_item))
story.append(Paragraph("<b>Classification (Predict GICS Sector Category):</b>", body_bold))
story.append(Paragraph("• Algorithms: Logistic Regression, Decision Trees, Random Forest Classifier, Support Vector Machines.", bullet_item))
story.append(Paragraph("<b>Clustering (Group Similar Corporate Profiles):</b>", body_bold))
story.append(Paragraph("• Algorithms: K-Means Clustering, DBSCAN, Hierarchical Clustering.", bullet_item))
story.append(Paragraph("<b>Time Series Forecasting (Predict Market Demand & Prices):</b>", body_bold))
story.append(Paragraph("• Algorithms: ARIMA, Prophet, LSTM Neural Networks.", bullet_item))

# ── 10. KEY PERFORMANCE INDICATORS (KPIS) ──
story.append(Paragraph("10. Key Performance Indicators (KPIs)", sec_title))
story.append(Paragraph("• Total Market Revenue & Net Income", bullet_item))
story.append(Paragraph("• Average Gross & Operating Margins per Sector", bullet_item))
story.append(Paragraph("• Current Ratio & Quick Ratio Liquidity Standards", bullet_item))
story.append(Paragraph("• Annualized Price Volatility & Sharpe Ratio", bullet_item))
story.append(Paragraph("• Model Mean Absolute Error (MAE) & Root Mean Squared Error (RMSE)", bullet_item))
story.append(Paragraph("• Classification F1-Score & Accuracy across Sectors", bullet_item))

# ── 11. PROPOSED VISUALIZATIONS ──
story.append(Paragraph("11. Proposed Visualizations", sec_title))
story.append(Paragraph("• Line Charts (Historical price trends & active ticker timelines)", bullet_item))
story.append(Paragraph("• Bar Charts (Sector counts & missing value percentages)", bullet_item))
story.append(Paragraph("• Correlation Heatmaps (Feature collinearity evaluation)", bullet_item))
story.append(Paragraph("• Box Plots (Spread of financial ratios across industries)", bullet_item))
story.append(Paragraph("• Interactive Dashboards & KPI Cards", bullet_item))

# ── 12. EXPECTED OUTCOMES ──
story.append(Paragraph("12. Expected Outcomes", sec_title))
story.append(Paragraph("• Establish a clean, leak-free financial dataset pruned of collinear features.", bullet_item))
story.append(Paragraph("• Identify high-performing GICS sectors and corporate profit drivers.", bullet_item))
story.append(Paragraph("• Accurately predict stock returns without look-ahead bias.", bullet_item))
story.append(Paragraph("• Provide quantitative insights to assist portfolio managers in risk optimization.", bullet_item))

# ── 13. TOOLS AND TECHNOLOGIES ──
story.append(Paragraph("13. Tools and Technologies", sec_title))
story.append(Paragraph("• <b>Languages & Environments:</b> Python 3.13, Jupyter Notebook", bullet_item))
story.append(Paragraph("• <b>Data Processing:</b> Pandas, NumPy", bullet_item))
story.append(Paragraph("• <b>Visualization:</b> Matplotlib, Seaborn", bullet_item))
story.append(Paragraph("• <b>Machine Learning:</b> Scikit-Learn, XGBoost", bullet_item))
story.append(Paragraph("• <b>Reporting:</b> ReportLab PDF Engine", bullet_item))

# ── 14. FUTURE SCOPE & THEME ──
story.append(Paragraph("14. Future Scope", sec_title))
story.append(Paragraph("• Live API integration for real-time stock pricing.", bullet_item))
story.append(Paragraph("• Automated sentiment analysis of SEC 10-K text filings using NLP.", bullet_item))
story.append(Paragraph("• Deep learning (LSTM / Transformer) real-time return forecasting.", bullet_item))
story.append(Spacer(1, 0.4*cm))

story.append(Paragraph("<b>Overall Project Theme:</b>", body_bold))
story.append(Paragraph(
    "<i>\"Data-driven quantitative analysis of S&P 500 corporate fundamentals and stock pricing to eliminate data leakage, "
    "prune collinearity, optimize portfolio risk, and support sustainable investment decision-making.\"</i>",
    body_text
))

doc.build(story)
print("Practical 1 Project Proposal PDF generated successfully!")
print(f"Location: {OUTPUT_PDF}")
