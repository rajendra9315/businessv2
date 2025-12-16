import pandas as pd
import numpy as np


def analyze_file(file_path: str):
    # Load data
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    # Basic cleaning
    df.dropna(inplace=True)

    # ---- REQUIRED COLUMNS ----
    # date | revenue | cost | product | category

    # KPIs
    revenue = df["revenue"].sum()
    cost = df["cost"].sum()
    profit = revenue - cost
    margin = (profit / revenue) * 100 if revenue else 0

    # ---- Revenue Trend (Monthly) ----
    df["date"] = pd.to_datetime(df["date"])
    monthly_revenue = (
        df.groupby(df["date"].dt.to_period("M"))["revenue"]
        .sum()
        .reset_index()
    )

    revenue_labels = monthly_revenue["date"].astype(str).tolist()
    revenue_data = monthly_revenue["revenue"].tolist()

    # ---- Profit by Product ----
    product_profit = (
        df.groupby("product")[["revenue", "cost"]]
        .sum()
        .reset_index()
    )
    product_profit["profit"] = (
        product_profit["revenue"] - product_profit["cost"]
    )

    product_labels = product_profit["product"].tolist()
    product_data = product_profit["profit"].tolist()

    # ---- Cost Breakdown ----
    cost_breakdown = (
        df.groupby("category")["cost"]
        .sum()
        .reset_index()
    )

    cost_labels = cost_breakdown["category"].tolist()
    cost_data = cost_breakdown["cost"].tolist()

    # ---- Growth ----
    growth = (
        monthly_revenue["revenue"]
        .pct_change()
        .mean() * 100
    )

    return {
        "kpis": {
            "revenue": round(revenue, 2),
            "profit": round(profit, 2),
            "margin": round(margin, 2),
            "growth": round(growth, 2)
        },
        "charts": {
            "revenue_trend": {
                "labels": revenue_labels,
                "data": revenue_data
            },
            "profit_by_product": {
                "labels": product_labels,
                "data": product_data
            },
            "cost_breakdown": {
                "labels": cost_labels,
                "data": cost_data
            }
        }
    }

