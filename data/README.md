# Retail Demand Forecasting — Data Documentation

## Raw Data (`data/raw/`)
M5 Forecasting dataset files downloaded from Kaggle.
These files should NOT be committed to Git (they are in .gitignore).

### Expected Files:
- `sales_train_validation.csv` — Daily unit sales (30,490 products × 1,913 days)
- `sales_train_evaluation.csv` — Extended sales with additional 28 days
- `calendar.csv` — Date features, events, SNAP eligibility
- `sell_prices.csv` — Weekly selling prices per product/store
- `sample_submission.csv` — Kaggle submission format

## Processed Data (`data/processed/`)
Cleaned and transformed datasets ready for analysis and modeling.

## External Data (`data/external/`)
Supplementary data sources (e.g., economic indicators, weather data).
