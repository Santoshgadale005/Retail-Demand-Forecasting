# 🏆 Production Forecast Model Comparison & Selection Report

Evaluating final hyperparameter-tuned model metrics over 30-day time-series evaluation windows.

## 📊 Performance Metrics

| Model | MAE | RMSE | MAPE (%) | Training Time (s) | Inference Time (s) | Memory (MB) |
|---|---|---|---|---|---|---|
| **Prophet** | 1902.75 | 2344.56 | 10.33% | 0.06s | 0.09s | 15.1 MB |
| **ARIMA (SARIMAX)** | 1772.87 | 2226.35 | 9.52% | 0.82s | 0.00s | 0.3 MB |
| **LightGBM** | 1957.87 | 2327.16 | 10.52% | 0.11s | 0.00s | 2.1 MB |

## 🎯 Model Selection Decision

The selected production model is **ARIMA (SARIMAX)**.

### Key Criteria:
1. **Accuracy**: Achieved lowest overall MAE (1772.87) and RMSE (2226.35).
2. **Speed**: Sub-second execution for rapid real-time dashboard updates.
3. **Scalability**: Handles exogenous features (promotions, price changes, calendar events) gracefully.
