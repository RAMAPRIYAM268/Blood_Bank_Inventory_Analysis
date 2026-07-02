import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from streamlit_option_menu import option_menu

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Blood Bank Inventory Analytics",
    page_icon="🩸",
    layout="wide"
)

# =========================================================
# PROFESSIONAL CSS
# =========================================================

st.markdown("""
<style>

.stApp{
    background:#F8FAFC;
}

h1,h2,h3{
    color:#7F1D1D;
}

/* KPI Cards */
[data-testid="metric-container"]{
    background:white;
    border-left:6px solid #B91C1C;
    border-radius:12px;
    padding:18px;
    box-shadow:0px 3px 10px rgba(0,0,0,0.08);
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:white;
}

/* Tables */
thead tr th{
    background:#B91C1C !important;
    color:white !important;
    text-align:center;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TITLE
# =========================================================

st.title("🩸 Blood Bank Inventory Analytics Dashboard")

st.caption(
    f"Executive Decision Support Dashboard | Last Updated : {datetime.now().strftime('%d %b %Y')}"
)

st.markdown("---")

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        r"C:\Users\Ramapriya Murugesan\Desktop\Blood_Bank_Inventory_Analytics\Dataset\Blood_Bank_Inventory_Feature_Engineered.csv"
    )

    return df


df = load_data()

# =========================================================
# SIDEBAR FILTERS
# =========================================================

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

# =========================================================
# APPLY FILTERS
# =========================================================

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

# =========================================================
# KPI CALCULATIONS
# =========================================================

inventory = filtered_df["Inventory_Units"].sum()

demand = filtered_df["Demand_Units"].sum()

used = filtered_df["Units_Used"].sum()

near_expiry = filtered_df[
    filtered_df["Days_To_Expiry"] <= 7
].shape[0]

shortage = filtered_df["Stock_Shortage"].sum()

fulfillment = (
    (used / demand) * 100
    if demand > 0 else 0
)

health = (
    (inventory / (inventory + shortage)) * 100
    if (inventory + shortage) > 0 else 0
)
# =========================================================
# CHART 1 : Inventory vs Demand by Blood Group
# =========================================================

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
    template="plotly_white",
    paper_bgcolor="white",
    plot_bgcolor="white",
    height=450,
    title_x=0.02
)

# =========================================================
# CHART 2 : Hospital Stock Shortage
# =========================================================

hospital_shortage = (
    filtered_df.groupby("Hospital")["Stock_Shortage"]
    .sum()
    .sort_values()
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
    template="plotly_white",
    paper_bgcolor="white",
    plot_bgcolor="white",
    height=450,
    title_x=0.02
)

# =========================================================
# CHART 3 : Near Expiry Blood Units
# =========================================================

expiry = (
    filtered_df[
        filtered_df["Days_To_Expiry"] <= 7
    ]
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
    color_continuous_scale="Reds",
    title="Near Expiry Blood Units"
)

fig3.update_traces(textposition="outside")

fig3.update_layout(
    template="plotly_white",
    paper_bgcolor="white",
    plot_bgcolor="white",
    height=450,
    title_x=0.02
)

# =========================================================
# CHART 4 : Inventory Health by Hospital
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
    )
) * 100

fig4 = px.bar(
    health_df,
    x="Hospital",
    y="Inventory_Health",
    text="Inventory_Health",
    color="Inventory_Health",
    color_continuous_scale="Reds",
    title="Inventory Health by Hospital"
)

fig4.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig4.update_layout(
    template="plotly_white",
    paper_bgcolor="white",
    plot_bgcolor="white",
    height=450,
    title_x=0.02
)

# =========================================================
# CHART 5 : Demand Fulfillment
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
    color_continuous_scale="Reds",
    title="Demand Fulfillment by Blood Group"
)

fig5.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig5.update_layout(
    template="plotly_white",
    paper_bgcolor="white",
    plot_bgcolor="white",
    height=450,
    title_x=0.02
)

fig5.update_yaxes(range=[0,110])
# =========================================================
# BUSINESS INSIGHTS
# =========================================================

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
    filtered_df[
        filtered_df["Days_To_Expiry"] <= 7
    ]
    .groupby("Blood_Group")
    .size()
    .idxmax()
)

# =========================================================
# HOSPITAL PERFORMANCE SUMMARY
# =========================================================

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

# =========================================================
# STATUS INDICATORS
# =========================================================

inventory_status = (
    "🟢 Healthy"
    if health >= 85
    else "🟡 Moderate"
    if health >= 70
    else "🔴 Critical"
)

fulfillment_status = (
    "🟢 On Target"
    if fulfillment >= 90
    else "🟡 Needs Improvement"
)

expiry_status = (
    "🟢 Low Risk"
    if near_expiry < 20
    else "🔴 High Risk"
)
# =========================================================
# WEBSITE NAVIGATION
# =========================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 Executive Dashboard",
    "📦 Inventory Analytics",
    "🏥 Hospital Performance",
    "📈 Executive Insights"
])
with tab1:

        st.header("🏠 Executive Dashboard")

        st.markdown("### Key Performance Indicators")

        c1, c2, c3, c4, c5 = st.columns(5)

        with c1:
            st.metric(
                "🩸 Inventory",
                f"{inventory:,}"
            )

        with c2:
            st.metric(
                "📈 Fulfillment",
                f"{fulfillment:.1f}%"
            )

        with c3:
            st.metric(
                "⚠ Near Expiry",
                near_expiry
            )

        with c4:
            st.metric(
                "🚑 Shortage",
                f"{shortage:,}"
            )

        with c5:
            st.metric(
                "❤️ Health",
                f"{health:.1f}%"
            )

        st.markdown("---")

        st.subheader("🚨 Operational Alerts")

        st.error(
                f"Highest stock shortage is observed at **{highest_shortage}**."
            )
        st.warning(
                f"**{expiry_group}** has the highest number of near-expiry blood units."
            )

        st.info(
                f"Current demand fulfillment is **{fulfillment:.1f}%**."
            )

        st.markdown("---")

        st.subheader("📊 Executive Snapshot")

        left, right = st.columns(2)

        with left:
            st.metric(
                    "Inventory Status",
                    inventory_status
                )

            st.metric(
                    "Demand Fulfillment",
                    fulfillment_status
                )

        with right:
            st.metric(
                    "Expiry Risk",
                    expiry_status
                )

            st.metric(
                    "Highest Demand",
                    highest_demand
                )
# =========================================================
# TAB 2 : INVENTORY ANALYTICS
# =========================================================

with tab2:

    st.header("📦 Inventory Analytics")
    st.caption("Monitor inventory availability, demand fulfillment, and expiry risks.")

    # ------------------------------
    # Inventory vs Demand & Near Expiry
    # ------------------------------

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    st.markdown("---")

        # ------------------------------
        # Demand Fulfillment
        # ------------------------------

    st.plotly_chart(
        fig5,
        use_container_width=True
    )


# =========================================================
# TAB 3 : HOSPITAL PERFORMANCE
# =========================================================

with tab3:

    st.header("🏥 Hospital Performance")
    st.caption("Analyze hospital inventory health and stock shortages.")

    # ------------------------------
    # Hospital Charts
    # ------------------------------

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            fig4,
            use_container_width=True
        )

    st.markdown("---")

    # ------------------------------
    # Hospital Performance Summary
    # ------------------------------

    st.subheader("🏥 Hospital Performance Summary")

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )
    # =========================================================
# TAB 4 : EXECUTIVE INSIGHTS
# =========================================================

with tab4:

    st.header("📈 Executive Insights")

    st.markdown("### 📌 Business Summary")

    st.success(f"""
### Executive Business Insights

**Demand Analysis**
- Peak demand is observed for **{highest_demand}** blood group.

**Inventory Status**
- Highest inventory availability is for **{highest_inventory}** blood group.

**Operational Alert**
- **{highest_shortage}** requires immediate stock replenishment due to the highest shortage.

**Utilization Analysis**
- **{highest_usage_city}** records the highest blood utilization.

**Expiry Monitoring**
- **{expiry_group}** has the highest number of near-expiry units.

**Demand Fulfillment**
- Overall demand fulfillment is **{fulfillment:.1f}%**.

**Inventory Health**
- Current inventory health score is **{health:.1f}%**.
""")

    st.markdown("---")

    st.subheader("💡 Strategic Recommendations")

    col1, col2 = st.columns(2)

    with col1:

        st.success(
            f"Increase blood collection campaigns for **{highest_demand}**."
        )

        st.warning(
            f"Allocate additional inventory to **{highest_shortage}**."
        )

        st.info(
            f"Prioritize utilization of **{expiry_group}** blood units."
        )

    with col2:

        st.success(
            "Implement inter-hospital stock balancing."
        )

        st.success(
            "Monitor KPI trends weekly for better operational planning."
        )

        st.success(
            "Conduct monthly inventory health reviews."
        )

    st.markdown("---")

    st.subheader("📄 Executive Summary")

    st.info(f"""
    ### Overall Performance

    🟢 **Inventory Health:** **{health:.1f}%** ({inventory_status})

    🟢 **Demand Fulfillment:** **{fulfillment:.1f}%** ({fulfillment_status})

    🟠 **Near Expiry Units:** **{near_expiry}** ({expiry_status})

    ---

    ### Management Priorities

    • Maintain adequate inventory for high-demand blood groups.

    • Reduce shortages through proactive replenishment.

    • Minimize expiry-related wastage.

    • Improve inventory balancing across hospitals.

    • Continuously monitor operational KPIs.
    """)

    # =========================================================
    # FOOTER
    # =========================================================

    st.markdown("---")

    st.markdown("""
    <div style="
    text-align:center;
    padding:18px;
    font-size:15px;
    color:#6B7280;
    ">

    🩸 <b>Blood Bank Inventory Analytics Dashboard</b><br>

    Executive Decision Support Dashboard

    <br><br>

    Developed using <b>Python • Streamlit • Plotly • Pandas</b>

    </div>
    """, unsafe_allow_html=True)