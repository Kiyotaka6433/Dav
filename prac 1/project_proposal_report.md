# DATA ANALYTICS & VISUALIZATION PROJECT REPORT

**Name:** Aryan Mori & Shlok Vaishnav  
**Roll No:** 24BCE119 & 24BCE135  
**Subject:** Data Analysis and Visualization  

## Project Title
**S&P 500 Financial & Fundamental Market Analytics using Open Financial Data**

---

## 1. Introduction
The rapid growth of algorithmic trading and quantitative finance has increased the demand for robust financial data analysis pipelines. Governments, regulatory bodies, and financial institutions rely heavily on accurate market datasets to monitor corporate health, evaluate systemic risk, and maintain fair capital markets.

The objective of this project is to analyze S&P 500 market pricing and corporate fundamental session data collected from open financial data portals. The dataset contains comprehensive information about stock pricing sessions, trading volumes, corporate balance sheets, income statements, cash flows, and GICS industry sector classifications. This analysis helps understand market behavior, corporate financial stability, and pricing efficiency.

The project aims to discover hidden patterns in corporate performance, identify market risks, eliminate look-ahead data leakage, and develop predictive models that support strategic portfolio planning and quantitative decision-making.

---

## 2. Problem Statement
With the increasing complexity of financial markets, historical data modeling faces severe technical challenges including look-ahead bias, stock split distortions, extreme class imbalance across industry sectors, and high feature collinearity. Improper data processing leads to flawed backtests, poor portfolio risk management, and failed predictive models.

The challenge is to clean, prune, and analyze financial market data to answer key questions such as:
* Which GICS sectors and sub-industries generate the highest revenue and net income?
* How do corporate fundamental metrics impact daily stock price volatility and returns?
* What factors cause high collinearity between balance sheet line items?
* Can corporate filing lag (90-day window) be modeled without leaking future financial knowledge?
* Can stock returns and sector classifications be accurately predicted using quantitative algorithms?

---

## 3. Objectives
The main objectives of this project are:
* Analyze S&P 500 stock pricing and fundamental financial performance patterns.
* Eliminate statistical look-ahead bias by enforcing a strict 90-day accounting filing lag.
* Reduce feature dimensionality by pruning collinear and redundant balance sheet attributes (from 92 columns to 34 key features).
* Compare financial metrics across GICS industry sectors.
* Predict stock price returns and sector classifications using machine learning models.
* Provide actionable quantitative recommendations for portfolio managers and quantitative analysts.

---

## 4. Dataset Description
The dataset consists of S&P 500 corporate financial records and daily trading sessions collected from open financial data platforms. The raw dataset originally contained over 851,000 price records and 1,780 fundamental quarterly filings across 92 attributes. Through feature selection and collinearity reduction, an optimized subset of **34 core attributes** was retained.

### Selected Key Dataset Attributes (30 Key Fields):

| Attribute | Category | Description & Rationale |
| :--- | :--- | :--- |
| `symbol` | Metadata Key | Unique ticker identifier for cross-table joins. |
| `Security` | Metadata | Official corporate company name. |
| `GICS Sector` | Target Label | Broad industry classification (11 primary sectors). |
| `GICS Sub Industry` | Metadata | Granular industry sub-category. |
| `date` | Timestamp | Daily stock trading session date. |
| `Period Ending` | Timestamp | Accounting report period end date. |
| `lagged_date` | Timestamp | Public filing date shifted by 90 days to prevent look-ahead bias. |
| `open` | Price (USD) | Split-adjusted opening market price. |
| `high` | Price (USD) | Split-adjusted highest intra-day price. |
| `low` | Price (USD) | Split-adjusted lowest intra-day price. |
| `close` | Price (USD) | Split-adjusted closing market price. |
| `volume` | Trading Vol | Total number of shares traded during session. |
| `Total Revenue` | Income Stmt | Total gross top-line corporate revenue. |
| `Cost of Revenue` | Income Stmt | Direct cost of goods and services sold. |
| `Gross Profit` | Income Stmt | Gross earnings before operating overhead. |
| `Operating Income` | Income Stmt | Core operational earnings (EBIT). |
| `Net Income` | Income Stmt | Bottom-line net profit after tax and interest. |
| `Research & Development` | Income Stmt | Total corporate R&D investment expenditure. |
| `Cash & Equivalents` | Balance Sheet | Highly liquid cash reserves. |
| `Net Receivables` | Balance Sheet | Outstanding customer payments owed. |
| `Inventory` | Balance Sheet | Valuation of unsold goods and materials. |
| `Total Current Assets` | Balance Sheet | Assets convertible to cash within 12 months. |
| `Total Assets` | Balance Sheet | Total corporate balance sheet asset valuation. |
| `Total Liabilities` | Balance Sheet | Total corporate debt and financial obligations. |
| `Total Equity` | Balance Sheet | Net book value of shareholder equity. |
| `Gross Margin` | Ratio | Percentage of revenue retained after direct costs. |
| `Operating Margin` | Ratio | Core operational efficiency margin percentage. |
| `Current Ratio` | Ratio | Short-term liquidity ratio (Current Assets / Liabilities). |
| `Earnings Per Share` | Metric | Net profit divided by total share count (EPS). |
| `Estimated Shares Out` | Shares | Total number of common shares outstanding. |

