import pandas as pd
import plotly.express as px
from pathlib import Path


# --- Settings: update paths if needed ---
DATA_DIR = Path(__file__).parent / 'sample_data'
PRESENT_CSV = DATA_DIR / 'present.csv' # rename your export to this
FUTURE_CSV = DATA_DIR / 'future.csv' # rename your export to this
OUT_XLSX = Path(__file__).parent / 'aggregated.xlsx'
OUT_PNG_PRESENT = Path(__file__).parent / 'aggregate_present.png'
OUT_PNG_FUTURE = Path(__file__).parent / 'aggregate_future.png'


# --- Load & tidy ---
def load_csv(path):
df = pd.read_csv(path)
# Expect columns from Formspree submission
# a_public_safety, b_civil_liberties, c_accountability, plot_id
# Coerce to floats and normalise to sum=1 (just in case)
for col in ['a_public_safety','b_civil_liberties','c_accountability']:
df[col] = pd.to_numeric(df[col], errors='coerce')
df = df.dropna(subset=['a_public_safety','b_civil_liberties','c_accountability'])
S = df[['a_public_safety','b_civil_liberties','c_accountability']].sum(axis=1)
df['A'] = df['a_public_safety'] / S
df['B'] = df['b_civil_liberties'] / S
df['C'] = df['c_accountability'] / S
return df


present = load_csv(PRESENT_CSV)
future = load_csv(FUTURE_CSV)


# --- Save Excel workbook ---
with pd.ExcelWriter(OUT_XLSX) as xw:
present[['A','B','C']].to_excel(xw, sheet_name='present', index=False)
future[['A','B','C']].to_excel(xw, sheet_name='future_2075', index=False)
print(f"Wrote {OUT_XLSX}")


# --- Plot aggregates (scatter_ternary) ---
fig_p = px.scatter_ternary(present, a='A', b='B', c='C', title='Aggregate — Today', opacity=0.85)
fig_f = px.scatter_ternary(future, a='A', b='B', c='C', title='Aggregate — 2075', opacity=0.85)


# Export to PNG (needs kaleido)
fig_p.write_image(OUT_PNG_PRESENT, scale=2)
fig_f.write_image(OUT_PNG_FUTURE, scale=2)
print(f"Saved {OUT_PNG_PRESENT} and {OUT_PNG_FUTURE}")Commit new file
✓ Commit directly to the main branch.
Commit message (required):
[ add aggregate.py ]
