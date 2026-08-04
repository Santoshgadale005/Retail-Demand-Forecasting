import os
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("reports", exist_ok=True)

def generate_comparison():
    print("Comparing Prophet and ARIMA forecasting models...")
    
    prophet_metrics_path = "data/processed/metrics_prophet.csv"
    arima_metrics_path = "data/processed/metrics_arima.csv"
    
    if not os.path.exists(prophet_metrics_path) or not os.path.exists(arima_metrics_path):
        print("Missing evaluation metrics files. Make sure to run both training pipelines first.")
        return

    prophet_df = pd.read_csv(prophet_metrics_path)
    arima_df = pd.read_csv(arima_metrics_path)
    
    comparison_df = pd.concat([prophet_df, arima_df], ignore_index=True)
    
    # Select baseline
    best_model = comparison_df.loc[comparison_df['mae'].idxmin()]['model']
    
    # Generate Markdown Table
    comparison_md = f"""# Forecast Model Performance & Comparison

Evaluating performance metrics between Prophet and ARIMA model predictions over a 30-day forecast horizon.

| Metric | Prophet | ARIMA |
|---|---|---|
| **MAE** | {comparison_df.loc[0, 'mae']:.2f} | {comparison_df.loc[1, 'mae']:.2f} |
| **RMSE** | {comparison_df.loc[0, 'rmse']:.2f} | {comparison_df.loc[1, 'rmse']:.2f} |
| **MAPE (%)** | {comparison_df.loc[0, 'mape']:.2f}% | {comparison_df.loc[1, 'mape']:.2f}% |
| **Training Time (s)** | {comparison_df.loc[0, 'training_time']:.2f}s | {comparison_df.loc[1, 'training_time']:.2f}s |
| **Inference Time (s)** | {comparison_df.loc[0, 'prediction_time']:.2f}s | {comparison_df.loc[1, 'prediction_time']:.2f}s |

## Conclusion and Model Selection

The baseline model chosen for downstream predictions is **{best_model}**, based on its lower Mean Absolute Error (MAE). 

### Analysis Notes:
- **Prophet:** Performs robustly in capturing holidays and structural trend changes, making it ideal for retail campaigns.
- **ARIMA (SARIMAX):** Excels in capturing strict linear seasonal dependencies but can be computationally slower on large histories due to recursive parameter estimates.
"""

    with open("reports/model_comparison.md", "w") as f:
        f.write(comparison_md)
    print("Saved comparison table to reports/model_comparison.md")

    # Generate combined comparison chart
    plt.figure(figsize=(10, 5))
    metrics_to_plot = ['mae', 'rmse']
    x_labels = ['Prophet', 'ARIMA']
    
    plt.bar([0.8, 1.8], [comparison_df.loc[0, 'mae'], comparison_df.loc[1, 'mae']], width=0.4, label='MAE', color='teal')
    plt.bar([1.2, 2.2], [comparison_df.loc[0, 'rmse'], comparison_df.loc[1, 'rmse']], width=0.4, label='RMSE', color='orange')
    plt.xticks([1, 2], x_labels)
    plt.title("Error Comparison: Prophet vs ARIMA")
    plt.ylabel("Error Value")
    plt.legend()
    plt.tight_layout()
    plt.savefig("reports/figures/model_comparison.png")
    plt.close()
    print("Saved combined comparison chart to reports/figures/model_comparison.png")

if __name__ == "__main__":
    generate_comparison()
