# PRACTICAL-3: COMPREHENSIVE 5-NUMBER SUMMARY, CENTRAL TENDENCY & OUTLIER COMPARISON REPORT

**Authors:** Aryan Mori (24BCE119) & Shlok Vaishnav (24BCE135)  
**Subject:** Data Analysis & Visualization  
**Subject Code:** 2CS504CC23  
**Institution:** Nirma University • B.Tech CSE (Semester-IV)  

---

## 1. Executive Summary & Audit Purpose

Following the feature pruning and filing-lag temporal alignment performed in Practical 2, this report presents a thorough exploratory analysis of the cleaned S&P 500 dataset (**34 attributes, 851,264 records**). 

The primary objective of Practical 3 is to evaluate the underlying distribution of core financial metrics and stock trading variables. Specifically, we compute robust non-parametric summary statistics (the **5-Number Summary**), evaluate measures of central tendency (**Mean, Median, Mode, Midrange**), measure dispersion (**Standard Deviation, Interquartile Range**), and perform a head-to-head comparison between **Tukey's IQR Method** and the **Z-Score Method** for outlier identification.

### Key Audit Findings:
1. **Extreme Right Skewness across Financial Financials**: Metrics like `Total Revenue`, `Total Assets`, and `Volume` display positive skewness ranging from +5.20 to +13.13. As a result, the sample Mean is consistently pulled far to the right of the Median.
2. **Midrange Distortions**: The Midrange statistic, defined as `(Min + Max) / 2`, proves highly unstable for financial data. For `Total Assets`, the Midrange is **$1.285 Trillion**, whereas the Median is only **$14.93 Billion**—a distortion factor of over 86x caused by mega-cap financial institutions.
3. **Outlier Method Sensitivity**: 
   - **Tukey's IQR Method** flags **6.06% to 12.43%** of data points as outliers because its boundaries are anchored to quartile widths.
   - **Z-Score Method (|Z| > 3.0)** flags only **1.30% to 2.27%** of data points because the sample standard deviation is inflated by heavy tails, artificially stretching the 3-sigma thresholds.

---

## 2. Comprehensive 5-Number Summaries & Descriptive Statistics

The 5-Number Summary consists of the Minimum ($Min$), First Quartile ($Q_1$), Median ($Q_2$), Third Quartile ($Q_3$), and Maximum ($Max$). Together with the Mean, Standard Deviation ($\sigma$), Interquartile Range ($IQR = Q_3 - Q_1$), Mode, and Midrange, it provides a complete picture of distribution spread and asymmetry.

### Table 1: Complete 5-Number Summary & Extended Descriptive Statistics

| Feature Name | Minimum (Min) | 25th Percentile (Q1) | Median (Q2) | 75th Percentile (Q3) | Maximum (Max) | Sample Mean | Std Dev (σ) | IQR | Midrange | Skewness |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Close Price ($)** | $1.59 | $31.29 | $48.48 | $75.14 | $1,578.13 | $65.01 | $75.20 | $43.85 | $789.86 | +7.24 |
| **Open Price ($)** | $1.66 | $31.27 | $48.46 | $75.12 | $1,584.44 | $64.99 | $75.20 | $43.85 | $793.05 | +7.24 |
| **High Price ($)** | $1.81 | $31.62 | $48.96 | $75.85 | $1,600.93 | $65.64 | $75.91 | $44.23 | $801.37 | +7.24 |
| **Low Price ($)** | $1.50 | $30.94 | $47.97 | $74.40 | $1,549.94 | $64.34 | $74.46 | $43.46 | $775.72 | +7.24 |
| **Volume (Shares)** | 0 | 1,221,500 | 2,476,250 | 5,222,500 | 859,643,400 | 5,415,113 | 12,494,681 | 4,001,000 | 429,821,700 | +13.13 |
| **Total Revenue ($)** | $99.64M | $3.59B | $7.81B | $17.42B | $486.00B | $20.16B | $41.48B | $13.83B | $243.05B | +6.31 |
| **Gross Profit ($)** | -$12.65B | $1.56B | $2.91B | $6.89B | $149.00B | $7.19B | $13.90B | $5.34B | $68.18B | +5.20 |
| **Operating Income ($)** | -$27.91B | $525.86M | $1.01B | $2.20B | $71.23B | $2.26B | $5.04B | $1.67B | $21.66B | +5.64 |
| **Net Income ($)** | -$23.53B | $351.40M | $673.00M | $1.68B | $53.39B | $1.71B | $3.99B | $1.33B | $14.93B | +5.49 |
| **Total Assets ($)** | $216.90M | $6.44B | $14.93B | $35.96B | $2,570.00B | $57.81B | $213.19B | $29.52B | $1,285.11B | +8.44 |
| **Total Liabilities ($)**| $232.00M | $3.74B | $8.78B | $23.72B | $2,340.00B | $45.70B | $190.77B | $19.98B | $1,170.12B | +8.61 |
| **Total Equity ($)** | -$13.24B | $2.21B | $4.94B | $10.81B | $256.00B | $12.10B | $26.67B | $8.60B | $121.38B | +5.70 |
| **Earnings Per Share ($)**| -$61.20 | $1.60 | $2.82 | $4.57 | $50.09 | $3.37 | $4.55 | $2.97 | -$5.56 | +0.74 |

---

