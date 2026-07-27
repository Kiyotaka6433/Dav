# PRACTICAL-2: DATA CLEANING, FEATURE SELECTION & ANOMALY AUDIT REPORT

**Pipeline Focus:** Feature Pruning, Collinearity Reduction, 90-Day Filing Lag Shift, Tukey IQR Audit & As-Of Merging  
**Subject:** Data Analysis & Visualization  
**Subject Code:** 2CS504CC23  

---

## 1. Executive Summary & Feature Pruning Rationale

Raw merged financial datasets are often bloated and computationally inefficient. The initial raw merge contained **92 columns**, dominated by redundant index identifiers, unadjusted raw prices, raw HTML URLs, and near-identical balance sheet sub-line items.

### Why 92 Columns Were Reduced to 34 Columns:
1. **Perfect Accounting Identity Collinearity ($r = 1.000$)**: `Total Liabilities & Equity` is mathematically identical to `Total Assets` (Accounting Equation: Assets = Liabilities + Equity). Retaining both introduces exact multicollinearity, causing linear models to fail due to singular matrix inversion.
2. **Near-Identical Net Income Line Items ($r > 0.995$)**: `Net Income Applicable to Common Shareholders`, `Net Income-Cont. Operations`, and `Earnings Before Tax` were near-100% correlated with `Net Income`.
3. **Granular Balance Sheet Sub-Line Items**: Attributes such as `Accounts Payable`, `Deferred Liability Charges`, and `Other Current Assets` exhibited extreme missingness (>40% nulls) and were subsumed under high-level aggregates (`Total Current Assets` and `Total Liabilities`).
4. **Redundant Identifiers**: Dropped `CIK`, `SEC filings` (raw URL strings), and index columns (`Unnamed: 0`).

By pruning these redundancies, we produced a clean, non-collinear dataset of **34 core attributes** (shape: `851,264 x 34`), reducing storage overhead and boosting model performance.

---

## 2. Detailed Pruning Matrix: Rationale for Deleted Columns

| Deleted Column Name | Raw Category | Statistical & Financial Deletion Rationale |
| :--- | :--- | :--- |
| **`Total Liabilities & Equity`** | Balance Sheet | Deleted due to exact collinearity ($r=1.000$). Accounting Identity: Total Assets = Total Liabilities + Equity. |
| **`Net Income Applicable to Shareholders`** | Income Stmt | Deleted due to near-100% correlation ($r=0.999$) with Net Income. |
| **`Net Income-Cont. Operations`** | Income Stmt | Deleted due to $r=0.999$ correlation with Net Income. |
| **`Earnings Before Interest & Tax (EBIT)`** | Income Stmt | Deleted due to $r=0.998$ correlation with Operating Income. |
| **`Deferred Asset Charges`** | Balance Sheet | Deleted due to 100% missing values (entirely null column). |
| **`Misc. Stocks / Other Assets`** | Balance Sheet | Deleted due to 91.6% missing values; subsumed under Total Current Assets. |
| **`Raw Open / Close / High / Low`** | Prices (Raw) | Deleted due to stock split cliff jumps; split-adjusted prices were kept. |
| **`CIK / SEC Filings / Unnamed: 0`** | Metadata | Deleted as non-informative numerical index and raw HTML URL strings. |

---

## 3. Analysis of Columns with High Missingness (Pruned Features)

| Raw Fundamentals Column | Missing Count | Missing (%) | Pruning Action & Rationale |
| :--- | :---: | :---: | :--- |
| **Deferred Asset Charges** | 1,781 | 100.0% | Pruned: Entirely empty in dataset. |
| **Misc. Stocks** | 1,632 | 91.6% | Pruned: Sparse line item, sub-category of Total Assets. |
| **Other Financing Activities** | 1,141 | 64.1% | Pruned: Subsumed under Net Cash Flow. |
| **Effect of Exchange Rate** | 984 | 55.2% | Pruned: Sector-specific multinational metric. |
| **Minority Interest** | 852 | 47.8% | Pruned: Subsumed under Total Liabilities. |
| **Accounts Payable** | 412 | 23.1% | Pruned: Subsumed under Total Liabilities. |

