import streamlit as st

st.title("Contact Us")

st.markdown("""
We welcome questions, feedback, and collaboration inquiries. Please use the contact form below or reach out to us directly.
""")

# ---- Direct Contact Information ----
st.subheader("Curators")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Alex Wardale**  
    *Data Manager and Bioinformatics Lead*  
    
    e-mail: `alex.wardale [at] oist.jp`  
    [LinkedIn](https://www.linkedin.com/in/alex-wardale-a428a6114/)
    """)

with col2:
    st.markdown("""
    **Cédric Finet**  
    *Group Leader*  
    
    e-mail: `cedric.finet [at] oist.jp`  
    [Website](https://cfinet.github.io/research/index.html)
    """)

st.markdown("---")

# ---- Institution Information ----
st.subheader("Institution")

st.markdown("""
**Biological Design Unit**  
Okinawa Institute of Science and Technology Graduate University (OIST)

1919-1 Tancha, Onna-son, Okinawa 904-0495, Japan  
[www.oist.jp](https://www.oist.jp)  
[Biological Design Unit](https://www.oist.jp/research/research-units/bde)
""")

st.markdown("---")

# ---- Additional Resources ----
st.subheader("Additional Resources")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Database Help**
    - [Help & Documentation](/Help)
    - [Submit a Protein](/Submission)
    - [View Statistics](/Statistics)
    """)

with col2:
    st.markdown("""
    **Cite This Database**
    
    If you use Cuticulome.db in your research, please cite:
    
    > Wardale, A. & Finet, C. (2026). Cuticulome.db: A database of function-defined arthropod cuticular proteins (in preparation).
    """)

st.markdown("---")
