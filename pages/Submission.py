import streamlit as st
import requests
import os
from datetime import datetime

st.title("Submit a New Cuticular Protein")

st.markdown("""
Help us keep the **Cuticulome.db** up to date by submitting a new entry.  
Whether you've identified a missing protein or published a new finding, please provide as much detail as possible. We will contact you via e-mail following your submission.
""")

# ---- Google Form Configuration ----
# These are loaded from Streamlit secrets or environment variables

try:
    # Load from Streamlit secrets (for Streamlit Cloud deployment)
    GOOGLE_FORM_ACTION_URL = st.secrets["google_form"]["action_url"]
    FORM_ENTRY_IDS = {
        "protein_name": st.secrets["google_form"]["entry_protein_name"],
        "species": st.secrets["google_form"]["entry_species"],
        "protein_family": st.secrets["google_form"]["entry_protein_family"],
        "function": st.secrets["google_form"]["entry_function"],
        "tissue": st.secrets["google_form"]["entry_tissue"],
        "protein_sequence": st.secrets["google_form"]["entry_protein_sequence"],
        "cds_sequence": st.secrets["google_form"]["entry_cds_sequence"],
        "reference": st.secrets["google_form"]["entry_reference"],
        "doi": st.secrets["google_form"]["entry_doi"],
        "submitter_name": st.secrets["google_form"]["entry_submitter_name"],
        "submitter_email": st.secrets["google_form"]["entry_submitter_email"]
    }
except (FileNotFoundError, KeyError):
    # Fallback to environment variables (for local development)
    GOOGLE_FORM_ACTION_URL = os.getenv("GOOGLE_FORM_ACTION_URL", "")
    FORM_ENTRY_IDS = {
        "protein_name": os.getenv("ENTRY_PROTEIN_NAME", ""),
        "species": os.getenv("ENTRY_SPECIES", ""),
        "protein_family": os.getenv("ENTRY_PROTEIN_FAMILY", ""),
        "function": os.getenv("ENTRY_FUNCTION", ""),
        "tissue": os.getenv("ENTRY_TISSUE", ""),
        "protein_sequence": os.getenv("ENTRY_PROTEIN_SEQUENCE", ""),
        "cds_sequence": os.getenv("ENTRY_CDS_SEQUENCE", ""),
        "reference": os.getenv("ENTRY_REFERENCE", ""),
        "doi": os.getenv("ENTRY_DOI", ""),
        "submitter_name": os.getenv("ENTRY_SUBMITTER_NAME", ""),
        "submitter_email": os.getenv("ENTRY_SUBMITTER_EMAIL", "")
    }

# Check if form is configured
FORM_CONFIGURED = bool(GOOGLE_FORM_ACTION_URL and all(FORM_ENTRY_IDS.values()))

# ---- Submission form ----
with st.form("submission_form", clear_on_submit=True):
    st.subheader("Protein Information")
    
    protein_name = st.text_input(
        "Cuticular Protein Name *", 
        max_chars=200,
        help="Required. Max 200 characters."
    )
    
    species = st.text_input(
        "Species *", 
        max_chars=200,
        help="Required. Scientific name (e.g., Drosophila melanogaster)"
    )
    
    protein_family = st.text_input(
        "Protein Family", 
        max_chars=200,
        help="Optional. The protein family/group this protein belongs to"
    )
    
    function = st.text_area(
        "Function *", 
        max_chars=500,
        help="Required. Biological role or inferred function of the protein"
    )
    
    tissue = st.text_input(
        "Tissue Specificity", 
        max_chars=200,
        help="Optional. Where the protein is expressed (e.g., wing, cuticle, etc.)"
    )

    st.subheader("Sequence Information")
    st.markdown("""
    Provide protein and/or CDS sequences in FASTA format. Both fields are optional.
    
    **FASTA format example:**
    ```
    >Dme_CPR1
    MKTIIALSYIFCLVFADYKDDDDK...
    ```
    """)
    
    protein_sequence = st.text_area(
        "Protein Sequence (FASTA)", 
        height=150,
        max_chars=50000,
        help="Optional. Amino acid sequence in FASTA format."
    )
    
    cds_sequence = st.text_area(
        "CDS Sequence (FASTA)", 
        height=150,
        max_chars=150000,
        help="Optional. Coding DNA sequence in FASTA format."
    )

    st.subheader("Publication Information")
    
    reference = st.text_input(
        "Reference (Author et al. Year)", 
        max_chars=300,
        help="Optional. Citation format: Smith et al. 2024"
    )
    
    doi = st.text_input(
        "DOI or URL", 
        max_chars=200,
        help="Optional. Either a DOI (10.xxxx/xxxxx) or full URL to the publication"
    )

    st.subheader("Submitter Information")
    
    submitter_name = st.text_input(
        "Your Name", 
        max_chars=100,
        help="Optional but appreciated"
    )
    
    submitter_email = st.text_input(
        "Your Email *", 
        max_chars=100,
        help="Required. We may contact you if we have questions about your submission"
    )

    submitted = st.form_submit_button("Submit Entry")

