import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
from engine import marketplace_analysis, shipping_mode_analysis, regional_analysis
from streamlit_dynamic_filters import DynamicFilters
from engine import load_data, clean_data, add_features, calculate_kpis
from streamlit_globe import streamlit_globe
st.set_page_config(page_title="APLLogistics", page_icon="1.png", layout="wide", initial_sidebar_state="collapsed", menu_items={
    'Get Help': 'https://www.apllogistics.com/contact-us/',})
st.title("APL Logistics - Data Analysis and Insights")
st.title("Supply Chain Analytics Dashboard")
selected = option_menu(
    menu_title=None,
    options=["Overview", "Analysis", "Insights"],
    icons=["house", "bar-chart", "graph-up"],
    orientation="horizontal"
)



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
    mode_df = shipping_mode_analysis(df)
    fig = px.bar(
        mode_df,
        x="delay_gap",
        y=mode_df.index,
        orientation="h",
        title="Delay by Shipping Mode"
        )
    st.plotly_chart(fig,use_container_width=True)
    region_df = regional_analysis(df)

    fig = px.bar(
        region_df,
        x="delay_gap",
        y=region_df.index,
        orientation="h",
        title="Delay by Region"
        )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    market_df = marketplace_analysis(df)

    fig = px.bar(
    market_df,
    x="delay_gap",
    y=market_df.index,
    orientation="h",
    title="Market-wise Delay Analysis"
)

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    st.subheader("⏱ Delay Risk Analysis")

# Histogram
    fig = px.histogram(
    df,
    x="delay_gap",
    nbins=50,
    title="Delay Gap Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

# Risk distribution
    fig2 = px.pie(
    df,
    names="Late_delivery_risk",
    title="Late Delivery Risk Distribution"
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.subheader("Global Delivery Intelligence")


    colA, colB = st.columns(2)

    with colA:
        view_option = st.radio(
        "Shipment View",
        ["All", "Delayed Only", "On-Time Only"],
        horizontal=True
        )

    with colB:
        size_option = st.selectbox(
        "Point Intensity",
        ["Low", "Medium", "High"]
    )
    if view_option == "Delayed Only":
        map_df = df[df["delivery_status_new"] == "Delayed"]
    elif view_option == "On-Time Only":
        map_df = df[df["delivery_status_new"] == "On-Time"]
    else:
        map_df = df.copy()

    map_df = map_df.dropna(subset=["Latitude", "Longitude"])
    map_df = map_df.sample(min(len(map_df), 1500))


    size_map = {
    "Low": 0.1,
    "Medium": 0.2,
    "High": 0.35
    }
    point_size = size_map[size_option]

    region_df = regional_analysis(df)
    worst_region = region_df["delay_gap"].idxmax()

    pointsData = []
    for _, row in map_df.iterrows():
    
  
        if row["Order Region"] == worst_region:
            color = "yellow"   # highlight worst region
        elif row["delivery_status_new"] == "Delayed":
            color = "red"
        elif row["delivery_status_new"] == "On-Time":
            color = "green"
        else:
            color = "blue"

    pointsData.append({
        "lat": row["Latitude"],
        "lng": row["Longitude"],
        "size": point_size,
        "color": color
    })
    worst_points = map_df[map_df["Order Region"] == worst_region].head(5)

    labelsData = [
        {
        "lat": row["Latitude"],
        "lng": row["Longitude"],
        "size": 0.4,
        "color": "yellow",
        "text": f"⚠ {worst_region}"
        }
        for _, row in worst_points.iterrows()
    ]
    streamlit_globe(
    pointsData=pointsData,
    labelsData=labelsData,
    daytime='night',
    width=900,
    height=450
    )


    st.markdown("### Live Map Stats")

    col1, col2, col3 = st.columns(3)

    col1.metric("Points Shown", len(map_df))
    col2.metric("Worst Region", worst_region)
    col3.metric("Avg Delay", f"{df['delay_gap'].mean():.2f} days")


elif selected == "Insights":
    st.subheader("Key Insights")
    region_df = regional_analysis(df)
    mode_df = shipping_mode_analysis(df)
    kpis = calculate_kpis(df)
    worst_mode = mode_df["delay_gap"].idxmax()
    worst_region = region_df["delay_gap"].idxmax()
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div style="
        background: linear-gradient(135deg, #1f1f1f, #2c2c2c);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #ff4b4b;
        ">
        <h3 style='color:#ff4b4b;'> Observations</h3>
        <ul>
            <li>Worst shipping mode: <b>{worst_mode}</b></li>
            <li>Highest delay region: <b>{worst_region}</b></li>
            <li>Avg delay: <b>{kpis['avg_delay']:.2f} days</b></li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="
        background: linear-gradient(135deg, #1f1f1f, #2c2c2c);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #00c896;
        ">
        <h3 style='color:#00c896;'> Recommendations</h3>
        <ul>
            <li>Optimize <b>{worst_mode}</b> routes</li>
            <li>Fix logistics in <b>{worst_region}</b></li>
            <li>Improve SLA monitoring</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)