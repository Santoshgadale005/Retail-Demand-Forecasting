# 🛒 Retail Demand Forecasting & Inventory Optimization

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![BigQuery](https://img.shields.io/badge/Google-BigQuery-4285F4.svg)](https://cloud.google.com/bigquery)
[![dbt](https://img.shields.io/badge/dbt-Data%20Build%20Tool-FF694B.svg)](https://www.getdbt.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Project Overview

An end-to-end analytics platform that forecasts future product demand using historical sales data, promotional events, seasonality, and pricing information. The platform helps inventory managers optimize stock levels, reduce stockouts, minimize overstocking, and improve supply chain efficiency.

## 🎯 Objectives

- **Demand Forecasting**: Predict future product demand using time-series models (Prophet, ARIMA, LightGBM)
- **Inventory Optimization**: Recommend optimal stock levels based on forecasted demand
- **Stockout Reduction**: Identify products at risk of stockout and trigger reorder alerts
- **Overstocking Prevention**: Minimize excess inventory carrying costs
- **What-If Analysis**: Enable scenario-based planning for promotions and pricing changes
- **Interactive Dashboard**: Provide real-time insights via Streamlit dashboard

## 📊 Dataset

**M5 Forecasting Dataset** — Walmart historical sales data from Kaggle

| Component | Description |
|-----------|-------------|
| `sales_train_validation.csv` | Daily unit sales per product per store (1,913 days) |
| `sales_train_evaluation.csv` | Extended sales data with additional 28 days |
| `calendar.csv` | Date features, events, and SNAP eligibility |
| `sell_prices.csv` | Weekly selling prices per product per store |
| `sample_submission.csv` | Submission format for forecasting |

**Hierarchy**: State → Store → Category → Department → Product

## 🏗️ Architecture

```
M5 Dataset (Kaggle)
        ↓
Python ETL Pipeline
        ↓
Google BigQuery (Raw Layer)
        ↓
dbt Transformations (Staging → Intermediate → Marts)
        ↓
Clean Data Warehouse (Star Schema)
        ↓
Facebook Prophet / ARIMA / LightGBM
        ↓
Forecast Outputs → BigQuery
        ↓
Streamlit Dashboard
        ↓
Inventory Optimization Recommendations
```

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| **Language** | Python 3.10+ |
| **Database** | SQL, Google BigQuery |
| **Data Warehouse** | Google BigQuery |
| **Transformations** | dbt (Data Build Tool) |
| **Forecasting** | Facebook Prophet, ARIMA, LightGBM |
| **Dashboard** | Streamlit |
| **Visualization** | Plotly, Matplotlib |
| **Version Control** | Git & GitHub |
| **Environment** | Virtual Environment (venv) |
| **Configuration** | python-dotenv |

## 📁 Project Structure

```
retail-demand-forecasting/
│
├── data/
│   ├── raw/                    # Original M5 dataset files
│   ├── processed/              # Cleaned and transformed data
│   └── external/               # External datasets (holidays, economic data)
│
├── notebooks/                  # Jupyter notebooks for EDA and prototyping
├── warehouse/                  # BigQuery schema definitions and SQL scripts
├── dbt_project/                # dbt models, tests, and documentation
│
├── forecasting/
│   ├── prophet/                # Facebook Prophet models
│   ├── arima/                  # ARIMA/SARIMA models
│   └── lightgbm/              # LightGBM gradient boosting models
│
├── inventory/                  # Inventory optimization logic
├── streamlit/                  # Streamlit dashboard application
├── reports/                    # Generated analysis reports
├── dashboards/                 # Dashboard configurations
├── deployment/                 # Deployment scripts and configs
├── docker/                     # Docker containerization files
├── docs/                       # Project documentation
├── tests/                      # Unit and integration tests
├── configs/                    # Configuration files
│
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not committed)
├── .gitignore                  # Git ignore rules
├── main.py                     # Main application entry point
└── README.md                   # Project documentation
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.10 or higher
- Google Cloud Platform account with BigQuery enabled
- Git installed

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/retail-demand-forecasting.git
cd retail-demand-forecasting
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Google Cloud Configuration
GCP_PROJECT_ID=your-gcp-project-id
GCP_CREDENTIALS_PATH=path/to/service-account-key.json
BQ_DATASET=retail_forecasting
BQ_LOCATION=US

# Kaggle Configuration
KAGGLE_USERNAME=your-kaggle-username
KAGGLE_KEY=your-kaggle-api-key
```

### 5. Set Up Google Cloud

```bash
gcloud auth application-default login
gcloud config set project your-gcp-project-id
```

### 6. Verify Setup

```bash
python main.py --verify
```

## 📅 Development Timeline

| Week | Focus Area |
|------|-----------|
| **Week 1** | Project setup, data ingestion, EDA |
| **Week 2** | Data warehouse design, dbt transformations |
| **Week 3** | Forecasting models (Prophet, ARIMA, LightGBM) |
| **Week 4** | Inventory optimization, Streamlit dashboard, deployment |

## 📈 Key Features

- **Automated ETL Pipelines**: Python-based data ingestion from M5 dataset to BigQuery
- **Data Warehouse**: Star schema design with fact and dimension tables in BigQuery
- **dbt Transformations**: Modular SQL transformations with testing and documentation
- **Multi-Model Forecasting**: Ensemble approach using Prophet, ARIMA, and LightGBM
- **Inventory Optimization**: Safety stock, reorder point, and EOQ calculations
- **Interactive Dashboard**: Real-time Streamlit dashboard with filters and drill-downs
- **What-If Analysis**: Scenario planning for pricing and promotional strategies
- **Comprehensive Documentation**: Full project documentation and code comments

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## 📬 Contact

**Santosh Gadale**

- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

---

⭐ If you found this project useful, please give it a star!
