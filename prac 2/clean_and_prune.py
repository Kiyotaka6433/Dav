import os
import pandas as pd
import numpy as np

# File paths
RAW_DIR = r"C:\Users\aryan\OneDrive\Desktop\dav"
PRAC2_DIR = r"C:\Users\aryan\dav\prac 2"

os.makedirs(PRAC2_DIR, exist_ok=True)

print("Starting Data Cleaning, Feature Pruning & Merging...")

# Load raw files
sec_raw = pd.read_csv(os.path.join(RAW_DIR, "securities.csv"))
fund_raw = pd.read_csv(os.path.join(RAW_DIR, "fundamentals.csv"))
prices_raw = pd.read_csv(os.path.join(RAW_DIR, "prices-split-adjusted.csv"))

# 1. Clean Securities
print("\n--- Cleaning Securities ---")
sec = sec_raw.copy()
sec = sec.rename(columns={"Ticker symbol": "symbol"})
sec = sec.drop(columns=["CIK", "SEC filings"], errors="ignore")
sec = sec.dropna(subset=["GICS Sector", "GICS Sub Industry"])
print(f"Securities cleaned shape: {sec.shape}")

# 2. Select High-Signal Columns from Fundamentals (Pruning Collinearity & Redundancy)
SELECTED_FUND_COLS = [
    "Ticker Symbol", "Period Ending",
    # Income Statement
    "Total Revenue", "Cost of Revenue", "Gross Profit", "Operating Income", 
    "Net Income", "Research and Development",
    # Balance Sheet
    "Cash and Cash Equivalents", "Net Receivables", "Inventory", 
    "Total Current Assets", "Total Assets", "Total Liabilities", "Total Equity",
    # Ratios & Metrics
    "Gross Margin", "Operating Margin", "Pre-Tax Margin", 
    "Current Ratio", "Quick Ratio", "Earnings Per Share",
    # Cash Flow & Shares
    "Estimated Shares Outstanding", "Net Cash Flow-Operating", "Capital Expenditures"
]

# Verify columns exist
SELECTED_FUND_COLS = [c for c in SELECTED_FUND_COLS if c in fund_raw.columns]
fund = fund_raw[SELECTED_FUND_COLS].copy()
fund = fund.rename(columns={"Ticker Symbol": "symbol"})

# Parse dates and apply 90-day filing lag
fund["Period Ending"] = pd.to_datetime(fund["Period Ending"], format="%d-%m-%Y")
fund["lagged_date"] = fund["Period Ending"] + pd.Timedelta(days=90)

print(f"Fundamentals pruned shape: {fund.shape} ({len(fund.columns)} columns)")

# 3. Clean Prices
print("\n--- Cleaning Prices ---")
prices = prices_raw.copy()
prices["date"] = pd.to_datetime(prices["date"], format="%d-%m-%Y")
prices = prices.drop_duplicates(subset=["date", "symbol"])
print(f"Prices cleaned shape: {prices.shape}")

# 4. Perform As-Of Join (Prices + Lagged Fundamentals)
print("\n--- Performing Chronological As-Of Join ---")
prices_sorted = prices.sort_values(by="date")
fund_sorted = fund.sort_values(by="lagged_date")

prices_fund = pd.merge_asof(
    prices_sorted,
    fund_sorted,
    by="symbol",
    left_on="date",
    right_on="lagged_date",
    direction="backward"
)

# 5. Merge with Securities Metadata
master_df = pd.merge(prices_fund, sec[["symbol", "Security", "GICS Sector", "GICS Sub Industry"]], on="symbol", how="inner")

print(f"\nFinal Merged Master Dataset Shape: {master_df.shape} ({len(master_df.columns)} columns)")
print("\nMaster Dataset Columns (Total 33):")
for i, col in enumerate(master_df.columns, 1):
    print(f" {i:2d}. {col}")

# Save pruned merged CSV
output_csv_path = os.path.join(PRAC2_DIR, "master_dataset_pruned.csv")
master_df.to_csv(output_csv_path, index=False)
print(f"\nSaved pruned master CSV to: {output_csv_path}")

# Print Correlation Matrix of Key Financial Features to verify collinearity reduction
num_cols = ["close", "volume", "Total Revenue", "Net Income", "Total Assets", "Total Liabilities", "Total Equity", "Earnings Per Share"]
num_cols = [c for c in num_cols if c in master_df.columns]
corr = master_df[num_cols].corr()
print("\nCorrelation Matrix of Selected Financial Features:")
print(corr.round(3).to_string())
