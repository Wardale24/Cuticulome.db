import streamlit as st

st.title("Understanding the Cuticulome Database")

st.markdown("""
### Overview
The **Cuticulome Database** compiles verified information on function-defined arthropod cuticular proteins, 
including protein family, tissue specificity, and identified or inferred functions. 
Our goal is to centralize cuticular protein information across arthropod species to facilitate downstream comparative studies and functional analyses.

---

### Nomenclature Standard

#### The Challenge
Historically, scientists have not had a unified way of naming cuticular proteins in arthropods. This has led to inconsistent naming conventions across different research groups and publications. For example, the same protein across different species might be named:

- `Dmel_CPR1` in *Drosophila melanogaster*
- `apme_cpr1` in *Apis mellifera*  
- `MpCPR1` in *Myzus persicae*

This inconsistency can lead to difficulties in downstream cross-species comparisons.

###
#### Our Solution
To avoid misunderstandings and facilitate database searches, we have standardized all protein nomenclature in our database to the following format:

**Format:** `Xxx_ProteinName`

Where:
- **First letter:** Capitalized (genus initial)
- **Second & third letters:** Lowercase (species initials)
- **Underscore:** Separator
- **Protein name:** Original protein designation

#### Examples

| Species | Old Nomenclature | New Standardized Name |
|---------|------------------|----------------------|
| *Drosophila melanogaster* | Dmel_CPR1, DMCPR1 | **Dme_CPR1** |
| *Myzus persicae* | MpCPR1, mp-cpr1 | **Mpe_CPR1** |
| *Apis mellifera* | apme_cpr1, AmCPR1 | **Ame_CPR1** |

###
#### Exceptions to Nomenclature
The three-letter species prefix system can lead to naming conflicts between different species. For example, *Heliothis virescens* and *Heortia vitessoides* would both generate the same prefix. To avoid ambiguity, the full genus name is added as an additional prefix when such conflicts occur. This ensures that each protein name remains unique and clearly associated with the correct species. Exception example:

| Species | Standardized Name | New Standadized Name | 
|---------|------------------|----------------------|
| *Heliothis virescens* | Hvi_ProteinName | Heliothis_Hvi_ProteinName |
| *Heortia vitessoides* | Hvi_ProteinName | Heortia_Hvi_ProteinName |

###
#### Important Notes

**We are not attempting to officially rename proteins.** This standardization applies only within our database for consistency and searchability.

**Previous nomenclatures are preserved.** We maintain records of alternative names in the additional information section.

**Search flexibility.** You can search for proteins using either the standardized cuticulome.db name or common alternatives.

---

### Database Structure

The database is organized chronologically, with newest additions to the database appearing first.

#### Protein Information
|  | Description |
|--------|--------------|
| **Cuticular Protein** | Standardized name of the cuticular protein (see **Nomenclature** section below for more details) |
| **Protein Family** | Family or group to which the cuticular protein belongs (e.g., CPR, CPAP, CPLC) |
| **Function** | Biological role or experimentally validated/inferred function |

#### Source Publication Information
|  | Description |
|--------|--------------|
| **Reference** | Source publication that describes the function of the protein (not necessarily the identification of the protein) |
| **DOI** | Digital Object Identifier or URL to the source publication |

---

### Using the Database

Return to the [**Database**](/) to start exploring.

#### Filtering
Use the sidebar filters to narrow down entries by:
- Taxonomic level (Subphylum → Class → Order → Family → Genus → Species)
- Protein name search (searches across all fields)

#### Exporting Data
Select your desired entries using the filters, then click the download button to export:
- **CSV file** with all metadata
- **FASTA files** with protein and CDS sequences
- **README** with additional information

---

### Contributing

If you have identified a missing protein or published new findings on arthropod cuticular proteins, 
please visit the [**Submission**](/Submission) page to contribute to the database.

All submissions are reviewed by our curators before being added to ensure data quality and consistency.

---

### Questions or Feedback?

For questions, suggestions, or to report issues, please visit the [**Contact**](/Contact) page.
""")

# --------------------
# Footer
# --------------------
st.markdown("---")
st.caption("Cuticulome.db v0.1 | Last updated: February 2026")
