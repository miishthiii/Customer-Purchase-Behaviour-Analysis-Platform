import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Customer Intelligence Platform",
    layout="wide",
    page_icon="📊"
)

# =========================================================
# LOAD DEFAULT DATA
# =========================================================
@st.cache_data
def load_default_data():
    df = pd.read_csv("data/customer_data.csv")
    df["Total_Spend"] = df["Quantity"] * df["Price"]
    return df

# Load default initially
if "df" not in st.session_state:
    st.session_state.df = load_default_data()

df = st.session_state.df

# =========================================================
# SIDEBAR FILTERS ONLY
# =========================================================
st.sidebar.title("🔎 Filters")

category_filter = st.sidebar.multiselect(
    "Product Category",
    options=df["Product_Category"].unique(),
    default=df["Product_Category"].unique()
)

discount_filter = st.sidebar.multiselect(
    "Discount Applied",
    options=df["Discount_Applied"].unique(),
    default=df["Discount_Applied"].unique()
)

filtered_df = df[
    (df["Product_Category"].isin(category_filter)) &
    (df["Discount_Applied"].isin(discount_filter))
]

# =========================================================
# MAIN TITLE
# =========================================================
st.title("📊 Customer Purchase Behaviour Analysis Platform")

st.markdown("## 📌 Executive Summary")
st.info("Analyze customer behavior across income, age, category, and discount factors.")

# =========================================================
# TABS
# =========================================================
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📂 Data Upload", "📄 Dataset View"])

# =========================================================
# TAB 1 — DASHBOARD
# =========================================================
with tab1:

    # KPIs
    total_revenue = filtered_df["Total_Spend"].sum()
    avg_spend = filtered_df["Total_Spend"].mean()
    high_income_spend = filtered_df[filtered_df["Income"] > 60000]["Total_Spend"].sum()
    discount_revenue = filtered_df[filtered_df["Discount_Applied"] == "Yes"]["Total_Spend"].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
    col2.metric("Average Spend", f"₹{avg_spend:,.0f}")
    col3.metric("High Income Revenue", f"₹{high_income_spend:,.0f}")
    col4.metric("Discount Revenue", f"₹{discount_revenue:,.0f}")

    st.divider()

    # Age vs Spend
    st.subheader("Age vs Total Spend")
    fig1, ax1 = plt.subplots()
    sns.scatterplot(x="Age", y="Total_Spend", data=filtered_df, ax=ax1)
    st.pyplot(fig1)

    # Income Regression
    st.subheader("Income vs Total Spend")
    fig2, ax2 = plt.subplots()
    sns.regplot(x="Income", y="Total_Spend", data=filtered_df, ax=ax2)
    st.pyplot(fig2)

    # Revenue by Category
    st.subheader("Revenue by Product Category")
    fig3, ax3 = plt.subplots()
    filtered_df.groupby("Product_Category")["Total_Spend"].sum().plot(kind="bar", ax=ax3)
    st.pyplot(fig3)

    # Discount Impact
    st.subheader("Discount Impact on Spending")
    fig4, ax4 = plt.subplots()
    sns.boxplot(x="Discount_Applied", y="Total_Spend", data=filtered_df, ax=ax4)
    st.pyplot(fig4)

    # Heatmap
    st.subheader("Correlation Heatmap")
    fig5, ax5 = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        filtered_df.select_dtypes(include="number").corr(),
        annot=True,
        cmap="coolwarm",
        ax=ax5
    )
    st.pyplot(fig5)

# =========================================================
# TAB 2 — DATA UPLOAD
# =========================================================
with tab2:

    st.subheader("📂 Upload New Dataset")

    uploaded_file = st.file_uploader(
        "Drop your CSV file here",
        type=["csv"]
    )

    if uploaded_file is not None:
        new_df = pd.read_csv(uploaded_file)

        if "Total_Spend" not in new_df.columns:
            new_df["Total_Spend"] = new_df["Quantity"] * new_df["Price"]

        st.session_state.df = new_df
        st.success("New dataset loaded successfully!")

# =========================================================
# TAB 3 — DATASET VIEW
# =========================================================
with tab3:

    st.subheader("📄 Full Dataset View")
    st.dataframe(df)

    st.markdown("### Dataset Summary Statistics")
    st.write(df.describe())
