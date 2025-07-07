import streamlit as st
from cloner import clone_dashboard

st.set_page_config(page_title="Finout Dashboard Cloner", layout="centered")
st.title("📊 Finout Dashboard Cloner 📊")
st.write(
    "Quick cloning of dashboards to other accounts, maintaining all relevent widgets and placement."
)

with st.form("clone_form", clear_on_submit=True):
    st.header("Source:")
    st.text("Where do you want to clone a dashboard from?")
    source_account_id = st.text_input("Source Account ID", key="source_account_id")
    source_dashboard_id = st.text_input("Source Dashboard ID", key="source_dashboard_id")
    st.header("Target:")
    st.text("Where do you want to copy this dashboard?")
    target_account_id = st.text_input("Target Account ID", key="target_account_id")
    st.header("New Dashboard Details:")
    new_dashboard_name = st.text_input("New Dashboard Name",key="new_dashboard_name")
    submitted = st.form_submit_button("Clone Dashboard", disabled=False)

if submitted:
    if not all([source_account_id, target_account_id, source_dashboard_id, new_dashboard_name]):
        st.error("Please fill out all fields.")
    else:
        with st.spinner("Cloning dashboard, please wait..."):
            try:
                st.session_state['button_disabled'] = True
                new_id = clone_dashboard(
                    source_account_id=source_account_id,
                    target_account_id=target_account_id,
                    source_dashboard_id=source_dashboard_id,
                    new_dashboard_name=new_dashboard_name
                )

                st.success(f"Dashboard cloned successfully! New Dashboard ID: {new_id}", icon="✅")

            except Exception as e:
                st.error(f"Error cloning dashboard: {e}", icon="🚨")
            finally:
                st.session_state['button_disabled'] = False
