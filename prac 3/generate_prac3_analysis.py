import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Paths
PRAC2_CSV = r"C:\Users\aryan\dav\prac 2\master_dataset_pruned.csv"
PRAC3_DIR = r"C:\Users\aryan\dav\prac 3"
PLOTS_DIR = os.path.join(PRAC3_DIR, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

print("=== Starting Practical 3 Analysis Pipeline ===")
print(f"Loading dataset from: {PRAC2_CSV}")

df = pd.read_csv(PRAC2_CSV)
print(f"Dataset Loaded. Shape: {df.shape}")

# Define key numerical columns for deep statistical audit
num_cols = [
    'close', 'open', 'high', 'low', 'volume',
    'Total Revenue', 'Gross Profit', 'Operating Income', 'Net Income',
    'Total Assets', 'Total Liabilities', 'Total Equity',
    'Cash and Cash Equivalents', 'Earnings Per Share', 'Current Ratio'
]

# Filter existing columns
num_cols = [col for col in num_cols if col in df.columns]

# Color Palette: Strictly Earth Tones
# No Blue, No Purple
EARTH_SADDLE_BROWN = "#5D3A1A"
EARTH_TERRACOTTA   = "#B85B35"
EARTH_OLIVE        = "#4A5D4E"
EARTH_SAND         = "#F4EBE1"
EARTH_BG           = "#FDFBF7"
EARTH_CHARCOAL     = "#2B2523"
EARTH_CLAY         = "#D97724"

sns.set_theme(style="whitegrid")
plt.rcParams.update({
    "font.size": 9.5,
    "axes.labelsize": 10.5,
    "axes.titlesize": 12,
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5,
    "figure.titlesize": 14,
    "figure.dpi": 200,
    "figure.facecolor": EARTH_BG,
    "axes.facecolor": EARTH_BG,
    "text.color": EARTH_CHARCOAL,
    "axes.labelcolor": EARTH_CHARCOAL,
    "xtick.color": EARTH_CHARCOAL,
    "ytick.color": EARTH_CHARCOAL
})

stats_summary = []

for col in num_cols:
    series = df[col].dropna()
    if len(series) == 0:
        continue
    
    # 5-Number Summary
    qmin = series.min()
    q1 = series.quantile(0.25)
    median = series.median()
    q3 = series.quantile(0.75)
    qmax = series.max()
    
    # Central Tendency & Dispersion
    mean_val = series.mean()
    std_val = series.std()
    iqr_val = q3 - q1
    midrange = (qmin + qmax) / 2.0
    skewness = series.skew()
    
    # Mode estimation (for continuous data, round to 2 decimals or find modal bin)
    rounded_series = series.round(2)
    mode_vals = rounded_series.mode()
    mode_val = mode_vals.iloc[0] if len(mode_vals) > 0 else np.nan
    
    # Outlier Method 1: Tukey's IQR Method
    iqr_lower = q1 - 1.5 * iqr_val
    iqr_upper = q3 + 1.5 * iqr_val
    iqr_outliers = series[(series < iqr_lower) | (series > iqr_upper)]
    iqr_count = len(iqr_outliers)
    iqr_pct = (iqr_count / len(series)) * 100.0
    
    # Outlier Method 2: Z-Score Method (|Z| > 3)
    if std_val > 0:
        z_scores = np.abs((series - mean_val) / std_val)
        z_outliers = series[z_scores > 3.0]
        z_count = len(z_outliers)
        z_pct = (z_count / len(series)) * 100.0
    else:
        z_count = 0
        z_pct = 0.0
        
    stats_summary.append({
        'Feature': col,
        'Count': len(series),
        'Min': qmin,
        'Q1': q1,
        'Median': median,
        'Q3': q3,
        'Max': qmax,
        'Mean': mean_val,
        'Std': std_val,
        'IQR': iqr_val,
        'Midrange': midrange,
        'Mode': mode_val,
        'Skewness': skewness,
        'IQR_Outliers': iqr_count,
        'IQR_Outlier_%': iqr_pct,
        'Z_Outliers': z_count,
        'Z_Outlier_%': z_pct
    })

summary_df = pd.DataFrame(stats_summary)
summary_csv_path = os.path.join(PRAC3_DIR, "prac3_summary_metrics.csv")
summary_df.to_csv(summary_csv_path, index=False)
print(f"Summary metrics exported to: {summary_csv_path}")

# Print tabular preview
print("\n--- 5-NUMBER SUMMARY & OUTLIER COMPARISON PREVIEW ---")
print(summary_df[['Feature', 'Min', 'Q1', 'Median', 'Q3', 'Max', 'IQR_Outlier_%', 'Z_Outlier_%']].to_string(index=False))

# --- PLOT 1: Earth-Tone Boxplots for 5-Number Summary Visualization ---
fig, axes = plt.subplots(2, 2, figsize=(11, 7.5))
plot_cols = ['close', 'volume', 'Total Revenue', 'Net Income']

for ax, col in zip(axes.flatten(), plot_cols):
    if col in df.columns:
        s = df[col].dropna()
        # Draw boxplot using Earth Tones
        bp = ax.boxplot(s, vert=False, patch_artist=True,
                        boxprops=dict(facecolor=EARTH_SAND, color=EARTH_SADDLE_BROWN, linewidth=1.5),
                        whiskerprops=dict(color=EARTH_TERRACOTTA, linewidth=1.5),
                        capprops=dict(color=EARTH_SADDLE_BROWN, linewidth=1.5),
                        medianprops=dict(color=EARTH_CLAY, linewidth=2.0),
                        flierprops=dict(marker='o', markerfacecolor=EARTH_TERRACOTTA, markeredgecolor='none', markersize=3, alpha=0.4))
        ax.set_title(f"5-Number Summary & Outliers: {col}", color=EARTH_SADDLE_BROWN, fontweight='bold')
        ax.set_yticks([])
        
        # Annotate 5-number summary points
        qmin, q1, med, q3, qmax = s.min(), s.quantile(0.25), s.median(), s.quantile(0.75), s.max()
        ax.set_xlabel(f"Min: {qmin:,.1f} | Q1: {q1:,.1f} | Med: {med:,.1f} | Q3: {q3:,.1f} | Max: {qmax:,.1f}", fontsize=8)

plt.suptitle("Figure 1: Earth-Tone Boxplot Distribution & 5-Number Summaries", color=EARTH_SADDLE_BROWN, fontsize=13, fontweight='bold', y=0.98)
plt.tight_layout()
fig1_path = os.path.join(PLOTS_DIR, "fig1_5num_summary_boxplots.png")
plt.savefig(fig1_path, dpi=200, bbox_inches='tight')
plt.close()
print(f"Saved: {fig1_path}")

# --- PLOT 2: Outlier Method Comparison (Tukey IQR vs Z-Score) ---
fig, ax = plt.subplots(figsize=(10, 5))
sub_df = summary_df.head(10)
x = np.arange(len(sub_df))
width = 0.35

rects1 = ax.bar(x - width/2, sub_df['IQR_Outlier_%'], width, label='Tukey IQR Method (Quartile)', color=EARTH_TERRACOTTA)
rects2 = ax.bar(x + width/2, sub_df['Z_Outlier_%'], width, label='Z-Score Method (|Z| > 3)', color=EARTH_OLIVE)

ax.set_ylabel('Outlier Percentage (%)', color=EARTH_SADDLE_BROWN, fontweight='bold')
ax.set_title('Figure 2: Outlier Detection Method Comparison (IQR vs Z-Score)', color=EARTH_SADDLE_BROWN, fontweight='bold', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(sub_df['Feature'], rotation=35, ha='right')
ax.legend(frameon=True, facecolor=EARTH_BG)

for rect in rects1:
    height = rect.get_height()
    ax.annotate(f'{height:.1f}%', xy=(rect.get_x() + rect.get_width()/2, height),
                xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=7.5)

for rect in rects2:
    height = rect.get_height()
    ax.annotate(f'{height:.1f}%', xy=(rect.get_x() + rect.get_width()/2, height),
                xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=7.5)

plt.tight_layout()
fig2_path = os.path.join(PLOTS_DIR, "fig2_outlier_comparison.png")
plt.savefig(fig2_path, dpi=200, bbox_inches='tight')
plt.close()
print(f"Saved: {fig2_path}")

# --- PLOT 3: Skewness vs Midrange & Mean Disparities ---
fig, ax = plt.subplots(figsize=(9, 4.5))
skew_sorted = summary_df.sort_values(by='Skewness', ascending=False).head(8)
ax.barh(skew_sorted['Feature'], skew_sorted['Skewness'], color=EARTH_CLAY, edgecolor=EARTH_SADDLE_BROWN)
ax.set_xlabel('Fisher-Pearson Skewness Coefficient', color=EARTH_SADDLE_BROWN, fontweight='bold')
ax.set_title('Figure 3: Feature Distribution Skewness Impacting Central Tendency', color=EARTH_SADDLE_BROWN, fontweight='bold')

for i, v in enumerate(skew_sorted['Skewness']):
    ax.text(v + 0.1, i, f"{v:.2f}", va='center', fontsize=8.5, fontweight='bold', color=EARTH_SADDLE_BROWN)

plt.tight_layout()
fig3_path = os.path.join(PLOTS_DIR, "fig3_skewness_distributions.png")
plt.savefig(fig3_path, dpi=200, bbox_inches='tight')
plt.close()
print(f"Saved: {fig3_path}")

print("=== Practical 3 Analysis Pipeline Complete ===")
