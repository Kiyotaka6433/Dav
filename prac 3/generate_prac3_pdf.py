import os
import pandas as pd

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, HRFlowable, Image)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

# Paths
PRAC3_DIR = r"C:\Users\aryan\dav\prac 3"
PLOTS_DIR = os.path.join(PRAC3_DIR, "plots")
SUMMARY_CSV = os.path.join(PRAC3_DIR, "prac3_summary_metrics.csv")
OUTPUT_PDF = os.path.join(PRAC3_DIR, "eda_outlier_report.pdf")

print("=== Starting Practical 3 Earth-Tone PDF Generator ===")

doc = SimpleDocTemplate(
    OUTPUT_PDF, pagesize=A4,
    leftMargin=1.8*cm, rightMargin=1.8*cm,
    topMargin=1.8*cm, bottomMargin=1.8*cm
)

styles = getSampleStyleSheet()

def S(name, parent, **kw):
    return ParagraphStyle(name, parent=parent, **kw)

# STRICT EARTH TONE PALETTE (NO BLUE, NO PURPLE)
COLOR_PRIMARY     = HexColor("#5D3A1A")  # Deep Saddle Brown
COLOR_SECONDARY   = HexColor("#B85B35")  # Terracotta / Rust
COLOR_ACCENT      = HexColor("#4A5D4E")  # Olive / Sage
COLOR_BG_LIGHT    = HexColor("#FDFBF7")  # Warm Cream
COLOR_CARD_BG     = HexColor("#F4EBE1")  # Warm Sand
COLOR_LINE        = HexColor("#D2C4B5")  # Earthy Taupe Line
COLOR_TEXT        = HexColor("#2B2523")  # Dark Charcoal Text
COLOR_MUTED       = HexColor("#5A524E")  # Muted Earth Text

title_style = S("P3Title", styles['Heading1'], fontSize=15, textColor=COLOR_PRIMARY, alignment=TA_CENTER, fontName="Helvetica-Bold", leading=19, spaceAfter=4)
subtitle_style = S("P3SubTitle", styles['Heading2'], fontSize=11, textColor=COLOR_SECONDARY, alignment=TA_CENTER, fontName="Helvetica-Bold", leading=15, spaceAfter=2)
info_style = S("P3Info", styles['Normal'], fontSize=9, textColor=COLOR_MUTED, alignment=TA_CENTER, fontName="Helvetica", leading=13)

sec_title = S("P3SecTitle", styles['Heading2'], fontSize=12, textColor=COLOR_PRIMARY, fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=4, leading=15)
subsec_title = S("P3SubSecTitle", styles['Heading3'], fontSize=10.5, textColor=COLOR_SECONDARY, fontName="Helvetica-Bold", spaceBefore=6, spaceAfter=3, leading=13)

body_style = S("P3Body", styles['Normal'], fontSize=8.8, textColor=COLOR_TEXT, fontName="Helvetica", leading=12.5, alignment=TA_JUSTIFY, spaceAfter=5)
bullet_style = S("P3Bullet", body_style, leftIndent=12, spaceAfter=3)

th_style = S("P3TH", styles['Normal'], fontSize=7.5, textColor=white, fontName="Helvetica-Bold", alignment=TA_CENTER, leading=9.5)
tb_style = S("P3TB", styles['Normal'], fontSize=7.0, textColor=COLOR_TEXT, fontName="Helvetica", alignment=TA_CENTER, leading=9.0)
tb_left  = S("P3TBLeft", styles['Normal'], fontSize=7.0, textColor=COLOR_TEXT, fontName="Helvetica", alignment=TA_LEFT, leading=9.0)

story = []

# --- Header ---
story.append(Paragraph("DATA ANALYSIS & VISUALIZATION — PRACTICAL 3 REPORT", title_style))
story.append(Paragraph("5-Number Summary, Central Tendency & Comparative Outlier Detection", subtitle_style))
story.append(Paragraph("<b>Authors:</b> Aryan Mori (24BCE119) & Shlok Vaishnav (24BCE135)<br/>Nirma University • B.Tech CSE Semester-IV • Subject Code: 2CS504CC23", info_style))
story.append(Spacer(1, 6))
story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_SECONDARY, spaceBefore=2, spaceAfter=8))