---

## 5. Stakeholders
The findings of this project are valuable for multiple key stakeholders across finance and technology:
* **Quantitative Analysts (Quants):** Build leak-free algorithmic trading models and backtest quantitative factors.
* **Portfolio Managers:** Monitor sector exposure risk and optimize asset allocation across GICS industries.
* **Corporate Finance Officers:** Benchmark operational efficiency, profit margins, and debt leverage against sector peers.
* **Data Engineers:** Automate clean ETL ingestion pipelines while handling missingness and date alignment.
* **Individual / Retail Investors:** Access clean financial ratio summaries to identify undervalued equities.
* **Academic Researchers:** Study market efficiency, leptokurtic distribution shapes, and factor predictability.

---

## 6. Business Problem
The project addresses the following critical business and analytical questions:
* Which GICS sectors demonstrate the highest profit margins and revenue growth?
* Which balance sheet line items cause severe collinearity ($r > 0.99$) and require pruning?
* What is the impact of accounting filing lag (90 days) on signal accuracy?
* Which financial ratios best predict stock price volatility and returns?
* Can machine learning models accurately classify company industry sectors based on balance sheet metrics?

---

## 7. Data Preprocessing Plan
The following preprocessing steps are executed:
* Standardize ticker symbol keys across Securities, Fundamentals, and Prices.
* Remove redundant index columns (e.g. `Unnamed: 0`, `CIK`, `SEC filings`).
* Enforce a strict 90-day accounting filing lag (`lagged_date = Period Ending + 90 days`).
* Prune collinear features ($r > 0.95$, such as dropping Total Liabilities & Equity in favor of Total Assets).
* Execute an as-of join (`pd.merge_asof`) to match daily prices with the latest public fundamental records.
* Preserve numeric nulls to prevent premature imputation bias.

---

## 8. Exploratory Data Analysis
The planned exploratory visualizations include:
* GICS Sector classwise balance distribution analysis.
* Missing value percentage distribution across fundamental metrics.
* Historical split-adjusted price trajectories for major tickers.
* Daily active trading ticker volume timelines.
* Correlation matrix heatmaps evaluating collinearity among balance sheet metrics.

---

## 9. Machine Learning Opportunities
* **Regression (Predict Stock Returns & Close Prices):** Linear Regression, Ridge/Lasso, Random Forest Regressor, XGBoost Regressor.
* **Classification (Predict GICS Sector Category):** Logistic Regression, Decision Trees, Random Forest Classifier, Support Vector Machines.
* **Clustering (Group Similar Corporate Profiles):** K-Means Clustering, DBSCAN, Hierarchical Clustering.
* **Time Series Forecasting (Predict Market Demand & Prices):** ARIMA, Prophet, LSTM Neural Networks.

---

## 10. Key Performance Indicators (KPIs)
* Total Market Revenue & Net Income
* Average Gross & Operating Margins per Sector
* Current Ratio & Quick Ratio Liquidity Standards
* Annualized Price Volatility & Sharpe Ratio
* Model Mean Absolute Error (MAE) & Root Mean Squared Error (RMSE)
* Classification F1-Score & Accuracy across Sectors

---

## 11. Proposed Visualizations
* Line Charts (Historical price trends & active ticker timelines)
* Bar Charts (Sector counts & missing value percentages)
* Correlation Heatmaps (Feature collinearity evaluation)
* Box Plots (Spread of financial ratios across industries)
* Interactive Dashboards & KPI Cards

---

## 12. Expected Outcomes
* Establish a clean, leak-free financial dataset pruned of collinear features.
* Identify high-performing GICS sectors and corporate profit drivers.
* Accurately predict stock returns without look-ahead bias.
* Provide quantitative insights to assist portfolio managers in risk optimization.

---

## 13. Tools and Technologies
* **Languages & Environments:** Python 3.13, Jupyter Notebook
* **Data Processing:** Pandas, NumPy
* **Visualization:** Matplotlib, Seaborn
* **Machine Learning:** Scikit-Learn, XGBoost
* **Reporting:** ReportLab PDF Engine

---

## 14. Future Scope & Theme
* Live API integration for real-time stock pricing.
* Automated sentiment analysis of SEC 10-K text filings using NLP.
* Deep learning (LSTM / Transformer) real-time return forecasting.

**Overall Project Theme:**  
*"Data-driven quantitative analysis of S&P 500 corporate fundamentals and stock pricing to eliminate data leakage, prune collinearity, optimize portfolio risk, and support sustainable investment decision-making."*
