# Data Analysis & Visualization (DAV) - S&P 500 Analytics Pipeline

**Authors:** Aryan Mori (24BCE119) & Shlok Vaishnav (24BCE135)  
**Subject:** Data Analysis & Visualization  
**Subject Code:** 2CS504CC23  
**Institution:** Nirma University • B.Tech CSE (Semester-IV)  

---

## 📌 Repository Overview

This repository contains the end-to-end Data Analysis and Visualization (DAV) coursework project and practical submissions analyzing historical **S&P 500 market pricing and corporate fundamental metrics**.

The primary goal of this repository is to build a mathematically rigorous quantitative pipeline that eliminates **statistical look-ahead bias**, handles **collinearity**, prunes high-dimensional financial features, and provides deep insights into corporate health and market return predictors.

---

## 📁 Repository Structure

```text
├── prac 1/
│   ├── project_proposal_report.md     # Full Practical 1 Project Proposal Report
│   ├── project_proposal_report.pdf    # Formatted PDF Version of Practical 1 Proposal
│   └── generate_proposal_pdf.py      # Automated ReportLab PDF generator script
│
├── prac 2/
│   ├── data_cleaning_and_feature_selection_report.md  # Detailed Practical 2 Technical Report
│   ├── data_cleaning_and_feature_selection_report.pdf # Formatted PDF Version of Practical 2 Report
│   ├── clean_and_prune.py              # Feature pruning, collinearity & 90-day filing lag script
│   ├── data_cleaning_and_merging.py    # Raw dataset merging & initial data cleaning script
│   ├── generate_prac2_pdf.py           # Automated ReportLab PDF generator script with plots
│   └── plots/                          # Generated high-resolution diagnostic visualizations
│       ├── fig1_collinearity.png
│       ├── fig2_missingness.png
│       ├── fig3_reduction.png
│       ├── fig4_sector_balance.png
│       ├── fig5_asof_timeline.png
│       ├── fig6_retained_corr.png
│       └── fig7_tukey_iqr_outliers.png
│
├── .gitignore
└── README.md
```

---

## 📊 Practical Summaries

### Practical 1: Project Proposal Report
* **Topic:** S&P 500 Financial & Fundamental Market Analytics using Open Financial Data
* **Scope:** Analyzes stock pricing sessions, trading volumes, balance sheets, income statements, cash flows, and GICS industry sector classifications.
* **Objectives:** Define problem statement, risk evaluation, feature dimensionality reduction targets, and machine learning roadmap.

### Practical 2: Data Cleaning, Feature Selection & Anomaly Audit
* **Key Pipeline Operations:**
  1. **Dimensionality Reduction:** Reduced raw merged dataset from **92 columns to 34 core attributes**, eliminating redundant index columns and sub-line items.
  2. **Collinearity Elimination:** Removed exact accounting equation duplicates ($r = 1.000$) such as `Total Liabilities & Equity` $\equiv$ `Total Assets`, and near-100% correlated income metrics ($r > 0.995$).
  3. **90-Day Filing Lag Shift:** Applied a strict +90 calendar day temporal shift on corporate fundamental announcement dates before merging with daily stock pricing using `pd.merge_asof()`, resolving statistical look-ahead data leakage.
  4. **Tukey IQR Anomaly Audit:** Identified extreme structural financial outliers in metrics like `Net Income` and `Total Assets` caused by mega-cap market capitalization disparities.

---

## 📜 Authors & Credits
* **Aryan Mori** (24BCE119)
* **Shlok Vaishnav** (24BCE135)