---

## 4. Correlation Analysis of Retained Features

To verify collinearity reduction, we evaluate the correlation matrix across key numerical financial features:

| Feature | `close` | `volume` | `Total Revenue` | `Net Income` | `Total Assets` | `Total Liabilities` | `Total Equity` | `EPS` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`close`** | **1.000** | -0.133 | 0.012 | 0.014 | -0.055 | -0.053 | -0.057 | 0.583 |
| **`volume`** | -0.133 | **1.000** | 0.286 | 0.386 | 0.445 | 0.422 | 0.541 | -0.068 |
| **`Total Revenue`** | 0.012 | 0.286 | **1.000** | 0.679 | 0.307 | 0.265 | 0.562 | 0.137 |
| **`Net Income`** | 0.014 | 0.386 | 0.679 | **1.000** | 0.464 | 0.418 | 0.714 | 0.341 |
| **`Total Assets`** | -0.055 | 0.445 | 0.307 | 0.464 | **1.000** | **0.997** | 0.862 | 0.023 |
| **`Total Liabilities`** | -0.053 | 0.422 | 0.265 | 0.418 | **0.997** | **1.000** | 0.823 | 0.015 |
| **`Total Equity`** | -0.057 | 0.541 | 0.562 | 0.714 | 0.862 | 0.823 | **1.000** | 0.079 |
| **`EPS`** | 0.583 | -0.068 | 0.137 | 0.341 | 0.023 | 0.015 | 0.079 | **1.000** |

**Observation:** `Total Assets` and `Total Liabilities` share a high correlation ($r = 0.997$) due to firm size scaling. However, both are retained as they represent distinct accounting dimensions (Asset Base vs Debt Obligation), whereas `Total Liabilities & Equity` ($r = 1.000$) was dropped.

---

## 5. Rigorous Data Quality, Tukey's IQR Rule & Anomaly Audit

To ensure robust data hygiene for quantitative modeling, we applied **Tukey's Interquartile Range (IQR) Rule** to detect outliers:

$$\text{Lower Bound} = Q_1 - 1.5 \times \text{IQR}, \quad \text{Upper Bound} = Q_3 + 1.5 \times \text{IQR} \quad (\text{where } \text{IQR} = Q_3 - Q_1)$$

### Tukey IQR Boundaries & Outlier Breakdown:

