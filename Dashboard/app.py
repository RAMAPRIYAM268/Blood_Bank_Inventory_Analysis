import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Blood Bank Inventory Analytics Dashboard",
    page_icon="🩸",
    layout="wide"
)
st.title("🏥 Blood Bank Inventory Analytics Dashboard")

st.markdown("### Monitor Blood Inventory, Demand, Usage, and Shortages")

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

expired_units = filtered_df[
    filtered_df["Expiry_Status"]=="Expired"
].shape[0]

low_stock = filtered_df[
    filtered_df["Inventory_Status"]=="Low Stock"
].shape[0]

col1,col2,col3,col4,col5 = st.columns(5)

with col1:
    st.metric("🩸 Total Inventory",total_inventory)

with col2:
    st.metric("📈 Total Demand",total_demand)

with col3:
    st.metric("💉 Units Used",total_used)

with col4:
    st.metric("⚠️ Expired Units",expired_units)

with col5:
    st.metric("🏥 Low Stock",low_stock)
    
st.markdown("---")
#Interactive Charts
st.subheader("📈 Blood Bank Analytics")

col1,col2 = st.columns(2)
#Blood Group vs Demand
blood_demand = filtered_df.groupby("Blood_Group")["Demand_Units"].sum().reset_index()

fig1 = px.bar(
    blood_demand,
    x="Blood_Group",
    y="Demand_Units",
    color="Blood_Group",
    title="Blood Group vs Demand"
)

with col1:
    st.plotly_chart(fig1,use_container_width=True)
#Blood Group vs Inventory
blood_inventory = filtered_df.groupby("Blood_Group")["Inventory_Units"].sum().reset_index()

fig2 = px.bar(
    blood_inventory,
    x="Blood_Group",
    y="Inventory_Units",
    color="Blood_Group",
    title="Blood Group vs Inventory"
)

with col2:
    st.plotly_chart(fig2,use_container_width=True)

col3,col4 = st.columns(2)
#Hospital Shortage
hospital_shortage = filtered_df.groupby("Hospital")["Stock_Shortage"].sum().reset_index()

fig3 = px.bar(
    hospital_shortage,
    x="Hospital",
    y="Stock_Shortage",
    color="Hospital",
    title="Hospital Inventory Shortages"
)

with col3:
    st.plotly_chart(fig3,use_container_width=True)

#City Usage
city_usage = filtered_df.groupby("City")["Units_Used"].sum().reset_index()

fig4 = px.bar(
    city_usage,
    x="City",
    y="Units_Used",
    color="City",
    title="City-wise Blood Usage"
)

with col4:
    st.plotly_chart(fig4,use_container_width=True)
    
col5,col6 = st.columns(2)
#Expired vs Valid
expiry = filtered_df["Expiry_Status"].value_counts().reset_index()

expiry.columns=["Expiry_Status","Count"]

fig5 = px.pie(
    expiry,
    names="Expiry_Status",
    values="Count",
    title="Expired vs Valid Blood Units"
)

with col5:
    st.plotly_chart(fig5,use_container_width=True)
    
#Near Expiry
near = filtered_df[
    filtered_df["Days_To_Expiry"]<=7
]

near = near.groupby("Blood_Group").size().reset_index(name="Units")

fig6 = px.bar(
    near,
    x="Blood_Group",
    y="Units",
    color="Blood_Group",
    title="Blood Units Near Expiry"
)

with col6:
    st.plotly_chart(fig6,use_container_width=True)

col7,col8 = st.columns(2)
#Usage Rate
usage = filtered_df.groupby("Hospital")["Usage_Rate"].mean().reset_index()

fig7 = px.bar(
    usage,
    x="Hospital",
    y="Usage_Rate",
    color="Hospital",
    title="Average Usage Rate by Hospital"
)

with col7:
    st.plotly_chart(fig7,use_container_width=True)
    
#Inventory Redistribution
redistribution = filtered_df.groupby("Hospital")[["Stock_Excess","Stock_Shortage"]].sum().reset_index()

fig8 = px.bar(
    redistribution,
    x="Hospital",
    y=["Stock_Excess","Stock_Shortage"],
    barmode="group",
    title="Inventory Redistribution"
)

with col8:
    st.plotly_chart(fig8,use_container_width=True)
    
st.markdown("---")
#Business Recommendations
st.subheader("💡 Business Recommendations")

st.success("""
✅ Increase A+ blood donation campaigns to meet high demand.

✅ Prioritize MGM Hospital for inventory replenishment.

✅ Implement the FEFO (First Expiry First Out) policy to reduce blood wastage.

✅ Redistribute excess inventory from hospitals with surplus stock to hospitals experiencing shortages.

✅ Continuously monitor units nearing expiry and prioritize their usage.
""")

st.markdown("---")
#Dataset Preview
st.subheader("📋 Dataset Preview")

st.dataframe(filtered_df)
st.markdown("---")
#Project Summary
st.subheader("📌 Project Summary")

st.info("""
This dashboard analyzes blood inventory, demand, usage, shortages, and expiry trends.

Key insights help hospitals:
\n• Reduce blood wastage

\n• Prevent inventory shortages

\n• Improve blood availability during emergencies

\n• Optimize inventory planning

\n• Support data-driven healthcare decisions
""")