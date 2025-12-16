import pandas as pd
import numpy as np


def analyze_file(file_path: str):
    # Read file
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    # Basic cleaning
    df.dropna(inplace=True)

    # REQUIRED columns (example)
    # date | revenue | cost
    revenue = df["revenue"].sum()
    cost = df["cost"].sum()
    profit = revenue - cost
    margin = (profit / revenue) * 100 if revenue else 0

    # Trend calculation
    df["date"] = pd.to_datetime(df["date"])
    monthly = df.groupby(df["date"].dt.to_period("M"))["revenue"].sum()
    growth = monthly.pct_change().mean() * 100

    return {
        "kpis": {
            "revenue": round(revenue, 2),
            "profit": round(profit, 2),
            "margin": round(margin, 2),
            "growth": round(growth, 2)
        },
        "message": "Analysis completed successfully"
    }
