import streamlit as st

st.title("Contact Us")

st.markdown("""
We welcome questions, feedback, and collaboration inquiries. Please use the contact form below or reach out to us directly.
""")

# ---- Contact Form ----
st.subheader("Send Us a Message")

with st.form("contact_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        contact_name = st.text_input("Your Name *", max_chars=100)
    
    with col2:
        contact_email = st.text_input("Your Email *", max_chars=100)
    
    subject = st.selectbox(
        "Subject *",
        [
            "General Inquiry",
            "Database Question",
            "Submission Issue",
            "Collaboration Proposal",
            "Bug Report",
            "Feature Request",
            "Other"
        ]
    )
    
    message = st.text_area(
        "Message *",
        max_chars=2000,
        height=200,
        help="Please provide details about your inquiry"
    )
    
    contact_submitted = st.form_submit_button("Send Message")

if contact_submitted:
    errors = []
    
    if not contact_name or len(contact_name.strip()) == 0:
        errors.append("Name is required.")
    
    if not contact_email or len(contact_email.strip()) == 0:
        errors.append("Email is required.")
    elif '@' not in contact_email:
        errors.append("Please enter a valid email address.")
    
    if not message or len(message.strip()) == 0:
        errors.append("Message is required.")
    
    if errors:
        st.error("**Please fix the following errors:**")
        for error in errors:
            st.error(f"• {error}")
    else:
        # TODO: Connect to Google Form for contact submissions
        # For now, just show success message
        st.success("✅ Thank you! Your message has been received. We'll get back to you soon.")
        st.balloons()
        
        st.info("**For urgent matters**, please contact us directly using the information below.")

st.markdown("---")

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
