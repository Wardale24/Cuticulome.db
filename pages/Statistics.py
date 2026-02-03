import streamlit as st
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
from pathlib import Path
import re

st.title("Database Statistics")

# ---- Load data from SQLite ----
@st.cache_data
def load_data():
    db_path = Path("cuticulome.db")
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(
        """
        SELECT
            name AS "Cuticular Protein Name",
            species AS "Species",
            subphylum AS "Subphylum",
            class AS "Class",
            "order" AS "Order",
            family AS "Family",
            protein_family AS "Protein Family",
            function AS "Function",
            reference AS "Reference",
            doi AS "DOI"
        FROM proteins
        """,
        conn
    )
    conn.close()
    return df

df = load_data()

# ---- Overview ----
st.subheader("Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Proteins", len(df))

with col2:
    unique_species = df["Species"].nunique()
    st.metric("Species", unique_species)

with col3:
    unique_families = df["Protein Family"].nunique()
    st.metric("Protein Families", unique_families)

st.markdown("---")

# ---- Distribution by Species (Bar Chart) ----
st.subheader("Distribution by Species (Top 10)")

species_counts = df["Species"].value_counts().head(10).reset_index()
species_counts.columns = ["Species", "Count"]

fig_species = px.bar(
    species_counts,
    x="Count",
    y="Species",
    orientation='h',
    text="Count",
    color="Count",
    color_continuous_scale="Blues",
    labels={"Count": "Number of Proteins", "Species": "Species"}
)

fig_species.update_traces(textposition="outside")
fig_species.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    showlegend=False,
    yaxis={'categoryorder':'total ascending'},
    height=400
)

st.plotly_chart(fig_species, use_container_width=True)

st.markdown("---")

# ---- Protein Family Distribution ----
st.subheader("Protein Family Distribution")

if "Protein Family" in df.columns:
    # Filter out empty values
    family_data = df[df["Protein Family"].notna() & (df["Protein Family"].str.strip() != "")]
    family_counts = family_data["Protein Family"].value_counts().reset_index()
    family_counts.columns = ["Protein Family", "Count"]
    
    # Show top 15 families
    family_counts_top = family_counts.head(15)
    
    fig_family = px.bar(
        family_counts_top,
        x="Protein Family",
        y="Count",
        text="Count",
        color="Count",
        color_continuous_scale="Purples",
        labels={"Count": "Number of Proteins", "Protein Family": "Protein Family"}
    )
    
    fig_family.update_traces(textposition="outside")
    fig_family.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        xaxis_tickangle=-45,
        height=500
    )
    
    st.plotly_chart(fig_family, use_container_width=True)

st.markdown("---")

# ---- Publications by Year (from CSV) ----
st.subheader("Publications by Year")

pub_csv = "data/publications_by_year.csv"
if os.path.exists(pub_csv):
    df_pub = pd.read_csv(pub_csv).dropna(subset=["Year", "Count"])
    
    # Ensure numeric types
    df_pub["Year"] = df_pub["Year"].astype(int)
    df_pub["Count"] = df_pub["Count"].astype(int)
    df_pub = df_pub.sort_values("Year")
    
    # Rename Count to Publications for consistency
    df_pub = df_pub.rename(columns={"Count": "Publications"})
    
    # Create bar chart
    fig_pub = px.bar(
        df_pub,
        x="Year",
        y="Publications",
        text="Publications",
        labels={"Publications": "Number of Publications", "Year": "Year"},
        color="Publications",
        color_continuous_scale="Blues"
    )
    
    fig_pub.update_traces(textposition="outside")
    fig_pub.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        height=400,
        xaxis=dict(
            tickmode='linear',
            dtick=2  # Show every 2 years to avoid crowding
        )
    )
    
    st.plotly_chart(fig_pub, use_container_width=True)
    
st.markdown("---")