| Feature Name | Q1 (25%) | Q3 (75%) | IQR | Upper Bound | Outliers Count (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`close` ($)** | 31.29 | 75.14 | 43.85 | 140.91 | 51,585 (6.1%) |
| **`volume`** | 1.22M | 5.22M | 4.00M | 11.22M | 82,488 (9.7%) |
| **`Total Revenue` ($)** | 3.59B | 17.42B | 13.83B | 38.16B | 47,358 (12.4%) |
| **`Net Income` ($)** | 351.4M | 1.68B | 1.33B | 3.67B | 45,899 (12.1%) |
| **`Total Assets` ($)** | 6.44B | 35.96B | 29.52B | 80.23B | 42,932 (11.3%) |
| **`Earnings Per Share` ($)** | 1.60 | 4.57 | 2.97 | 9.03 | 22,693 (6.4%) |
| **`Est. Shares Outstanding`** | 149.3M | 546.0M | 396.7M | 1.14B | 39,160 (11.0%) |

### Specific Outlier Discoveries in Master CSV:
* **Price Outliers (51,585 rows, 6.1%)**: Driven by high-unit-price equities such as Booking Holdings ($P > \$1,500$), Google ($P > \$800$), and Chipotle ($P > \$600$).
* **Volume Outliers (82,488 rows, 9.7%)**: Caused by extreme single-session trading activity in high-liquidity stocks (Bank of America, Apple, Ford) reaching >850 Million shares.
* **Balance Sheet Megabanks (42,932 rows, 11.3%)**: Money-center financial institutions (JPMorgan Chase $\$2.57$ Trillion, Bank of America $\$2.18$ Trillion) create severe right-skewed balance sheet tails.
* **Revenue Leaders (47,358 rows, 12.4%)**: Mega-cap retail and energy giants (Walmart $\$486$ Billion, ExxonMobil $\$420$ Billion) exceed the $\$38.16\text{B}$ Tukey upper bound.

### 🚨 RAW SEC FILING ANOMALY AUDIT: NEGATIVE SHARES OUTSTANDING
* **Finding**: Identified **1,006 rows** where `Estimated Shares Outstanding` is negative (e.g. symbol **PRU** Prudential Financial on 2012-12-31 reporting **-1.083333 Billion shares**).
* **Root Cause**: Raw SEC 10-K filings compute shares via division: $\text{Net Income} / \text{Earnings Per Share}$. When Net Income or EPS have sign mismatches or treasury share adjustments, this quotient yields a negative share count.
* **Cleaning Solution**: In machine learning preprocessing, quantile trimming or filtering `Estimated Shares Outstanding > 0` safely cleans these 1,006 anomalous rows.

---

## 6. Accounting Filing Lag (90-Day Shift) & As-Of Merging

A primary error in financial modeling is merging quarterly accounting reports on their `Period Ending` dates. Company 10-K and 10-Q reports are filed with the SEC 60 to 90 days *after* the quarter ends.

### The 90-Day Shift Formula:
```python
fundamentals['lagged_date'] = fundamentals['Period Ending'] + pd.Timedelta(days=90)
```

### As-Of Chronological Join (Pandas):
We sort prices by `date` and fundamentals by `lagged_date`, then execute an as-of join matching each trading session date with the most recent lagged fundamental report where `lagged_date <= price_date`:
```python
prices_fund = pd.merge_asof(
    prices_sorted, 
    fund_sorted, 
    by='symbol', 
    left_on='date', 
    right_on='lagged_date', 
    direction='backward'
)
```

**Result:** Out of 851,264 daily price records, **380,845 records (44.74%)** successfully matched published fundamental filings with zero look-ahead leakage.

---

## 7. Target Class Balance (GICS Sector)

| GICS Sector Class | Company Count | Percentage (%) |
| :--- | :---: | :---: |
| **Consumer Discretionary** | 85 | 16.83% |
| **Industrials** | 69 | 13.66% |
| **Information Technology** | 68 | 13.47% |
| **Financials** | 64 | 12.67% |
| **Health Care** | 59 | 11.68% |
| **Consumer Staples** | 37 | 7.33% |
| **Energy** | 36 | 7.13% |
| **Real Estate** | 29 | 5.74% |
| **Utilities** | 28 | 5.54% |
| **Materials** | 25 | 4.95% |
| **Telecommunications Services** | 5 | 0.99% |

---

## 8. Five-Number Summaries of Retained Features

### A. Stock Price Columns (Split-Adjusted USD)

| Stat | Open ($) | Close ($) | Low ($) | High ($) | Volume (Shares) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Min** | 1.66 | 1.59 | 1.50 | 1.81 | 0 |
| **25% (Q1)** | 31.27 | 31.29 | 30.94 | 31.62 | 1,221,500 |
| **50% (Median)** | 48.46 | 48.48 | 47.97 | 48.96 | 2,476,250 |
| **75% (Q3)** | 75.12 | 75.14 | 74.40 | 75.85 | 5,222,500 |
| **Max** | 1,584.43 | 1,578.13 | 1,549.93 | 1,600.93 | 859,643,400 |

### B. Key Fundamental Metrics

| Stat | Total Revenue ($) | Gross Profit ($) | Net Income ($) | Total Assets ($) | EPS ($) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Min** | $1.51 \times 10^6$ | -$1.28 \times 10^9$ | -$2.35 \times 10^{10}$ | $2.71 \times 10^6$ | -61.20 |
| **25% (Q1)** | $3.71 \times 10^9$ | $1.58 \times 10^9$ | $3.53 \times 10^8$ | $6.55 \times 10^9$ | 1.59 |
| **50% (Median)** | $8.02 \times 10^9$ | $3.36 \times 10^9$ | $6.86 \times 10^8$ | $1.52 \times 10^{10}$ | 2.81 |
| **75% (Q3)** | $1.75 \times 10^{10}$ | $7.25 \times 10^9$ | $1.70 \times 10^9$ | $3.60 \times 10^{10}$ | 4.59 |
| **Max** | $4.86 \times 10^{11}$ | $1.48 \times 10^{11}$ | $5.34 \times 10^{10}$ | $2.57 \times 10^{12}$ | 50.09 |

---

## 9. Cleaning Code Documentation (`data_cleaning_and_merging.py`)

The full Python cleaning script is available at `C:\Users\aryan\dav\prac 2\data_cleaning_and_merging.py`:

```python
import os
import pandas as pd

RAW_DIR = r"C:\Users\aryan\OneDrive\Desktop\dav"
PRAC2_DIR = r"C:\Users\aryan\dav\prac 2"

# 1. Clean Securities & Drop Redundant Identifiers
sec_raw = pd.read_csv(os.path.join(RAW_DIR, "securities.csv"))
sec = sec_raw.rename(columns={"Ticker symbol": "symbol"}).drop(columns=["CIK", "SEC filings"], errors="ignore")
sec = sec.dropna(subset=["GICS Sector", "GICS Sub Industry"])

# 2. Select 25 High-Signal Fundamentals Attributes & Apply 90-Day Lag
fund_raw = pd.read_csv(os.path.join(RAW_DIR, "fundamentals.csv"))
fund = fund_raw[SELECTED_25_COLS].rename(columns={"Ticker Symbol": "symbol"})
fund["Period Ending"] = pd.to_datetime(fund["Period Ending"], format="%d-%m-%Y")
fund["lagged_date"] = fund["Period Ending"] + pd.Timedelta(days=90)

# 3. Clean Prices & Drop Duplicates
prices_raw = pd.read_csv(os.path.join(RAW_DIR, "prices-split-adjusted.csv"))
prices = prices_raw.copy()
prices["date"] = pd.to_datetime(prices["date"], format="%d-%m-%Y")
prices = prices.drop_duplicates(subset=["date", "symbol"])

# 4. Chronological As-Of Join (Prices + Lagged Fundamentals)
prices_fund = pd.merge_asof(
    prices.sort_values("date"), 
    fund.sort_values("lagged_date"),
    by="symbol", 
    left_on="date", 
    right_on="lagged_date", 
    direction="backward"
)

# 5. Merge Sector Metadata
master_df = pd.merge(prices_fund, sec[["symbol", "Security", "GICS Sector", "GICS Sub Industry"]], on="symbol", how="inner")
master_df.to_csv(os.path.join(PRAC2_DIR, "master_dataset_pruned.csv"), index=False)
```

---

## 10. Tukey's IQR Outlier Treatment & Machine Learning Summary

### Summary of Tukey Outlier Treatment for Machine Learning:
1. **Quantile Trimming / Filtering**: Filtering rows where `Estimated Shares Outstanding <= 0` eliminates the 1,006 anomalous SEC division rows without altering valid market data.
2. **Winsorization (Percentile Capping at 1st and 99th Percentiles)**: Financial features like trading volume and revenue exhibit extreme leptokurtic fat tails (Kurtosis > 40-300). Capping extreme upper values at $Q_3 + 1.5 \times \text{IQR}$ prevents numerical instability during regression gradient descent while preserving 99%+ of structural variation.
3. **Model Suitability**: Linear models (OLS, Ridge, Lasso) require Winsorized/trimmed features to satisfy homoscedasticity assumptions. Non-parametric tree models (Random Forest, XGBoost) natively handle heavy tails.