# --- Section 1: Executive Summary ---
story.append(Paragraph("1. Executive Summary & Audit Overview", sec_title))
story.append(HRFlowable(width="100%", thickness=0.8, color=COLOR_LINE, spaceBefore=1, spaceAfter=5))

exec_text = (
    "Following the data pruning and 90-day filing lag alignment established in Practical 2, "
    "this report conducts a rigorous statistical examination of the cleaned S&P 500 financial dataset "
    "(<b>34 attributes, 851,264 records</b>). The primary objective is to evaluate distribution spread, "
    "central tendency measures, and outlier behavior using non-parametric and parametric techniques."
)
story.append(Paragraph(exec_text, body_style))

story.append(Paragraph("<b>Core Audit Takeaways:</b>", body_style))
story.append(Paragraph("• <b>Distribution Asymmetry:</b> Financial metrics (Revenue, Assets, Net Income, Volume) exhibit extreme positive skewness (+5.20 to +13.13), causing the arithmetic Mean to be strongly pulled away from the Median.", bullet_style))
story.append(Paragraph("• <b>Midrange Vulnerability:</b> The Midrange statistic, defined as (Min + Max) / 2, is highly unstable for financial variables. For instance, Total Assets has a Median of $14.93 Billion but a Midrange of $1.285 Trillion due to mega-cap banking institutions.", bullet_style))
story.append(Paragraph("• <b>Outlier Detection Disparity:</b> Tukey's IQR Method flags 6.06% to 12.43% of data as outliers based on quartile boundaries, whereas the Z-Score Method (|Z| > 3.0) flags only 1.30% to 2.27% because heavy tails inflate the sample standard deviation.", bullet_style))
story.append(Spacer(1, 6))

# --- Section 2: 5-Number Summary Table ---
story.append(Paragraph("2. Comprehensive 5-Number Summary & Descriptive Statistics", sec_title))
story.append(HRFlowable(width="100%", thickness=0.8, color=COLOR_LINE, spaceBefore=1, spaceAfter=5))

intro_sec2 = (
    "The 5-Number Summary consists of the Minimum (Min), 25th Percentile (Q1), Median (Q2), "
    "75th Percentile (Q3), and Maximum (Max). Combined with the Sample Mean, Standard Deviation, "
    "Interquartile Range (IQR = Q3 - Q1), Midrange, and Skewness, it provides a robust structural overview."
)
story.append(Paragraph(intro_sec2, body_style))

# Load metrics from CSV
metrics_df = pd.read_csv(SUMMARY_CSV)

table_data = [[
    Paragraph("Feature Name", th_style),
    Paragraph("Min", th_style),
    Paragraph("Q1 (25%)", th_style),
    Paragraph("Median (Q2)", th_style),
    Paragraph("Q3 (75%)", th_style),
    Paragraph("Max", th_style),
    Paragraph("Mean", th_style),
    Paragraph("Std Dev", th_style),
    Paragraph("IQR", th_style),
    Paragraph("Midrange", th_style),
    Paragraph("Skew", th_style)
]]

def fmt_num(val):
    if abs(val) >= 1e12:
        return f"${val/1e12:.2f}T"
    elif abs(val) >= 1e9:
        return f"${val/1e9:.2f}B"
    elif abs(val) >= 1e6:
        return f"${val/1e6:.2f}M"
    elif abs(val) >= 1000:
        return f"{val:,.1f}"
    else:
        return f"{val:.2f}"

