from pathlib import Path
import pandas as pd

CLEANED_DATA_PATH = Path("data/cleaned/fashion_retail_cleaned.csv")
OUTPUT_DIR = Path("data/cleaned")

def create_category_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby("Product Category")
        .agg(
            Purchases=("Item Purchased", "count"),
            Total_Sales_USD=("Purchase Amount", "sum"),
            Average_Purchase_USD=("Purchase Amount", "mean"),
            Average_Rating=("Review Rating", "mean")
        )
        .reset_index()
    )
    summary["Total_Sales_USD"] = summary["Total_Sales_USD"].round(0).astype(int)
    summary["Average_Purchase_USD"] = summary["Average_Purchase_USD"].round(1)
    summary["Average_Rating"] = summary["Average_Rating"].round(1)
    return summary.sort_values("Purchases", ascending=False)

def create_monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Month"] = df["Date Purchase"].dt.to_period("M").astype(str)
    return df.groupby("Month").size().reset_index(name="Purchase_Count")

def create_top_items(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    return (
        df.groupby("Item Purchased")["Purchase Amount"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
        .rename(columns={"Purchase Amount": "Total_Purchase_Amount_USD"})
    )

def create_payment_distribution(df: pd.DataFrame) -> pd.DataFrame:
    counts = df["Payment Method"].value_counts().reset_index()
    counts.columns = ["Payment Method", "Transactions"]
    counts["Percentage"] = (counts["Transactions"] / counts["Transactions"].sum() * 100).round(2)
    return counts

def run_eda():
    df = pd.read_csv(CLEANED_DATA_PATH)
    df["Date Purchase"] = pd.to_datetime(df["Date Purchase"])

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    category_summary = create_category_summary(df)
    monthly_trend = create_monthly_trend(df)
    top_items = create_top_items(df)
    payment_distribution = create_payment_distribution(df)

    category_summary.to_csv(OUTPUT_DIR / "category_summary.csv", index=False)
    monthly_trend.to_csv(OUTPUT_DIR / "monthly_purchase_trend.csv", index=False)
    top_items.to_csv(OUTPUT_DIR / "top10_items_by_purchase_amount.csv", index=False)
    payment_distribution.to_csv(OUTPUT_DIR / "payment_method_distribution.csv", index=False)

    return category_summary, monthly_trend, top_items, payment_distribution

if __name__ == "__main__":
    run_eda()
    print("EDA tables created.")