# ---- On submit ----
if submitted:
    # Check if form is configured
    if not FORM_CONFIGURED:
        st.error("⚠️ Submission system is not configured. Please contact the administrators.")
        st.stop()
    
    # Basic validation
    errors = []
    
    if not protein_name or len(protein_name.strip()) == 0:
        errors.append("Protein name is required.")
    
    if not species or len(species.strip()) == 0:
        errors.append("Species name is required.")
    
    if not function or len(function.strip()) == 0:
        errors.append("Function is required.")
    
    if not submitter_email or len(submitter_email.strip()) == 0:
        errors.append("Email is required.")
    elif '@' not in submitter_email:
        errors.append("Please enter a valid email address.")
    
    # Display errors if any
    if errors:
        st.error("**Please fix the following errors:**")
        for error in errors:
            st.error(f"• {error}")
    else:
        # Prepare data for Google Forms
        form_data = {
            FORM_ENTRY_IDS["protein_name"]: protein_name.strip(),
            FORM_ENTRY_IDS["species"]: species.strip(),
            FORM_ENTRY_IDS["protein_family"]: protein_family.strip() if protein_family else "",
            FORM_ENTRY_IDS["function"]: function.strip(),
            FORM_ENTRY_IDS["tissue"]: tissue.strip() if tissue else "",
            FORM_ENTRY_IDS["protein_sequence"]: protein_sequence.strip() if protein_sequence else "",
            FORM_ENTRY_IDS["cds_sequence"]: cds_sequence.strip() if cds_sequence else "",
            FORM_ENTRY_IDS["reference"]: reference.strip() if reference else "",
            FORM_ENTRY_IDS["doi"]: doi.strip() if doi else "",
            FORM_ENTRY_IDS["submitter_name"]: submitter_name.strip() if submitter_name else "",
            FORM_ENTRY_IDS["submitter_email"]: submitter_email.strip()
        }
        
        try:
            # Submit to Google Forms
            response = requests.post(
                GOOGLE_FORM_ACTION_URL,
                data=form_data,
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'User-Agent': 'Mozilla/5.0'
                },
                timeout=10
            )
            
            # Google Forms returns 200 even on success
            st.success("✅ Thank you! Your submission has been received and will be reviewed by the curators.")
            
            # Optional: Display what was submitted for confirmation
            with st.expander("View your submission"):
                st.write("**Protein Name:**", protein_name.strip())
                st.write("**Species:**", species.strip())
                if protein_family.strip():
                    st.write("**Protein Family:**", protein_family.strip())
                st.write("**Function:**", function.strip())
                if tissue.strip():
                    st.write("**Tissue Specificity:**", tissue.strip())
                if protein_sequence.strip():
                    st.write("**Protein Sequence:**", "Provided")
                if cds_sequence.strip():
                    st.write("**CDS Sequence:**", "Provided")
                if reference.strip():
                    st.write("**Reference:**", reference.strip())
                if doi.strip():
                    st.write("**DOI/URL:**", doi.strip())
        
        except requests.exceptions.Timeout:
            st.error("❌ The submission timed out. Please try again.")
            st.info("If the problem persists, please contact the curators directly via the Contact page.")
        except requests.exceptions.RequestException as e:
            st.error("❌ An error occurred while submitting your data. Please try again later.")
            st.info("If the problem persists, please contact the curators directly via the Contact page.")

# ---- Information box ----
st.markdown("---")
st.info("""
**Required fields are marked with an asterisk (*)**

Your submission will be reviewed by our curators before being added to the main database. 
We appreciate your contribution to Cuticulome.db!

For questions or issues, please visit the Contact page.
""")
