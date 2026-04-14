import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# Page configuration
# ---------------------------
st.set_page_config(
    page_title="State Demographics Dashboard",
    layout="wide"
)

st.title("📊 State Demographics Dashboard")
st.markdown("Explore population and income trends across U.S. states.")

# ---------------------------
# Data load
# ---------------------------
df = pd.read_csv("state_data.csv")

# ---------------------------
# Sidebar: Filters
# ---------------------------
st.sidebar.header("🔎 Filters")

state = st.sidebar.selectbox(
    "State",
    sorted(df["State"].unique())
)

demographic = st.sidebar.selectbox(
    "Demographic",
    ["Total Population", "Median Household Income"]
)

year = st.sidebar.selectbox(
    "Year",
    sorted(df["Year"].unique())
)

# ---------------------------
# Tabs
# ---------------------------
tab_trend, tab_map, tab_table = st.tabs(
    ["📈 Trends", "🗺️ Map View", "📋 Data Table"]
)

# ---------------------------
# Trend Tab
# ---------------------------
with tab_trend:
    st.subheader(f"{demographic} Trend — {state}")

    col1, col2 = st.columns([3, 1])

    with col1:
        df_state = df[df["State"] == state]

        fig = px.line(
            df_state,
            x="Year",
            y=demographic,
            markers=True,
            title=f"{demographic} Over Time"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        latest_value = df_state.sort_values("Year").iloc[-1][demographic]
        st.metric(
            label="Latest Value",
            value=f"{latest_value:,.0f}" if demographic == "Total Population" else f"${latest_value:,.0f}"
        )

# ---------------------------
# Map Tab
# ---------------------------
with tab_map:
    st.subheader(f"{demographic} by State — {year}")

    df_year = df[df["Year"] == year]

    fig = px.choropleth(
        df_year,
        locations="State Abbrev",
        locationmode="USA-states",
        color=demographic,
        scope="usa",
        title=f"{demographic} ({year})",
        color_continuous_scale="viridis"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Data Table Tab
# ---------------------------
with tab_table:
    st.subheader("Underlying Data")
    df_filtered = df[df["State"] == state]
    st.dataframe(df_filtered, use_container_width=True)

    col1, col2 = st.columns([1, 3])
    with col1:
        st.download_button(
            "⬇️ Download CSV",
            df.to_csv(index=False).encode("utf-8"),
            "state_data.csv",
            "text/csv"
        )

