from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

IMAGE_DIR = Path("images")
IMAGE_DIR.mkdir(exist_ok=True)

def save_purchase_frequency_chart(score_df):
    df = score_df.sort_values("Purchases", ascending=True)
    plt.figure(figsize=(10, 6))
    plt.barh(df["Product Category"], df["Purchases"])
    plt.title("Purchase Frequency by Product Category")
    plt.xlabel("Purchase Frequency")
    plt.tight_layout()
    plt.savefig(IMAGE_DIR / "purchase_frequency_by_category.png", dpi=300)
    plt.close()

def save_market_score_chart(score_df):
    df = score_df.sort_values("Taiwan_Market_Potential_Score", ascending=True)
    plt.figure(figsize=(10, 6))
    plt.barh(df["Product Category"], df["Taiwan_Market_Potential_Score"])
    plt.title("Taiwan Market Potential Score by Category")
    plt.xlabel("Taiwan Market Potential Score")
    plt.tight_layout()
    plt.savefig(IMAGE_DIR / "taiwan_market_potential_score.png", dpi=300)
    plt.close()

def save_monthly_trend_chart(monthly_df):
    plt.figure(figsize=(10, 6))
    plt.plot(monthly_df["Month"], monthly_df["Purchase_Count"], marker="o")
    plt.title("Monthly Purchase Trend")
    plt.xlabel("Month")
    plt.ylabel("Purchase Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(IMAGE_DIR / "monthly_purchase_trend.png", dpi=300)
    plt.close()

def save_top_items_chart(top_items_df):
    df = top_items_df.sort_values("Total_Purchase_Amount_USD", ascending=True)
    plt.figure(figsize=(10, 6))
    plt.barh(df["Item Purchased"], df["Total_Purchase_Amount_USD"])
    plt.title("Top 10 Items by Total Purchase Amount")
    plt.xlabel("Total Purchase Amount (USD)")
    plt.tight_layout()
    plt.savefig(IMAGE_DIR / "top10_items_by_total_purchase_amount.png", dpi=300)
    plt.close()

def save_payment_chart(payment_df):
    plt.figure(figsize=(7, 5))
    plt.bar(payment_df["Payment Method"], payment_df["Transactions"])
    plt.title("Payment Method Distribution")
    plt.xlabel("Payment Method")
    plt.ylabel("Number of Transactions")
    plt.tight_layout()
    plt.savefig(IMAGE_DIR / "payment_method_distribution.png", dpi=300)
    plt.close()

def run_visualizations():
    score_df = pd.read_csv("data/cleaned/taiwan_market_potential_score.csv")
    monthly_df = pd.read_csv("data/cleaned/monthly_purchase_trend.csv")
    top_items_df = pd.read_csv("data/cleaned/top10_items_by_purchase_amount.csv")
    payment_df = pd.read_csv("data/cleaned/payment_method_distribution.csv")

    save_purchase_frequency_chart(score_df)
    save_market_score_chart(score_df)
    save_monthly_trend_chart(monthly_df)
    save_top_items_chart(top_items_df)
    save_payment_chart(payment_df)

if __name__ == "__main__":
    run_visualizations()
    print("Visualizations created.")
