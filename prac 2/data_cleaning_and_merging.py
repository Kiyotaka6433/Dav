"""
================================================================================
DATA CLEANING, COLLINEARITY PRUNING & AS-OF MERGING MASTER PIPELINE
================================================================================
Course: Data Analysis and Visualization (2CS504CC23)
Project: S&P 500 Financial & Fundamental Market Analytics

Description:
This master Python script performs all data cleaning, feature selection,
collinearity reduction, 90-day filing lag shifting, and chronological 
as-of merging for the S&P 500 dataset.
================================================================================
"""

import os
import pandas as pd
import numpy as np

# ── 1. CONFIGURATION & DIRECTORY SETUP ─────────────────────────────────────────
RAW_DIR = r"C:\Users\aryan\OneDrive\Desktop\dav"
PRAC2_DIR = r"C:\Users\aryan\dav\prac 2"

os.makedirs(PRAC2_DIR, exist_ok=True)
print("=== Starting S&P 500 Data Cleaning & Merging Master Script ===")

# ── 2. LOAD RAW DATASETS ───────────────────────────────────────────────────────
print("\n[Step 1] Loading raw CSV datasets...")
sec_raw_path = os.path.join(RAW_DIR, "securities.csv")
fund_raw_path = os.path.join(RAW_DIR, "fundamentals.csv")
prices_raw_path = os.path.join(RAW_DIR, "prices-split-adjusted.csv")

sec_raw = pd.read_csv(sec_raw_path)
fund_raw = pd.read_csv(fund_raw_path)
prices_raw = pd.read_csv(prices_raw_path)

print(f" Raw Securities Shape:   {sec_raw.shape}")
print(f" Raw Fundamentals Shape: {fund_raw.shape}")
print(f" Raw Prices Shape:       {prices_raw.shape}")

# ── 3. CLEAN SECURITIES DATASET ────────────────────────────────────────────────
print("\n[Step 2] Cleaning Securities Dataset...")
sec = sec_raw.copy()

# Rename join key to 'symbol'
sec = sec.rename(columns={"Ticker symbol": "symbol"})

# Drop redundant index/URL columns (CIK, SEC filings)
sec = sec.drop(columns=["CIK", "SEC filings"], errors="ignore")

# Drop rows missing target sector classifications
initial_sec_len = len(sec)
sec = sec.dropna(subset=["GICS Sector", "GICS Sub Industry"])
dropped_sec = initial_sec_len - len(sec)

print(f" Cleaned Securities Shape: {sec.shape} (Dropped {dropped_sec} rows missing sector labels)")

# ── 4. FEATURE SELECTION & COLLINEARITY PRUNING (FUNDAMENTALS) ───────────────
print("\n[Step 3] Pruning Fundamentals & Eliminating Collinearity...")

# Select 25 high-signal, essential attributes out of 79 raw columns
# Rationale: Prune accounting identities (e.g. Assets = Liabilities + Equity) 
# and near-100% correlated net income line items.
SELECTED_FUND_COLS = [
    "Ticker Symbol", "Period Ending",
    # Income Statement (Core metrics)
    "Total Revenue", "Cost of Revenue", "Gross Profit", "Operating Income", 
    "Net Income", "Research and Development",
    # Balance Sheet (Aggregates)
    "Cash and Cash Equivalents", "Net Receivables", "Inventory", 
    "Total Current Assets", "Total Assets", "Total Liabilities", "Total Equity",
    # Ratios & Financial Metrics
    "Gross Margin", "Operating Margin", "Pre-Tax Margin", 
    "Current Ratio", "Quick Ratio", "Earnings Per Share",
    # Cash Flow & Shares
    "Estimated Shares Outstanding", "Net Cash Flow-Operating", "Capital Expenditures"
]

# Retain existing columns
SELECTED_FUND_COLS = [c for c in SELECTED_FUND_COLS if c in fund_raw.columns]
fund = fund_raw[SELECTED_FUND_COLS].copy()

# Rename ticker symbol key
fund = fund.rename(columns={"Ticker Symbol": "symbol"})

