import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime


st.set_page_config(
    page_title="Blood Bank Inventory Analytics Dashboard",
    page_icon="🩸",
    layout="wide"
)

def load_css():
    with open("Dashboard/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()


st.title("🩸 Blood Bank Inventory Analytics")

st.caption(
    f"Hospital Inventory Monitoring & Decision Support Dashboard | Last Updated: {datetime.now().strftime('%d %b %Y')}"
)

st.markdown("---")

@st.cache_data
def load_data():
    df = pd.read_csv(
        r"C:\Users\Ramapriya Murugesan\Desktop\Blood_Bank_Inventory_Analytics\Dataset\Blood_Bank_Inventory_Feature_Engineered.csv"
    )
    return df

df = load_data()

#Sidebar Filters
st.sidebar.header("🔍 Filters")

hospital = st.sidebar.selectbox(
    "Select Hospital",
    ["All"] + sorted(df["Hospital"].dropna().unique())
)

blood_group = st.sidebar.selectbox(
    "Select Blood Group",
    ["All"] + sorted(df["Blood_Group"].dropna().unique())
)

city = st.sidebar.selectbox(
    "Select City",
    ["All"] + sorted(df["City"].dropna().unique())
)

#Apply Filters
filtered_df = df.copy()

if hospital != "All":
    filtered_df = filtered_df[
        filtered_df["Hospital"] == hospital
    ]

if blood_group != "All":
    filtered_df = filtered_df[
        filtered_df["Blood_Group"] == blood_group
    ]

if city != "All":
    filtered_df = filtered_df[
        filtered_df["City"] == city
    ]
#KPI Section
st.subheader("📊 Key Performance Indicators")

total_inventory = filtered_df["Inventory_Units"].sum()

total_demand = filtered_df["Demand_Units"].sum()

total_used = filtered_df["Units_Used"].sum()

low_stock = filtered_df[
    filtered_df["Inventory_Status"]=="Low Stock"
].shape[0]

near_expiry = filtered_df[
    filtered_df["Days_To_Expiry"]<=7
].shape[0]


col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="kpi-card inventory">
        <div class="kpi-title">🩸 Total Inventory</div>
        <div class="kpi-value">{total_inventory:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card demand">
        <div class="kpi-title">📈 Total Demand</div>
        <div class="kpi-value">{total_demand:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card used">
        <div class="kpi-title">💉 Units Used</div>
        <div class="kpi-value">{total_used:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card low">
        <div class="kpi-title">⚠️ Low Stock</div>
        <div class="kpi-value">{low_stock}</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="kpi-card expiry">
        <div class="kpi-title">⏳ Near Expiry</div>
        <div class="kpi-value">{near_expiry}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

#Interactive Charts

st.subheader("📈 Inventory Performance")

col1,col2 = st.columns(2)

#Blood Group vs Demand

comparison = (
    filtered_df.groupby("Blood_Group")[["Demand_Units", "Inventory_Units"]]
    .sum()
    .reset_index()
)

fig1 = px.bar(
    comparison,
    x="Blood_Group",
    y=["Demand_Units", "Inventory_Units"],
    barmode="group",
    color_discrete_sequence=["#F59E0B", "#2563EB"],
    template="plotly_white",
    text_auto=True,
    title="Demand vs Inventory by Blood Group"
)

fig1.update_layout(
    title_x=0.5,
    title_font=dict(size=20, color="#1E3A8A"),
    font=dict(size=13),
    xaxis_title="Blood Group",
    yaxis_title="Blood Units",
    legend_title="Metrics",
    plot_bgcolor="white",
    paper_bgcolor="white",
    bargap=0.25
)

fig1.update_traces(textposition="outside")




#Blood Group vs Inventory
blood_inventory = (
    filtered_df.groupby("Blood_Group")["Inventory_Units"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig2 = px.bar(
    blood_inventory,
    x="Blood_Group",
    y="Inventory_Units",
    color="Inventory_Units",
    color_continuous_scale="Tealgrn",
    template="plotly_white",
    text="Inventory_Units",
    title="Inventory by Blood Group"
)

fig2.update_layout(
    title_x=0.5,
    title_font=dict(size=20,color="#1E3A8A"),
    font=dict(size=13),
    xaxis_title="Blood Group",
    yaxis_title="Inventory Units",
    coloraxis_showscale=False,
    plot_bgcolor="white",
    paper_bgcolor="white"
)

fig2.update_traces(textposition="outside")


#Hospital Shortage

hospital_shortage = (
    filtered_df.groupby("Hospital")["Stock_Shortage"]
    .sum()
    .sort_values(ascending=True)
    .reset_index()
)

fig3 = px.bar(
    hospital_shortage,
    x="Stock_Shortage",
    y="Hospital",
    orientation="h",
    color="Stock_Shortage",
    color_continuous_scale="Reds",
    template="plotly_white",
    text="Stock_Shortage",
    title="Hospital Inventory Shortages"
)

fig3.update_layout(
    title_x=0.5,
    title_font=dict(size=20,color="#1E3A8A"),
    font=dict(size=13),
    xaxis_title="Shortage Units",
    yaxis_title="Hospital",
    coloraxis_showscale=False,
    plot_bgcolor="white",
    paper_bgcolor="white"
)

fig3.update_traces(textposition="outside")



#City Usage
city_usage = (
    filtered_df.groupby("City")["Units_Used"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig4 = px.bar(
    city_usage,
    x="City",
    y="Units_Used",
    color="Units_Used",
    color_continuous_scale="Blues",
    template="plotly_white",
    text="Units_Used",
    title="City-wise Blood Usage"
)

fig4.update_layout(
    title_x=0.5,
    title_font=dict(size=20,color="#1E3A8A"),
    font=dict(size=13),
    xaxis_title="City",
    yaxis_title="Blood Units Used",
    coloraxis_showscale=False,
    plot_bgcolor="white",
    paper_bgcolor="white"
)

fig4.update_traces(textposition="outside")



#Average Usage Rate by Hospital

usage = (
    filtered_df.groupby("Hospital")["Usage_Rate"]
    .mean()
    .sort_values(ascending=True)
    .reset_index()
)

fig6 = px.bar(
    usage,
    x="Usage_Rate",
    y="Hospital",
    orientation="h",
    color="Usage_Rate",
    color_continuous_scale="Greens",
    template="plotly_white",
    text="Usage_Rate",
    title="Average Blood Usage Rate by Hospital"
)

fig6.update_layout(
    title_x=0.5,
    title_font=dict(size=20,color="#1E3A8A"),
    font=dict(size=13),
    xaxis_title="Usage Rate (%)",
    yaxis_title="Hospital",
    coloraxis_showscale=False,
    plot_bgcolor="white",
    paper_bgcolor="white"
)

fig6.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)


#Inventory Redistribution
redistribution = (
    filtered_df.groupby("Hospital")[["Stock_Excess", "Stock_Shortage"]]
    .sum()
    .reset_index()
)

fig7 = px.bar(
    redistribution,
    x="Hospital",
    y=["Stock_Excess", "Stock_Shortage"],
    barmode="group",
    color_discrete_sequence=["#22C55E", "#DC2626"],
    template="plotly_white",
    text_auto=True,
    title="Inventory Redistribution Analysis"
)

fig7.update_layout(
    title_x=0.5,
    title_font=dict(size=20,color="#1E3A8A"),
    font=dict(size=13),
    xaxis_title="Hospital",
    yaxis_title="Blood Units",
    legend_title="Inventory Status",
    plot_bgcolor="white",
    paper_bgcolor="white",
    bargap=0.25
)

fig7.update_traces(textposition="outside")



#Layout

st.subheader("📊 Blood Inventory Analytics")

# Row 1
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)

# Row 2
col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.plotly_chart(fig4, use_container_width=True)

# Row 3
col5, col6 = st.columns(2)

with col5:
    st.plotly_chart(fig6, use_container_width=True)

with col6:
    st.plotly_chart(fig7, use_container_width=True)
    
st.markdown("---")

#Hospital Performance Summary

st.markdown("---")

st.subheader("🏥 Hospital Performance Summary")

summary = (
    filtered_df.groupby("Hospital")
    .agg(
        Inventory=("Inventory_Units","sum"),
        Demand=("Demand_Units","sum"),
        Used=("Units_Used","sum"),
        Shortage=("Stock_Shortage","sum"),
        Excess=("Stock_Excess","sum")
    )
    .reset_index()
)

st.dataframe(summary, use_container_width=True)

#Operational Recommendations

st.markdown("---")

st.subheader("💡 Operational Recommendations")

recommendations = pd.DataFrame({
    "Priority": [
        "High",
        "High",
        "Medium",
        "High",
        "Medium"
    ],
    "Recommendation": [
        "Increase A+ blood donation campaigns",
        "Replenish inventory at MGM Hospital",
        "Monitor blood units nearing expiry",
        "Redistribute excess stock between hospitals",
        "Review inventory weekly to reduce shortages"
    ]
})

st.dataframe(recommendations, use_container_width=True)

#Key Business Insights

st.markdown("---")

st.subheader("📌 Key Business Insights")

highest_demand = (
    filtered_df.groupby("Blood_Group")["Demand_Units"]
    .sum()
    .idxmax()
)

highest_inventory = (
    filtered_df.groupby("Blood_Group")["Inventory_Units"]
    .sum()
    .idxmax()
)

highest_usage_city = (
    filtered_df.groupby("City")["Units_Used"]
    .sum()
    .idxmax()
)

highest_shortage = (
    filtered_df.groupby("Hospital")["Stock_Shortage"]
    .sum()
    .idxmax()
)

st.info(f"""
• **Highest Demand Blood Group:** {highest_demand}

• **Highest Available Inventory:** {highest_inventory}

• **Highest Blood Usage City:** {highest_usage_city}

• **Hospital with Highest Shortage:** {highest_shortage}

• Inventory monitoring helps reduce shortages and optimize blood availability.
""")

st.markdown("---")



#Executive Summary

st.markdown("---")

st.subheader("📄 Executive Summary")

st.success("""
This dashboard provides a centralized view of blood inventory across hospitals.

The analysis helps healthcare administrators:

• Monitor blood demand and inventory.

• Identify hospitals with inventory shortages.

• Optimize blood redistribution.

• Improve emergency blood availability.

• Support informed operational decisions using data.
""")

#Footer


st.markdown("---")

st.markdown("""
<div style="text-align:center;color:gray">

Blood Bank Inventory Analytics Dashboard

Developed using Python • Pandas • Plotly • Streamlit

</div>
""", unsafe_allow_html=True)