# CSV Datasets

This folder contains the core dataset files for the DAV project:

| File | Size | Location / Description |
|---|---|---|
| `securities.csv` | ~60 KB | S&P 500 company info, tickers, sectors, and industries |
| `fundamentals.csv` | ~1.15 MB | Annual fundamental financial metrics and balance sheet data |
| `prices-split-adjusted.csv` | ~51 MB | Daily historical stock prices split-adjusted |
| `original_merged_uncleaned.csv` | ~470 MB | Raw uncleaned merged dataset available in [GitHub Release v1.0.0](https://github.com/Kiyotaka6433/Dav/releases/tag/v1.0.0) |

## Note on Large Files (>100MB)
GitHub restricts committing files larger than 100MB directly to repository git trees.
`original_merged_uncleaned.csv` (~470MB) is hosted directly on GitHub as an asset in [Release v1.0.0](https://github.com/Kiyotaka6433/Dav/releases/tag/v1.0.0). You can download it directly from the release page or place it locally in this `csvs/` directory.