for _, row in metrics_df.iterrows():
    f_name = row['Feature']
    table_data.append([
        Paragraph(f_name, tb_left),
        Paragraph(fmt_num(row['Min']), tb_style),
        Paragraph(fmt_num(row['Q1']), tb_style),
        Paragraph(fmt_num(row['Median']), tb_style),
        Paragraph(fmt_num(row['Q3']), tb_style),
        Paragraph(fmt_num(row['Max']), tb_style),
        Paragraph(fmt_num(row['Mean']), tb_style),
        Paragraph(fmt_num(row['Std']), tb_style),
        Paragraph(fmt_num(row['IQR']), tb_style),
        Paragraph(fmt_num(row['Midrange']), tb_style),
        Paragraph(f"{row['Skewness']:.2f}", tb_style)
    ])

col_widths = [1.8*cm, 1.2*cm, 1.4*cm, 1.5*cm, 1.4*cm, 1.5*cm, 1.4*cm, 1.4*cm, 1.4*cm, 1.6*cm, 1.0*cm]
t1 = Table(table_data, colWidths=col_widths, repeatRows=1)
t1.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
    ('TEXTCOLOR', (0,0), (-1,0), white),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [COLOR_BG_LIGHT, COLOR_CARD_BG]),
    ('GRID', (0,0), (-1,-1), 0.4, COLOR_LINE),
]))
story.append(t1)
story.append(Spacer(1, 8))

# Add Boxplots Image
fig1_file = os.path.join(PLOTS_DIR, "fig1_5num_summary_boxplots.png")
if os.path.exists(fig1_file):
    img1 = Image(fig1_file, width=17.2*cm, height=9.5*cm)
    story.append(img1)
    story.append(Spacer(1, 8))

# --- Section 3: Central Tendency Evaluation ---
story.append(Paragraph("3. Central Tendency Analysis: Midrange & Mode Evaluation", sec_title))
story.append(HRFlowable(width="100%", thickness=0.8, color=COLOR_LINE, spaceBefore=1, spaceAfter=5))

ct_text = (
    "In symmetric Gaussian distributions, Mean, Median, Mode, and Midrange converge to the same central value. "
    "However, financial data exhibits severe right-skewness, causing dramatic divergences:"
)
story.append(Paragraph(ct_text, body_style))

story.append(Paragraph("<b>1. Midrange Instability:</b> Midrange is computed as (Min + Max) / 2. Because it relies solely on extreme endpoints, a single mega-cap entity distorts the metric. For Total Revenue, the Median is $7.81 Billion while the Midrange is $243.05 Billion (a 31x overstatement). For Total Assets, Midrange reaches $1.285 Trillion versus a Median of $14.93 Billion.", bullet_style))
story.append(Paragraph("<b>2. Modal Price & Volume Patterns:</b> Discrete modes appear around standard corporate targets. Stock prices exhibit modes around $34.00 and $35.00 due to historical stock split management, while daily volume exhibits institutional block trading modes around 1,100,000 shares.", bullet_style))
story.append(Spacer(1, 6))

fig3_file = os.path.join(PLOTS_DIR, "fig3_skewness_distributions.png")
if os.path.exists(fig3_file):
    img3 = Image(fig3_file, width=16.5*cm, height=7.5*cm)
    story.append(img3)
    story.append(Spacer(1, 8))

# --- Section 4: Outlier Detection Comparison ---
story.append(Paragraph("4. Outlier Detection Method Comparison (Tukey IQR vs Z-Score)", sec_title))
story.append(HRFlowable(width="100%", thickness=0.8, color=COLOR_LINE, spaceBefore=1, spaceAfter=5))

outlier_intro = (
    "We compare two distinct outlier identification frameworks: "
    "<b>Tukey's IQR Method</b> (Quartile Rule: Q1 - 1.5 * IQR to Q3 + 1.5 * IQR) and "
    "the <b>Z-Score Method</b> (Standard 3-Sigma Rule: |x - Mean| / StdDev > 3.0)."
)
story.append(Paragraph(outlier_intro, body_style))

# Outlier Comparison Table
table2_data = [[
    Paragraph("Feature Name", th_style),
    Paragraph("Valid Records", th_style),
    Paragraph("Tukey Outliers", th_style),
    Paragraph("Tukey Outlier %", th_style),
    Paragraph("Z-Score Outliers", th_style),
    Paragraph("Z-Score Outlier %", th_style),
    Paragraph("Primary Cause of Disparity", th_style)
]]

