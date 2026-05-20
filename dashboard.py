import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="ODA Cloud Migration: Sovereignty Pre-Flight Audit",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)
@st.cache_data
def load_audit_data():
    return pd.read_csv('vodafone_migration_audit.csv')

try:
    df = load_audit_data()
except FileNotFoundError:
    st.error("❌ 'vodafone_migration_audit.csv' not found. Please run your digital_bouncer.py script first to generate the dataset!")
    st.stop()

st.sidebar.header("🛡️ Governance Control Center")
st.sidebar.markdown("Use these filters to audit specific vectors across the Open Digital Architecture footprint.")

source_filter = st.sidebar.multiselect(
    "Select Source Infrastructure:",
    options=df['source_node'].unique(),
    default=df['source_node'].unique()
)

data_filter = st.sidebar.multiselect(
    "Select Data Type Sensitivity:",
    options=df['data_type'].unique(),
    default=df['data_type'].unique()
)

filtered_df = df[
    (df['source_node'].isin(source_filter)) & 
    (df['data_type'].isin(data_filter))
]

st.title("🛡️ ODA Cloud Migration: Sovereignty Pre-Flight Audit")
st.markdown("""
**Automated Data Lineage & Policy Enforcement Framework** This operational control panel monitors the staging environment during the decoupled migration of legacy monolithic IT stacks to cloud-native ODA frameworks. 
It programmatically intercepts and quarantines cross-border data routing violations before deployment to production environments.
""")

st.divider()

total_scanned = len(filtered_df)
safe_transfers = len(filtered_df[filtered_df['sovereignty_status'] == 'Safe'])
violations_prevented = total_scanned - safe_transfers

m1, m2, m3 = st.columns(3)
m1.metric("Total Transmission Routes Audited", f"{total_scanned:,}")
m2.metric("✅ Compliant Migrations (Approved)", f"{safe_transfers:,}")
m3.metric("🚨 Boundary Violations Intercepted", f"{violations_prevented:,}", delta="- Risk Mitigated", delta_color="inverse")

st.divider()

col_viz, col_log = st.columns([1, 1])

with col_viz:
    st.subheader("📊 Policy Compliance Distribution")
    if total_scanned > 0:
        status_chart_data = filtered_df['sovereignty_status'].value_counts().reset_index()
        status_chart_data.columns = ['Sovereignty Status', 'Total Interceptions']
        
        st.bar_chart(
            data=status_chart_data, 
            x='Sovereignty Status', 
            y='Total Interceptions',
            use_container_width=True
        )
    else:
        st.info("No records match the current filter selection.")

with col_log:
    st.subheader("📝 Active Interception Log (Quarantine Zone)")
    # Filter view to strictly display actionable policy threats
    threat_log = filtered_df[filtered_df['sovereignty_status'] != 'Safe']
    
    if len(threat_log) > 0:
        st.dataframe(
            threat_log[['flow_id', 'source_node', 'destination_node', 'data_type', 'sovereignty_status']], 
            use_container_width=True,
            hide_index=True
        )
        
        # Add an export feature for compliance officers
        csv_download = threat_log.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Interception Log for Legal Review",
            data=csv_download,
            file_name="oda_sovereignty_intercept_log.csv",
            mime="text/csv"
        )
    else:
        st.success("🟢 Zero boundary violations detected across current parameters.")

st.divider()
st.caption("🔒 System Infrastructure Status: ACTIVE | Policy Version: NIS 2 & GDPR Real-Time Lineage Validation Engine")