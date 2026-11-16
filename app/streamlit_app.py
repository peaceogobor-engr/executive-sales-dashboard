"""Executive Sales Dashboard — reads the mart produced by the
retail-sales-data-pipeline repo and answers three executive questions:
How are we doing? Where are we winning/losing? What needs attention?
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Executive Sales Dashboard", layout="wide")

DATA = Path(__file__).resolve().parent.parent / "data" / "sales_mart.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA)
    df["date"] = pd.to_datetime(df["year_month"])
    return df


df = load_data()

st.title("Executive Sales Dashboard")
st.caption("Source: star-schema mart from retail-sales-data-pipeline (public demo data)")

# --- Filters ---
with st.sidebar:
    st.header("Filters")
    regions = st.multiselect("Region", sorted(df["region"].unique()),
                             default=sorted(df["region"].unique()))
    categories = st.multiselect("Category", sorted(df["category"].unique()),
                                default=sorted(df["category"].unique()))
    segments = st.multiselect("Segment", sorted(df["segment"].unique()),
                              default=sorted(df["segment"].unique()))

f = df[df["region"].isin(regions)
       & df["category"].isin(categories)
       & df["segment"].isin(segments)]

# --- KPI cards ---
sales, profit, orders = f["sales"].sum(), f["profit"].sum(), f["orders"].sum()
margin = profit / sales if sales else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Sales", f"${sales:,.0f}")
c2.metric("Total Profit", f"${profit:,.0f}")
c3.metric("Profit Margin", f"{margin:.1%}")
c4.metric("Orders", f"{orders:,}")

# --- Trend ---
trend = f.groupby("date", as_index=False)[["sales", "profit"]].sum()
st.subheader("Sales & Profit Trend")
st.plotly_chart(px.line(trend, x="date", y=["sales", "profit"],
                        labels={"value": "USD", "variable": ""}),
                use_container_width=True)

# --- Breakdowns ---
left, right = st.columns(2)
with left:
    st.subheader("Sales by Category")
    cat = f.groupby("category", as_index=False)["sales"].sum()
    st.plotly_chart(px.bar(cat, x="category", y="sales"), use_container_width=True)
with right:
    st.subheader("Profit by Segment")
    seg = f.groupby("segment", as_index=False)["profit"].sum()
    st.plotly_chart(px.pie(seg, names="segment", values="profit", hole=0.4),
                    use_container_width=True)

# --- Attention table: where margin is negative ---
st.subheader("Needs Attention: Negative-Margin Slices")
bad = (f.groupby(["region", "category"], as_index=False)
         .agg(sales=("sales", "sum"), profit=("profit", "sum")))
bad["margin"] = bad["profit"] / bad["sales"]
st.dataframe(bad[bad["profit"] < 0].sort_values("profit"),
             use_container_width=True, hide_index=True)
