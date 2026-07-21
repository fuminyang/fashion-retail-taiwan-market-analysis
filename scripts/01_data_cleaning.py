from pathlib import Path
import pandas as pd

RAW_DATA_PATH = Path("data/raw/fashion_retail_sales.csv")
CLEANED_DATA_PATH = Path("data/cleaned/fashion_retail_cleaned.csv")
SUMMARY_PATH = Path("data/cleaned/data_cleaning_summary.csv")

CATEGORY_MAP = {
    "Backpack": "Bags & Accessories",
    "Belt": "Bags & Accessories",
    "Bowtie": "Bags & Accessories",
    "Gloves": "Bags & Accessories",
    "Handbag": "Bags & Accessories",
    "Hat": "Bags & Accessories",
    "Scarf": "Bags & Accessories",
    "Socks": "Bags & Accessories",
    "Sun Hat": "Bags & Accessories",
    "Sunglasses": "Bags & Accessories",
    "Tie": "Bags & Accessories",
    "Umbrella": "Bags & Accessories",
    "Wallet": "Bags & Accessories",

    "Sneakers": "Footwear",
    "Loafers": "Footwear",
    "Boots": "Footwear",
    "Sandals": "Footwear",
    "Slippers": "Footwear",
    "Flip-Flops": "Footwear",

    "Camisole": "Tops",
    "Tank Top": "Tops",
    "Hoodie": "Tops",
    "Cardigan": "Tops",
    "T-shirt": "Tops",
    "Flannel Shirt": "Tops",
    "Blouse": "Tops",
    "Tunic": "Tops",
    "Sweater": "Tops",
    "Polo Shirt": "Tops",

    "Poncho": "Outerwear",
    "Trench Coat": "Outerwear",
    "Coat": "Outerwear",
    "Blazer": "Outerwear",
    "Raincoat": "Outerwear",
    "Jacket": "Outerwear",
    "Vest": "Outerwear",

    "Shorts": "Bottoms",
    "Pants": "Bottoms",
    "Leggings": "Bottoms",
    "Jeans": "Bottoms",
    "Trousers": "Bottoms",
    "Skirt": "Bottoms",

    "Kimono": "Dresses & One-Piece",
    "Onesie": "Dresses & One-Piece",
    "Overalls": "Dresses & One-Piece",
    "Dress": "Dresses & One-Piece",
    "Jumpsuit": "Dresses & One-Piece",
    "Romper": "Dresses & One-Piece",

    "Pajamas": "Loungewear & Seasonal",
    "Swimsuit": "Loungewear & Seasonal",
}

def clean_data(input_path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    if not input_path.exists():
        raise FileNotFoundError("Please place the dataset at data/raw/fashion_retail_sales.csv")

    df = pd.read_csv(input_path)
    raw_records = len(df)
    raw_columns = len(df.columns)

    df = df.rename(columns={
        "Customer Reference ID": "Customer Reference ID",
        "Purchase Amount (USD)": "Purchase Amount",
        "Purchase amount": "Purchase Amount",
        "Date purchase": "Date Purchase",
        "Review Ratings": "Review Rating",
    })

    required = ["Item Purchased", "Purchase Amount", "Date Purchase", "Review Rating", "Payment Method"]
    missing_cols = [c for c in required if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    missing_purchase_amount = df["Purchase Amount"].isna().sum()
    missing_review_rating = df["Review Rating"].isna().sum()

    df["Date Purchase"] = pd.to_datetime(df["Date Purchase"], format="%d-%m-%Y", errors="coerce")
    df["Purchase Amount"] = pd.to_numeric(df["Purchase Amount"], errors="coerce")
    df["Review Rating"] = pd.to_numeric(df["Review Rating"], errors="coerce")

    df = df.dropna(subset=["Purchase Amount", "Review Rating", "Date Purchase"]).copy()
    records_after_missing = len(df)

    q1 = df["Purchase Amount"].quantile(0.25)
    q3 = df["Purchase Amount"].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    before_outlier = len(df)
    df = df[(df["Purchase Amount"] >= lower_bound) & (df["Purchase Amount"] <= upper_bound)].copy()
    outliers_removed = before_outlier - len(df)

    df["Product Category"] = df["Item Purchased"].map(CATEGORY_MAP).fillna("Other")

    CLEANED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEANED_DATA_PATH, index=False)

    summary = pd.DataFrame({
        "Metric": [
            "Raw records",
            "Raw columns",
            "Missing purchase amount",
            "Missing review rating",
            "Records after missing value removal",
            "Outliers removed using IQR",
            "Clean records used",
            "Unique items",
            "Date range start",
            "Date range end"
        ],
        "Value": [
            raw_records,
            raw_columns,
            missing_purchase_amount,
            missing_review_rating,
            records_after_missing,
            outliers_removed,
            len(df),
            df["Item Purchased"].nunique(),
            df["Date Purchase"].min().date(),
            df["Date Purchase"].max().date()
        ]
    })
    summary.to_csv(SUMMARY_PATH, index=False)

    return df

if __name__ == "__main__":
    cleaned = clean_data()
    print(f"Data cleaning complete. Clean records used: {len(cleaned)}")