for _, row in metrics_df.iterrows():
    f_name = row['Feature']
    cnt = f"{int(row['Count']):,}"
    iqr_c = f"{int(row['IQR_Outliers']):,}"
    iqr_p = f"{row['IQR_Outlier_%']:.2f}%"
    z_c = f"{int(row['Z_Outliers']):,}"
    z_p = f"{row['Z_Outlier_%']:.2f}%"
    
    if "close" in f_name or "open" in f_name or "high" in f_name or "low" in f_name:
        reason = "High-priced shares (e.g. Priceline > $1,000)"
    elif "volume" in f_name:
        reason = "Massive earnings-day volume surges"
    elif "Revenue" in f_name or "Assets" in f_name or "Liabilities" in f_name:
        reason = "Mega-cap conglomerates & money-center banks"
    else:
        reason = "Sector-specific financial leverage differences"
        
    table2_data.append([
        Paragraph(f_name, tb_left),
        Paragraph(cnt, tb_style),
        Paragraph(iqr_c, tb_style),
        Paragraph(f"<b>{iqr_p}</b>", tb_style),
        Paragraph(z_c, tb_style),
        Paragraph(f"<b>{z_p}</b>", tb_style),
        Paragraph(reason, tb_left)
    ])

col_widths2 = [2.2*cm, 1.8*cm, 1.8*cm, 1.8*cm, 1.8*cm, 1.8*cm, 5.0*cm]
t2 = Table(table2_data, colWidths=col_widths2, repeatRows=1)
t2.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), COLOR_SECONDARY),
    ('TEXTCOLOR', (0,0), (-1,0), white),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [COLOR_BG_LIGHT, COLOR_CARD_BG]),
    ('GRID', (0,0), (-1,-1), 0.4, COLOR_LINE),
]))
story.append(t2)
story.append(Spacer(1, 8))

fig2_file = os.path.join(PLOTS_DIR, "fig2_outlier_comparison.png")
if os.path.exists(fig2_file):
    img2 = Image(fig2_file, width=16.8*cm, height=8.0*cm)
    story.append(img2)
    story.append(Spacer(1, 8))

# --- Section 5: Practical Guidance ---
story.append(Paragraph("5. Practical Guidance & Domain Takeaways", sec_title))
story.append(HRFlowable(width="100%", thickness=0.8, color=COLOR_LINE, spaceBefore=1, spaceAfter=5))

guidance_text = (
    "<b>1. Why Z-Score Fails on Skewed Financial Data:</b> The Z-score method assumes Gaussian symmetry. In right-skewed data, extreme top-tier values inflate the sample standard deviation, pushing the 3-sigma fence artificially high and causing false negatives.<br/>"
    "<b>2. Why Tukey IQR is Superior:</b> Tukey's method uses rank-based quantiles (Q1 and Q3) with a 25% breakdown point. Upper-tail extreme values do not stretch the IQR width, ensuring consistent anomaly flagging.<br/>"
    "<b>3. Domain Reality (Anomalies vs Structural Heavyweights):</b> Outliers like Apple's Net Income or JPMorgan's Total Assets represent legitimate economic scale rather than data entry errors. They should be handled using robust scaling (RobustScaler, Log transform) rather than deletion."
)
story.append(Paragraph(guidance_text, body_style))
story.append(Spacer(1, 10))

# Sign-off block
signoff_table = Table([[
    Paragraph("<b>Report Verified & Authored By:</b><br/>Aryan Mori (24BCE119) & Shlok Vaishnav (24BCE135)<br/>Department of Computer Science & Engineering • Nirma University", info_style)
]], colWidths=[17.2*cm])
signoff_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), COLOR_CARD_BG),
    ('BOX', (0,0), (-1,-1), 1, COLOR_SECONDARY),
    ('PADDING', (0,0), (-1,-1), 6),
]))
story.append(signoff_table)

# Build Document
doc.build(story)
print(f"PDF Successfully Generated: {OUTPUT_PDF}")
