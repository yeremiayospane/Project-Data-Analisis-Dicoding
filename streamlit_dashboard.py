import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from matplotlib import dates


def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='dteday').agg({
        "cnt": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    return daily_orders_df

def total_registered_df(df):
   df_reg =  df.groupby(by="dteday").agg({
      "registered": "sum"
    })
   df_reg = df_reg.reset_index()
   df_reg.rename(columns={
        "registered": "total_register"
    }, inplace=True)
   return df_reg

def total_casual_df(df):
   df_casual =  df.groupby(by="dteday").agg({
      "casual": ["sum"]
    })
   df_casual = df_casual.reset_index()
   df_casual.rename(columns={
        "casual": "casual_sum"
    }, inplace=True)
   return df_casual

def total_sale_on_weeks(df):
    result_day_name = df.groupby(['dteday', 'day_name'])['cnt'].sum().reset_index()
    category_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    result_day_name['day_name'] = pd.Categorical(result_day_name['day_name'], categories=category_order, ordered=True)
    sorted_result_day_name = result_day_name.sort_values(by='day_name').reset_index()
    return sorted_result_day_name


def total_sale_time_category(df):
    result_time_category = df.groupby(['dteday', 'time_category'])['cnt'].sum().reset_index()
    return result_time_category


def our_user(df):
    usr = df[['casual', 'registered']].sum()
    usr_df = pd.DataFrame(usr).reset_index()
    usr_df.columns = ['User Type', 'Total']
    return usr_df


# Load datasets
df_day = pd.read_csv('./Datasets/fix_day.csv')
df_hour = pd.read_csv('./Datasets/fix_hour.csv')

df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])
# Filter Component
min_date_day = df_day['dteday'].min()
max_date_day = df_day['dteday'].max()

min_date_hour = df_hour['dteday'].min()
max_date_hour = df_hour['dteday'].max()

with st.sidebar:
    st.image("./logo.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date_day,
        max_value=max_date_day,
        value=[min_date_day, max_date_day]
    )

datasets_day = df_day[
    (df_day["dteday"] >= str(start_date)) &
    (df_day["dteday"] <= str(end_date))
]
datasets_hour = df_hour[
    (df_hour["dteday"] >= str(start_date)) &
    (df_hour["dteday"] <= str(end_date))
]

# Inisialisasi data
total_order = create_daily_orders_df(datasets_day)
total_registered = total_registered_df(datasets_day)
total_casual = total_casual_df(datasets_day)
total_sale_weeks = total_sale_on_weeks(datasets_day)
time_category = total_sale_time_category(datasets_hour)
users = our_user(datasets_day)

st.header('Project Submission Dicoding')
st.subheader('Daily Orders')

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total orders", value=total_order['cnt'].sum())

with col2:
    total_regist = total_registered.total_register.sum()
    st.metric("Total Registered", value=total_regist)

with col3:
    total_cas = total_casual.casual_sum.sum()
    st.metric("Total Casual", value=int(total_cas))

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    datasets_day["dteday"],
    datasets_day["cnt"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.subheader('Rental Berdasarkan Hari')

fig = plt.figure(figsize=(10, 5))
counts = total_sale_weeks['cnt'].to_list()
day_names = total_sale_weeks['day_name']
max_index = counts.index(max(counts))

    # Define colors for bars
colors = ['#FF7676'] * len(day_names)
colors[max_index] = '#0802A3'  # Set a different color for the maximum count bar

plt.figure(figsize=(20, 8))
bars = plt.bar(day_names, counts, color=colors)
plt.xlabel("Day Name", fontsize=14)
plt.ylabel("Count", fontsize=14)

    # Display the total count
total_count = sum(counts)
plt.text(0.5, -0.1, f"Total: {total_count}", fontsize=14, ha='center', va='center', transform=fig.transFigure)
st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot()

st.subheader('Rental Berdasarkan Kategori Waktu')
fig = plt.figure(figsize=(20, 8))
plt.bar(time_category['time_category'], time_category['cnt'], color='#64CCC5')
plt.xlabel("Time Category", fontsize=14)
plt.ylabel("Count")
st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot()






