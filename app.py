import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_dynamic_filters import DynamicFilters
from engine import load_data, clean_data, add_features, calculate_kpis
st.set_page_config(page_title="APLLogistics", page_icon="1.png", layout="wide", initial_sidebar_state="collapsed", menu_items={
    'Get Help': 'https://www.apllogistics.com/contact-us/',})
st.title("APL Logistics - Data Analysis and Insights")
selected = option_menu(
    menu_title=None,
    options=["Overview", "Analysis", "Insights"],
    icons=["house", "bar-chart", "graph-up"],
    orientation="horizontal"
)
st.title("Supply Chain Analytics Dashboard")


df = load_data("APL_Logistics.csv")
df = clean_data(df)
df = add_features(df)
filters = DynamicFilters(
    df,
    filters=[
        "Order Region",
        "Shipping Mode",
        "Customer Segment",
        "Market"
    ]
)
st.sidebar.header("Filter Data")
filters.display_filters(location="sidebar")
df = filters.filter_df()
if selected == "Overview":
    st.subheader("Key Metrics")
    kpis = calculate_kpis(df)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style='background-color:#1e1e1e;padding:20px;border-radius:10px'>
            <h4>On-Time Delivery %</h4>
            <h2>{kpis['on_time_rate']:.2f}%</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style='background-color:#1e1e1e;padding:20px;border-radius:10px'>
        <h4>Avg Delay (days)</h4>
        <h2>{kpis['avg_delay']:.2f}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style='background-color:#1e1e1e;padding:20px;border-radius:10px'>
            <h4>Late Risk Ratio</h4>
            <h2>{kpis['risk_ratio']:.2f}</h2>
        </div>
        """, unsafe_allow_html=True)

elif selected == "Analysis":
    st.subheader("Analysis Section")
    st.write("Add charts here")

elif selected == "Insights":
    st.subheader("Insights Section")
    st.write("Add insights here")

