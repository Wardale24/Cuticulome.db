import os
import zipfile
import tempfile
import shutil
import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

# --------------------
# Page configuration
# --------------------
st.set_page_config(page_title="Cuticulome.db", page_icon="🐜")

DB_PATH = Path("cuticulome.db")
FASTA_ROOT = Path("fasta_files")

# --------------------
# Load data from SQLite
# --------------------
@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        """
        SELECT
            name AS "Cuticular Protein Name",
            species AS "Species",
            phylum AS "Phylum",
            subphylum AS "Subphylum",
            class AS "Class",
            "order" AS "Order",
            family AS "Family",
            genus AS "Genus",
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

# --------------------
# Title & intro
# --------------------
st.title("🐜 Cuticulome.db")
st.markdown("""
A **database of function-defined arthropod cuticular proteins**, built to centralize
molecular, functional, and taxonomic information across species.

Use the sidebar filters to explore the dataset and export selected entries together
with their original FASTA sequences.
""")

# --------------------
# Sidebar filters
# --------------------
st.sidebar.header("Filter Proteins")

name_search = st.sidebar.text_input("Search Cuticular Protein")

filtered_df = df.copy()

# --- Subphylum ---
subphylum_opts = sorted(filtered_df["Subphylum"].dropna().unique())
subphylum = st.sidebar.selectbox("Subphylum", ["All"] + subphylum_opts)
if subphylum != "All":
    filtered_df = filtered_df[filtered_df["Subphylum"] == subphylum]

# --- Class ---
if subphylum != "All":
    class_opts = sorted(filtered_df["Class"].dropna().unique())
    class_sel = st.sidebar.selectbox("Class", ["All"] + class_opts)
    if class_sel != "All":
        filtered_df = filtered_df[filtered_df["Class"] == class_sel]
else:
    class_sel = "All"

# --- Order ---
if class_sel != "All":
    order_opts = sorted(filtered_df["Order"].dropna().unique())
    order_sel = st.sidebar.selectbox("Order", ["All"] + order_opts)
    if order_sel != "All":
        filtered_df = filtered_df[filtered_df["Order"] == order_sel]
else:
    order_sel = "All"

# --- Family ---
if order_sel != "All":
    family_opts = sorted(filtered_df["Family"].dropna().unique())
    family_sel = st.sidebar.selectbox("Family", ["All"] + family_opts)
    if family_sel != "All":
        filtered_df = filtered_df[filtered_df["Family"] == family_sel]
else:
    family_sel = "All"

# --- Genus ---
if family_sel != "All":
    genus_opts = sorted(filtered_df["Genus"].dropna().unique())
    genus_sel = st.sidebar.selectbox("Genus", ["All"] + genus_opts)
    if genus_sel != "All":
        filtered_df = filtered_df[filtered_df["Genus"] == genus_sel]
else:
    genus_sel = "All"

# --- Species ---
if genus_sel != "All":
    species_opts = sorted(filtered_df["Species"].dropna().unique())
    species_sel = st.sidebar.selectbox("Species", ["All"] + species_opts)
    if species_sel != "All":
        filtered_df = filtered_df[filtered_df["Species"] == species_sel]
else:
    species_sel = "All"

# --- Protein name search ---
if name_search:
    mask = filtered_df.apply(
        lambda row: row.astype(str).str.contains(
            name_search,
            case=False,
            regex=False,
            na=False
        ).any(),
        axis=1
    )
    filtered_df = filtered_df[mask]


# Preserve full dataframe for export
export_df = filtered_df.copy()

# --------------------
# Display table
# --------------------
columns_to_show = [
    "Cuticular Protein Name",
    "Species",
    "Protein Family",
    "Function",
    "Reference",
    "DOI"
]

display_df = filtered_df[columns_to_show]

st.subheader("Filtered Database")
st.dataframe(display_df, use_container_width=True, hide_index=True)


# --------------------
# Export logic
# --------------------
def create_zip_export_bytes(df):
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, "cuticulome_export.zip")

    # --- Metadata folder ---
    metadata_dir = os.path.join(temp_dir, "1_Metadata")
    os.makedirs(metadata_dir, exist_ok=True)

    # metadata.csv
    metadata_csv = os.path.join(metadata_dir, "metadata.csv")
    df.to_csv(metadata_csv, index=False, encoding="utf-8")

    # README.txt
    readme_txt = os.path.join(metadata_dir, "README.txt")
    with open(readme_txt, "w", encoding="utf-8") as f:
        f.write(
            "Thank you for using Cuticulome.db!\n\n"
            "If you use data from this download in a publication, preprint, "
            "presentation, or other scholarly work, we kindly ask that you cite "
            "Cuticulome.db.\n\n"
            "Citation information:\n"
            "  Cuticulome.db – A database of function-defined arthropod cuticular proteins, 2026 Release.\n"
            "  Authors: Alex Wardale & Cédric Finet\n"
            "  URL: (add project URL or repository here)\n\n"
            "This helps support continued development and maintenance of the database.\n\n"
            "Thank you!"
        )

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:

        # --- Add Metadata folder first ---
        zipf.write(metadata_csv, arcname="1_Metadata/metadata.csv")
        zipf.write(readme_txt, arcname="1_Metadata/README.txt")

        # --- Add FASTA folders ---
        for protein in df["Cuticular Protein Name"]:
            protein_dir = FASTA_ROOT / protein
            if not protein_dir.is_dir():
                continue

            for file in protein_dir.iterdir():
                if file.is_file():
                    arcname = f"{protein}/{file.name}"
                    zipf.write(file, arcname=arcname)

    with open(zip_path, "rb") as f:
        zip_bytes = f.read()

    shutil.rmtree(temp_dir)
    return zip_bytes

# --------------------
# Download section
# --------------------
st.subheader("Export")

if export_df.empty:
    st.warning("No entries selected.")
else:
    zip_bytes = create_zip_export_bytes(export_df)

    st.download_button(
        label="⬇️ Download dataset (CSV + FASTA)",
        data=zip_bytes,
        file_name="cuticulome_export.zip",
        mime="application/zip"
    )

# --------------------
# Footer
# --------------------
st.markdown("---")
st.caption("Cuticulome.db v0.1 | Last updated: February 2026")

