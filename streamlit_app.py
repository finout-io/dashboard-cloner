import streamlit as st
from cloner import clone_dashboard

st.set_page_config(page_title="Finout Dashboard Cloner", layout="centered")
st.title("📊 Finout Dashboard Cloner")
st.write(
    "An app built to enable quick cloning of dashboards to other accounts, maintaining all relevent widgets and placement."
)

with st.form("clone_form"):
    api_token = st.text_input("Finout API Token", type="password")
    source_dashboard_id = st.text_input("Source Dashboard ID")
    new_dashboard_name = st.text_input("New Dashboard Name")
    submitted = st.form_submit_button("Clone Dashboard")

if submitted:
    if not api_token or not source_dashboard_id or not new_dashboard_name:
        st.error("Please fill out all fields.")
    else:
        try:
            new_id = clone_dashboard(api_token, source_dashboard_id, new_dashboard_name)
            st.success(f"Dashboard cloned successfully! New Dashboard ID: {new_id}")
        except Exception as e:
            st.error(f"Error cloning dashboard: {e}")
