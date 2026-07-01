import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Blood Bank Inventory Analytics",
    page_icon="🩸",
    layout="wide"
)

# ---------------------------------------------------------
# Professional Theme
# ---------------------------------------------------------

st.markdown("""
<style>

/* Background */
.stApp{
    background-color:#F8FAFC;
}

/* KPI Cards */
[data-testid="metric-container"]{
    background:white;
    border-left:6px solid #B91C1C;
    border-radius:12px;
    padding:18px;
    box-shadow:0px 2px 10px rgba(0,0,0,0.08);
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#FFFFFF;
}

/* Tables */
thead tr th{
    background:#B91C1C !important;
    color:white !important;
}

h1,h2,h3{
    color:#7F1D1D;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Dashboard Title
# ---------------------------------------------------------

st.title("🩸 Blood Bank Inventory Analytics Dashboard")

st.caption(
    f"Hospital Inventory Monitoring & Decision Support Dashboard | Last Updated : {datetime.now().strftime('%d %b %Y')}"
)

st.markdown("---")

# ---------------------------------------------------------
# Load Dataset
# ---------------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv(
        r"C:\Users\Ramapriya Murugesan\Desktop\Blood_Bank_Inventory_Analytics\Dataset\Blood_Bank_Inventory_Feature_Engineered.csv"
    )

    return df

df = load_data()

# ---------------------------------------------------------
# Common Plot Style
# ---------------------------------------------------------

def style_chart(fig):

    fig.update_layout(

        template="plotly_white",

        paper_bgcolor="white",

        plot_bgcolor="white",

        height=450,

        font=dict(
            family="Segoe UI",
            size=13,
            color="#1F2937"
        ),

        title=dict(
            font=dict(
                size=20,
                color="#7F1D1D"
            ),
            x=0.02
        ),

        legend=dict(
            orientation="h",
            y=1.05,
            x=0
        ),

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),

        xaxis=dict(
            showgrid=False,
            linecolor="#E5E7EB"
        ),

        yaxis=dict(
            gridcolor="#E5E7EB",
            zeroline=False
        )

    )

    return fig

# ---------------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------------

st.sidebar.title("🔍 Dashboard Filters")

hospital = st.sidebar.selectbox(
    "Hospital",
    ["All"] + sorted(df["Hospital"].dropna().unique())
)

blood_group = st.sidebar.selectbox(
    "Blood Group",
    ["All"] + sorted(df["Blood_Group"].dropna().unique())
)

city = st.sidebar.selectbox(
    "City",
    ["All"] + sorted(df["City"].dropna().unique())
)

# ---------------------------------------------------------
# Apply Filters
# ---------------------------------------------------------

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

# ---------------------------------------------------------
# KPI Section
# ---------------------------------------------------------
inventory=filtered_df["Inventory_Units"].sum()

demand=filtered_df["Demand_Units"].sum()

used=filtered_df["Units_Used"].sum()

near_expiry=filtered_df[
filtered_df["Days_To_Expiry"]<=7
].shape[0]

shortage=filtered_df["Stock_Shortage"].sum()

fulfillment=(used/demand)*100

health=(inventory/(inventory+shortage))*100


st.subheader("Executive KPIs")

c1,c2,c3,c4,c5=st.columns(5)

c1.metric(
"🩸 Inventory",
f"{inventory:,}"
)

c2.metric(
"📈 Fulfillment",
f"{fulfillment:.1f}%"
)

c3.metric(
"⚠ Near Expiry",
near_expiry
)

c4.metric(
"🚑 Shortage",
f"{shortage:,}"
)

c5.metric(
"❤ Inventory Health",
f"{health:.1f}%"
)


st.markdown("---")

# ---------------------------------------------------------
# Interactive Charts
# ---------------------------------------------------------

st.subheader("📈 Blood Inventory Performance")

# =========================================================
# CHART 1 : Demand vs Inventory by Blood Group
# =========================================================

st.subheader("📊 Blood Inventory Analysis")

comparison = (
    filtered_df.groupby("Blood_Group")[["Inventory_Units", "Demand_Units"]]
    .sum()
    .reset_index()
)

fig1 = px.bar(
    comparison,
    x="Blood_Group",
    y=["Inventory_Units", "Demand_Units"],
    barmode="group",
    color_discrete_sequence=["#B91C1C", "#F59E0B"],
    title="Inventory vs Demand by Blood Group"
)

fig1.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    title_x=0.25,
    font=dict(size=13)
)


# =========================================================
# CHART 2: Hospital Stock Shortage
# =========================================================


hospital_shortage = (
    filtered_df.groupby("Hospital")["Stock_Shortage"]
    .sum()
    .sort_values(ascending=True)
    .reset_index()
)

fig2 = px.bar(
    hospital_shortage,
    x="Stock_Shortage",
    y="Hospital",
    orientation="h",
    text="Stock_Shortage",
    color="Stock_Shortage",
    color_continuous_scale="Reds",
    title="Hospital-wise Stock Shortage"
)

fig2.update_traces(textposition="outside")

fig2.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white"
)

# =========================================================
# CHART 3: Near Expiry Blood Units
# =========================================================


expiry = (
    filtered_df[filtered_df["Days_To_Expiry"] <= 7]
    .groupby("Blood_Group")
    .size()
    .reset_index(name="Near_Expiry_Units")
)

fig3 = px.bar(
    expiry,
    x="Blood_Group",
    y="Near_Expiry_Units",
    text="Near_Expiry_Units",
    color="Near_Expiry_Units",
    color_continuous_scale="Oranges",
    title="Near Expiry Blood Units"
)

fig3.update_traces(textposition="outside")

fig3.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white"
)

# =========================================================
# CHART 4: Inventory Health by Hospital
# =========================================================

health_df = (
    filtered_df.groupby("Hospital")
    .agg({
        "Inventory_Units":"sum",
        "Stock_Shortage":"sum"
    })
    .reset_index()
)

health_df["Inventory_Health"] = (
    health_df["Inventory_Units"] /
    (
        health_df["Inventory_Units"] +
        health_df["Stock_Shortage"]
    ) * 100
)

fig4 = px.bar(
    health_df,
    x="Hospital",
    y="Inventory_Health",
    text="Inventory_Health",
    color="Inventory_Health",
    color_continuous_scale="Greens",
    title="Inventory Health by Hospital"
)

fig4.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig4.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white"
)

# =========================================================
# CHART 5 : Demand Fulfillment by Blood Group
# =========================================================
fulfillment_df = (
    filtered_df.groupby("Blood_Group")
    .agg({
        "Demand_Units":"sum",
        "Units_Used":"sum"
    })
    .reset_index()
)

fulfillment_df["Demand_Fulfillment"] = (
    fulfillment_df["Units_Used"] /
    fulfillment_df["Demand_Units"]
) * 100

fig5 = px.bar(
    fulfillment_df,
    x="Blood_Group",
    y="Demand_Fulfillment",
    text="Demand_Fulfillment",
    color="Demand_Fulfillment",
    color_continuous_scale="Blues",
    title="Demand Fulfillment by Blood Group"
)

fig5.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig5.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white"
)

# =========================================================
# DASHBOARD LAYOUT
# =========================================================


row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.plotly_chart(fig1, use_container_width=True)

with row1_col2:
    st.plotly_chart(fig2, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.plotly_chart(fig3, use_container_width=True)

with row2_col2:
    st.plotly_chart(fig4, use_container_width=True)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

# ==========================================================
# BUSINESS INSIGHTS
# ==========================================================
st.subheader("📌 Business Insights")

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


highest_shortage = (
    filtered_df.groupby("Hospital")["Stock_Shortage"]
    .sum()
    .idxmax()
)

highest_usage_city = (
    filtered_df.groupby("City")["Units_Used"]
    .sum()
    .idxmax()
)

expiry_group = (
    filtered_df[filtered_df["Days_To_Expiry"] <= 7]
    .groupby("Blood_Group")
    .size()
    .idxmax()
)

st.info(f"""

### 📊 Executive Insights

🩸 **Highest Demand Blood Group:** **{highest_demand}**

🏥 **Highest Available Inventory:** **{highest_inventory}**

🚑 **Hospital with Highest Shortage:** **{highest_shortage}**

🌍 **Highest Blood Utilization City:** **{highest_usage_city}**

⚠️ **Highest Expiry Risk Blood Group:** **{expiry_group}**

📈 **Demand Fulfillment Rate:** **{fulfillment:.1f}%**

❤️ **Inventory Health Score:** **{health:.1f}%**

""")



# ==========================================================
# Operational Recommendations
# ==========================================================


st.subheader("💡 Operational Recommendations")

st.success(
    f"Increase donation campaigns for **{highest_demand}** blood group to meet rising demand."
)

st.warning(
    f"Prioritize replenishment for **{highest_shortage}** hospital to reduce stock shortages."
)

st.info(
    f"Utilize or redistribute **{expiry_group}** blood units before expiry to minimize wastage."
)

st.success(
    "Review inventory levels weekly and redistribute excess stock between hospitals."
)

st.success(
    "Monitor demand fulfillment regularly to improve emergency blood availability."
)


# ==========================================================
# Hospital Performance Summary
# ==========================================================

st.markdown("---")

st.subheader("🏥 Hospital Performance Summary")

summary = (
    filtered_df.groupby("Hospital")
    .agg(
        Total_Inventory=("Inventory_Units","sum"),
        Total_Demand=("Demand_Units","sum"),
        Units_Used=("Units_Used","sum"),
        Stock_Shortage=("Stock_Shortage","sum"),
        Stock_Excess=("Stock_Excess","sum"),
        Avg_Usage_Rate=("Usage_Rate","mean")
    )
    .reset_index()
)

summary["Avg_Usage_Rate"] = summary["Avg_Usage_Rate"].round(1)
st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)


# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================


st.markdown("---")

st.subheader("📄 Executive Summary")
inventory_status = "Healthy" if health >= 85 else "Needs Improvement"

demand_status = "Good" if fulfillment >= 90 else "Needs Attention"

expiry_status = "Low" if near_expiry < 20 else "High"

st.success(f"""
### Overall Inventory Status

• **Inventory Health:** {health:.1f}% ({inventory_status})

• **Demand Fulfillment:** {fulfillment:.1f}% ({demand_status})

• **Near Expiry Blood Units:** {near_expiry} ({expiry_status} Risk)

### Key Findings

✔ Blood demand is highest for **{highest_demand}**.

✔ **{highest_shortage}** requires immediate inventory replenishment.

✔ **{expiry_group}** blood units should be utilized or redistributed before expiry.

✔ **{highest_usage_city}** has the highest blood utilization.

### Recommended Actions

• Increase donation campaigns for high-demand blood groups.

• Redistribute excess blood inventory between hospitals.

• Prioritize usage of near-expiry blood units.

• Review inventory levels weekly.

• Monitor demand fulfillment to improve emergency preparedness.

""")



st.markdown("---")

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("""
<div style='text-align:center;
padding:15px;
font-size:15px;
color:gray;'>

🩸 <b>Blood Bank Inventory Analytics Dashboard</b><br>

Developed using Python • Pandas • Plotly • Streamlit

</div>
""",unsafe_allow_html=True)