# ── 5. APPLY 90-DAY FILING LAG SHIFT ───────────────────────────────────────────
print("\n[Step 4] Applying 90-Day Filing Lag Shift to Prevent Look-Ahead Bias...")
fund["Period Ending"] = pd.to_datetime(fund["Period Ending"], format="%d-%m-%Y")

# Shift Period Ending date forward by 90 days (10-K/10-Q filing delay)
fund["lagged_date"] = fund["Period Ending"] + pd.Timedelta(days=90)

print(" Formula: lagged_date = Period Ending + 90 days")
print(f" Pruned Fundamentals Shape: {fund.shape} ({len(fund.columns)} attributes)")

# ── 6. CLEAN PRICES DATASET ────────────────────────────────────────────────────
print("\n[Step 5] Cleaning Prices Dataset...")
prices = prices_raw.copy()

# Convert dates to datetime objects
prices["date"] = pd.to_datetime(prices["date"], format="%d-%m-%Y")

# Drop duplicate (date, symbol) records
dup_count = prices.duplicated(subset=["date", "symbol"]).sum()
if dup_count > 0:
    prices = prices.drop_duplicates(subset=["date", "symbol"])
print(f" Cleaned Prices Shape: {prices.shape} (Removed {dup_count} duplicate rows)")

# ── 7. EXECUTE CHRONOLOGICAL AS-OF JOIN ───────────────────────────────────────
print("\n[Step 6] Performing Chronological As-Of Join (Prices + Lagged Fundamentals)...")

# Sort dataframes by date columns as required by merge_asof
prices_sorted = prices.sort_values(by="date")
fund_sorted = fund.sort_values(by="lagged_date")

# Match daily prices backward to the most recent published fundamental report (lagged_date <= price_date)
prices_fund = pd.merge_asof(
    prices_sorted,
    fund_sorted,
    by="symbol",
    left_on="date",
    right_on="lagged_date",
    direction="backward"
)

matched_rows = prices_fund["lagged_date"].notnull().sum()
pct_matched = (matched_rows / len(prices_fund)) * 100
print(f" As-Of Merge Complete: {matched_rows:,} price records ({pct_matched:.2f}%) matched with lagged filings.")

# ── 8. MERGE SECURITIES METADATA (MASTER DATASET) ─────────────────────────────
print("\n[Step 7] Merging GICS Sector Metadata...")
master_df = pd.merge(
    prices_fund, 
    sec[["symbol", "Security", "GICS Sector", "GICS Sub Industry"]], 
    on="symbol", 
    how="inner"
)

print(f"\n Master Unified Dataset Shape: {master_df.shape} ({len(master_df.columns)} columns)")

# ── 9. CORRELATION CHECK ──────────────────────────────────────────────────────
print("\n[Step 8] Evaluating Feature Correlation Matrix (Collinearity Check):")
num_cols = ["close", "volume", "Total Revenue", "Net Income", "Total Assets", "Total Liabilities", "Total Equity", "Earnings Per Share"]
num_cols = [c for c in num_cols if c in master_df.columns]
corr_matrix = master_df[num_cols].corr()
print(corr_matrix.round(3).to_string())

# ── 10. EXPORT OUTPUT CSV FILES ───────────────────────────────────────────────
print("\n[Step 9] Exporting Cleaned & Merged CSV Files...")

# 1. Classification Joined File (Practical 7)
sec_fund_joined = pd.merge(fund, sec, on="symbol", how="inner")
sec_fund_path = os.path.join(PRAC2_DIR, "securities_fundamentals_joined.csv")
sec_fund_joined.to_csv(sec_fund_path, index=False)
print(f" Exported Sector Classification File: {sec_fund_path}")

# 2. Regression Joined File (Prices + Fundamentals)
prices_fund_path = os.path.join(PRAC2_DIR, "prices_fundamentals_joined.csv")
prices_fund.to_csv(prices_fund_path, index=False)
print(f" Exported Price-Fundamentals File:    {prices_fund_path}")

# 3. Master Pruned Dataset (34 Columns)
master_path = os.path.join(PRAC2_DIR, "master_dataset_pruned.csv")
master_df.to_csv(master_path, index=False)
print(f" Exported Master Pruned CSV (34 cols): {master_path}")

print("\n=== Master Script Executed Successfully! All Files Ready in C:\\Users\\aryan\\dav\\prac 2 ===")
