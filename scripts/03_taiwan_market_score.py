from pathlib import Path
import pandas as pd

CATEGORY_SUMMARY_PATH = Path("data/cleaned/category_summary.csv")
OUTPUT_PATH = Path("data/cleaned/taiwan_market_potential_score.csv")

def min_max_normalize(series: pd.Series) -> pd.Series:
    if series.max() == series.min():
        return pd.Series([100] * len(series), index=series.index)
    return (series - series.min()) / (series.max() - series.min()) * 100

def calculate_score(category_summary: pd.DataFrame) -> pd.DataFrame:
    df = category_summary.copy()

    df["Frequency_Score"] = min_max_normalize(df["Purchases"])
    df["Rating_Score"] = min_max_normalize(df["Average_Rating"])
    df["Purchase_Amount_Score"] = min_max_normalize(df["Average_Purchase_USD"])

    df["Taiwan_Market_Potential_Score"] = (
        0.45 * df["Frequency_Score"]
        + 0.30 * df["Rating_Score"]
        + 0.25 * df["Purchase_Amount_Score"]
    ).round(1)

    return df.sort_values("Taiwan_Market_Potential_Score", ascending=False)

def run_scoring():
    category_summary = pd.read_csv(CATEGORY_SUMMARY_PATH)
    score_table = calculate_score(category_summary)
    score_table.to_csv(OUTPUT_PATH, index=False)
    return score_table

if __name__ == "__main__":
    scores = run_scoring()
    print(scores[["Product Category", "Taiwan_Market_Potential_Score"]])
