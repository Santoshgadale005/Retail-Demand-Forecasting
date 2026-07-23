import pandas as pd


def load_sales_data():
    sales = pd.read_csv("data/raw/sales_train_validation.csv")
    return sales


def create_daily_sales(sales):
    day_columns = [col for col in sales.columns if col.startswith("d_")]

    daily_sales = sales[day_columns].sum().reset_index()
    daily_sales.columns = ["day", "sales"]

    return daily_sales


def create_features(df):
    """
    Create lag and rolling features.
    """

    # Convert d_1 -> 1
    df["day_number"] = df["day"].str.replace("d_", "").astype(int)

    # Lag Features
    df["lag_1"] = df["sales"].shift(1)
    df["lag_7"] = df["sales"].shift(7)
    df["lag_28"] = df["sales"].shift(28)

    # Rolling Mean Features
    df["rolling_mean_7"] = df["sales"].rolling(7).mean()
    df["rolling_mean_28"] = df["sales"].rolling(28).mean()

    # Remove missing values
    df.dropna(inplace=True)

    print("=" * 50)
    print("Feature Engineering Completed")
    print("=" * 50)

    print(df.head())

    print("\nShape :", df.shape)

    return df


if __name__ == "__main__":
    sales = load_sales_data()

    daily_sales = create_daily_sales(sales)

    feature_data = create_features(daily_sales)