from builtins import str
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from function import DataAnalyzer
from babel.numbers import format_currency
sns.set(style='dark')

# Function

# Dataset
datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
all_df = pd.read_csv("./data/all_data.csv")
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)
geolocation = pd.read_csv('./data/geolocation_dataset.csv')

for col in datetime_cols:
    all_df[col] = pd.to_datetime(all_df[col])


min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

# Sidebar
with st.sidebar:
    # Logo Image
    st.image("./image/Design.png")

    # Judul Perusahaan
    st.title("Irfan Saputra Nst")

    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & 
                (all_df["order_approved_at"] <= str(end_date))]

function = DataAnalyzer(main_df)
sum_spend_df = function.create_sum_spend_df()
sum_order_items_df = function.create_sum_order_items_df()
state, most_common_state = function.create_bystate_df()
review_score, common_score = function.review_score_df()

# Judul
st.header('E-Commerce Dashboard :sparkles:')

# Total Spend Customer
st.subheader("Total Spend Customer")
col1, col2 = st.columns(2)

with col1:
    total_spend = format_currency(sum_spend_df["total_spend"].sum(), "IDR", locale="id_ID")
    st.markdown(f"Total Spend: **{total_spend}**")

with col2:
    avg_spend = format_currency(sum_spend_df["total_spend"].mean(), "IDR", locale="id_ID")
    st.markdown(f"Average Spend: **{avg_spend}**")
        
fig, ax = plt.subplots(figsize=(20, 10))

colors = ["#068DA9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    y="order_approved_at", 
    x="total_spend",
    data=sum_spend_df.sort_values(by="total_spend", ascending=False),
    palette=colors,
    ax=ax
    )
ax.set_title("Total Pengeluaran Pelanggan Per Tahun", loc="center", fontsize=30)
ax.set_ylabel("Tahun", fontsize=20)
ax.set_xlabel("Total Pengeluaran Customer", fontsize=20)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

# Order Items
st.subheader("Order Items")
col1, col2 = st.columns(2)

with col1:
    total_items = sum_order_items_df["product_count"].sum()
    st.markdown(f"Total Items: **{total_items}**")

with col2:
    avg_items = sum_order_items_df["product_count"].mean()
    st.markdown(f"Average Items: **{avg_items}**")

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(35, 15))
colors = ["#068DA9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    x="product_count", 
    y="product_category_name_english", 
    data=sum_order_items_df.head(5),
    palette=colors,
    ax=ax 
)
ax.set_title("Produk Paling Laris", loc="center", fontsize=50)
ax.set_ylabel("Nama Product", fontsize=40)
ax.set_xlabel("Jumlah Order", fontsize=40)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=30)
st.pyplot(fig)


# Customer State
st.subheader("Customer State")
col1, col2 = st.columns(2)

with col1:
    states = state["customer_count"].sum()
    st.markdown(f"Total Customer: **{states}**")

with col2:
    most_common_state = state.customer_state.value_counts().index[0]
    st.markdown(f"Most Common Review Score: **{most_common_state}**")

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(35, 15))
    colors = ["#068DA9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    x="customer_count", 
    y="customer_state", 
    data=state.head(5),
    palette=colors,
    ax=ax 
)
ax.set_title("Pelanggan Terbanyak Berdasarkan Negara", loc="center", fontsize=50)
ax.set_ylabel("Asal Pelanggan", fontsize=40)
ax.set_xlabel("Jumlah Pelanggan", fontsize=40)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=30)
st.pyplot(fig)


# Review Score
st.subheader("Review Score")
col1,col2 = st.columns(2)

with col1:
    avg_review_score = review_score.mean()
    st.markdown(f"Average Review Score: **{avg_review_score}**")

with col2:
    most_common_review_score = review_score.value_counts().index[0]
    st.markdown(f"Most Common Review Score: **{most_common_review_score}**")

fig, ax = plt.subplots(figsize=(12, 6))
colors = ["#068DA9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x=review_score.index, 
            y=review_score.values, 
            order=review_score.index,
            palette=colors,
            )

plt.title("Tingkat Kepuasan Customer", fontsize=15)
plt.xlabel("Rating")
plt.ylabel("Jumlah Pelanggan")
plt.xticks(fontsize=12)
st.pyplot(fig)