## 3. Central Tendency Analysis: Midrange & Mode Evaluation

When analyzing financial time-series data, selecting the correct measure of central tendency is critical. The three standard statistics—Mean, Median, and Mode—behave differently depending on distribution shape, while the Midrange provides a structural baseline.

### 3.1 Midrange Sensitivity
The Midrange is calculated as:
$$\text{Midrange} = \frac{\text{Minimum} + \text{Maximum}}{2}$$

In Gaussian distributions, the Midrange converges toward the Mean and Median. However, in financial datasets, extreme upper values severely distort the Midrange:
- **`Total Revenue`**: The Median is **$7.81 Billion**, whereas the Midrange is **$243.05 Billion** (driven by retail giants like Walmart).
- **`Total Assets`**: The Median is **$14.93 Billion**, whereas the Midrange is **$1,285.11 Billion** (driven by mega-cap commercial banks like JPMorgan Chase).

**Conclusion**: Midrange should **never** be used as a representative central metric for financial datasets due to its zero breakdown point (a single outlier completely shifts the value).

### 3.2 Modal Value Behavior
For continuous variables like stock price and volume, true continuous modes are sparse. However, rounding prices to standard cent intervals reveals prominent empirical modes:
- **Stock Prices (`close`, `open`)**: The modal price level sits around **$35.00** and **$34.00**, reflecting typical stock split target ranges where management historically maintains share prices to ensure retail trading liquidity.
- **`Volume`**: The modal trading volume cluster is **1,100,000 shares**, representing baseline institutional block trading activity on average liquidity market days.

---

## 4. Outlier Detection Method Comparison: Tukey IQR vs Z-Score

To evaluate anomalies and heavy-tailed observations, we compare two widely established outlier detection techniques:
1. **Tukey's IQR Method (Quartile Rule)**: Non-parametric method using interquartile range.
   - Lower Bound = $Q_1 - 1.5 \times IQR$
   - Upper Bound = $Q_3 + 1.5 \times IQR$
2. **Z-Score Method (3-Sigma Rule)**: Parametric method assuming approximate Gaussian normality.
   - Threshold = $\left| \frac{x - \mu}{\sigma} \right| > 3.0$

### Table 2: Comparative Outlier Detection Results

| Feature Name | Total Valid Records | Tukey IQR Outlier Count | Tukey IQR Outlier % | Z-Score Outlier Count | Z-Score Outlier % | Primary Cause of Disparity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`close`** | 851,264 | 51,585 | **6.06%** | 12,945 | **1.52%** | High price tail (Priceline/Google shares > $750) |
| **`volume`** | 851,264 | 82,488 | **9.69%** | 11,076 | **1.30%** | Massive volume spikes during earnings announcements |
| **`Total Revenue`** | 380,845 | 47,358 | **12.43%** | 6,247 | **1.64%** | Mega-cap conglomerates vs mid-cap S&P 500 firms |
| **`Gross Profit`** | 380,845 | 38,997 | **10.24%** | 8,446 | **2.22%** | High margin technology sector companies |
| **`Operating Income`**| 380,845 | 44,152 | **11.59%** | 8,270 | **2.17%** | Extreme operating leverage in energy & tech |
| **`Net Income`** | 380,845 | 45,899 | **12.05%** | 8,656 | **2.27%** | One-time non-operating charges and gains |
| **`Total Assets`** | 380,845 | 42,932 | **11.27%** | 5,688 | **1.49%** | Multi-trillion asset scale of money-center banks |
| **`Total Equity`** | 380,845 | 36,860 | **9.68%** | 7,647 | **2.01%** | Capital intensive manufacturing balance sheets |

---

## 5. Statistical Interpretation & Practical Guidance

### 5.1 Why Z-Score Under-Reports Financial Outliers
The Z-score method assumes that data follows a symmetric normal distribution. In the presence of heavy-tailed, right-skewed data:
1. Extremely large values artificially inflate the sample standard deviation ($\sigma$).
2. The inflated $\sigma$ pushes the upper boundary ($\mu + 3\sigma$) to extreme heights.
3. Consequently, many legitimate structural anomalies fall below the $3\sigma$ threshold and pass undetected (false negatives).

### 5.2 Why Tukey's IQR Method is Preferred for Financial Pipelines
Tukey's IQR method is **non-parametric** and relies strictly on rank statistics ($Q_1$ and $Q_3$), which have a 25% breakdown point. Extreme values in the upper 5% of the data do not expand the IQR width. Thus, Tukey's method maintains a stable threshold and accurately captures structural sector differences.

### 5.3 Domain Context: Anomalies vs. Structural Heavyweights
In financial analytics, outliers flagged by Tukey's method (e.g. Apple's Net Income or JPMorgan's Total Assets) are **not data entry errors**. They represent structural economic realities of S&P 500 capitalization weights. Therefore:
- Outliers should **not** be deleted arbitrarily.
- Non-linear tree algorithms (Random Forest, XGBoost) or robust scaling transforms (RobustScaler, Log1p) should be applied prior to model training.

---

## 6. Author Sign-Off & Verification

This report and its accompanying numerical summaries were generated from `master_dataset_pruned.csv` and verified using `prac 3/generate_prac3_analysis.py`.

**Aryan Mori** (24BCE119) & **Shlok Vaishnav** (24BCE135)  
*Department of Computer Science and Engineering, Nirma University*
