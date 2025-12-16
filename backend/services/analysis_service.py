import pandas as pd
import numpy as np
from typing import Dict, Optional


# -------------------------------
# COLUMN DETECTION LOGIC
# -------------------------------

def detect_column(df: pd.DataFrame, keywords):
    """
    Try to detect a column based on keyword matches.
    """
    for col in df.columns:
        col_lower = col.lower().replace(" ", "").replace("_", "")
        for key in keywords:
            if key in col_lower:
                return col
    return None


# -------------------------------
# MAIN ANALYSIS FUNCTION
# -------------------------------

def analyze_file(
    file_path: str,
    column_mapping: Optional[Dict[str, str]] = None
):
    """
    Analyze uploaded CSV/Excel file and return KPIs + chart data.

    column_mapping (optional):
    {
        "date": "Order Date",
        "revenue": "Total Sales",
        "cost": "Shipping Cost",
        "product": "Product Name",
        "category": "Cost Type"
    }
    """

    # -------------------------------
    # LOAD FILE
    # -------------------------------
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    df.dropna(inplace=True)

    # -------------------------------
    # AUTO-DETECT OR USE MAPPING
    # -------------------------------
    if column_mapping:
        date_col = column_mapping.get("date")
        revenue_col = column_mapping.get("revenue")
        cost_col = column_mapping.get("cost")
        product_col = column_mapping.get("product")
        category_col = column_mapping.get("category")
    else:
        date_col = detect_column(df, ["date", "orderdate", "created"])
        revenue_col = detect_column(df, ["revenue", "sales", "amount", "total"])
        cost_col = detect_column(df, ["cost", "expense", "shipping"])
        product_col = detect_column(df, ["product", "item", "sku"])
        category_col = detect_column(df, ["category", "type", "costtype"])

    # -------------------------------
    # VALIDATION
    # -------------------------------
    required = {
        "date": date_col,
        "revenue": revenue_col,
        "cost": cost_col
    }

    missing = [k for k, v in required.items() if v is None]

    if missing:
        return {
            "status": "error",
            "message": "Required columns not detected",
            "missing": missing,
            "available_columns": list(df.columns)
        }

    # -------------------------------
    # DATA PREPARATION
    # -------------------------------
    df[date_col] = pd.to_datetime(df[date_col])
    df[revenue_col] = pd.to_numeric(df[revenue_col], errors="coerce")
    df[cost_col] = pd.to_numeric(df[cost_col], errors="coerce")

    df.dropna(subset=[revenue_col, cost_col, date_col], inplace=True)

    # -------------------------------
    # KPI CALCULATIONS
    # -------------------------------
    total_revenue = df[revenue_col].sum()
    total_cost = df[cost_col].sum()
    total_profit = total_revenue - total_cost
    margin = (total_profit / total_revenue * 100) if total_revenue else 0

    # -------------------------------
    # REVENUE TREND (MONTHLY)
    # -------------------------------
    monthly = (
        df.groupby(df[date_col].dt.to_period("M"))[revenue_col]
        .sum()
        .reset_index()
    )

    revenue_trend_labels = monthly[date_col].astype(str).tolist()
    revenue_trend_data = monthly[revenue_col].round(2).tolist()

    growth = monthly[revenue_col].pct_change().mean() * 100 if len(monthly) > 1 else 0

    # -------------------------------
    # PROFIT BY PRODUCT (OPTIONAL)
    # -------------------------------
    profit_by_product = {"labels": [], "data": []}

    if product_col:
        product_df = (
            df.groupby(product_col)[[revenue_col, cost_col]]
            .sum()
            .reset_index()
        )
        product_df["profit"] = product_df[revenue_col] - product_df[cost_col]

        profit_by_product = {
            "labels": product_df[product_col].tolist(),
            "data": product_df["profit"].round(2).tolist()
        }

    # -------------------------------
    # COST BREAKDOWN (OPTIONAL)
    # -------------------------------
    cost_breakdown = {"labels": [], "data": []}

    if category_col:
        cost_df = (
            df.groupby(category_col)[cost_col]
            .sum()
            .reset_index()
        )

        cost_breakdown = {
            "labels": cost_df[category_col].tolist(),
            "data": cost_df[cost_col].round(2).tolist()
        }

    # -------------------------------
    # FINAL RESPONSE
    # -------------------------------
    return {
        "status": "success",
        "kpis": {
            "revenue": round(total_revenue, 2),
            "profit": round(total_profit, 2),
            "margin": round(margin, 2),
            "growth": round(growth, 2)
        },
        "charts": {
            "revenue_trend": {
                "labels": revenue_trend_labels,
                "data": revenue_trend_data
            },
            "profit_by_product": profit_by_product,
            "cost_breakdown": cost_breakdown
        },
        "meta": {
            "rows_analyzed": len(df),
            "columns_used": {
                "date": date_col,
                "revenue": revenue_col,
                "cost": cost_col,
                "product": product_col,
                "category": category_col
            }
        }
    }


