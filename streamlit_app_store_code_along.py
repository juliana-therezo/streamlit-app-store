import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------
st.title("Supermarket Sales Dashboard")
st.write("This dashboard allow us to explore supermarket sales data using interactive Streamlit widgets.")

st.divider()

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv(
        "https://raw.githubusercontent.com/data-bootcamp-v4/data/main/supermarket_sales.csv"
    )

    df["Date"] = pd.to_datetime(df["Date"])

    return df


df = load_data()

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------
st.sidebar.header("Filters")

#City

selected_city = st.sidebar.selectbox("Select a City", options = ["All"] + list(df["City"].unique()))

#Gender
selected_gender = st.sidebar.radio("Select a Gender", options = ["All"] + list(df["Gender"].unique()))

#Rating
min_rating =st.sidebar.slider("Minimum Rating", min_value = 0, max_value = 10, value = 5, step = 3)

# Payment Method
selected_payment = st.sidebar.multiselect("Select Payment Method", options = df["Payment"].unique(), default = df["Payment"].unique())

# ---------------------------------------------------
# FILTER DATAFRAME
# ---------------------------------------------------
filtered_df = df.copy()

#City
if selected_city != "All":
    filtered_df = filtered_df[filtered_df["City"] == selected_city]

#Gender
if selected_gender != "All":
    filtered_df = filtered_df[filtered_df["Gender"] == selected_gender] 

#Rating
filtered_df = filtered_df[filtered_df["Rating"] >= min_rating]

#Payment Method
if selected_payment:
    filtered_df = filtered_df[filtered_df["Payment"].isin(selected_payment)]

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------

st.header("Summary statistics (KPIs)")

total_sales = filtered_df["Total"].sum()
avarage_rating = filtered_df["Rating"].mean()
total_Transactions = filtered_df["Invoice ID"].nunique()
avarage_transactions = filtered_df["Total"].mean()
top_product_line = filtered_df["Product line"].value_counts().index[0]

#First row

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Sales", f"{total_sales:,.2f} €")

with col2:
    st.metric("Average Rating", f"{avarage_rating:.2f}")


#Second row

col3, col4 = st.columns(2)

with col3:
    st.metric("Total Transactions", f"{total_Transactions:,}")

with col4:
    st.metric("Average Transaction", f"{avarage_transactions:,.2f} €")

# Third row
st.write("### Top Product Line")
st.success(top_product_line)

st.divider()


# ---------------------------------------------------
# DATAFRAME SECTION
# ---------------------------------------------------
st.header("Raw Data")

show_data = st.checkbox("Show dataset")

if show_data:
    st.dataframe(filtered_df)

st.divider()


# ---------------------------------------------------
# SALES OVER TIME
# ---------------------------------------------------

sales_over_time = filtered_df.groupby(filtered_df["Date"].dt.date)["Total"].sum()

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(sales_over_time.index, sales_over_time.values)
ax.set_title("Sales Over Time")
ax.set_xlabel("Date")
ax.set_ylabel("Total Sales")
plt.xticks (rotation = 45)    

st.pyplot(fig)

st.divider()


# ---------------------------------------------------
# TOP 5 TRANSACTIONS
# ---------------------------------------------------
st.header("Top 5 Transactions")

top5 = filtered_df.sort_values("Total", ascending=False).head(5)

st.table(top5[["Invoice ID", "City", "Product line", "Total", "Rating"]])

st.divider()

# ---------------------------------------------------
# FINAL MESSAGE
# ---------------------------------------------------

st.markdown( """<h2 style='color:#4CAF50;'>
       Dashboard loaded successfully!
    </h2> """, unsafe_allow_html=True)





