import json
import requests
import streamlit as st
from data_processing import create_dataframe, filter_dataframe
from visualizations import create_category_cost_bar_chart, plot_arima_forecast
from PIL import Image
import altair as alt
import pandas as pd
from streamlit_lottie import st_lottie
import plotly.express as px

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
lottie_witch = load_lottiefile('Witch.json')
lottie_bpk = load_lottiefile('bpk.json')
lottie_ww = load_lottiefile('ww.json')
lottie_g = load_lottiefile('g.json')
lottie_c = load_lottiefile('c.json')

df = create_dataframe("transactions.csv")
df['datetime'] = pd.to_datetime(df['datetime']).dt.date
st.set_page_config(
    page_title="Budget Management Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)
with st.sidebar:
    st_lottie(lottie_c, height= 175, width=200, key="castle_sidebar")
with st.sidebar:
    st.title('Budget Management Dashboard')

    # Sidebar filters
    year_list = df['year'].unique()[::-1]
    selected_year = st.selectbox('Select a year', year_list, index=0)

    month_list = ["All"] + list(df[df['year'] == selected_year]['month'].unique())
    selected_month = st.selectbox('Select a month', month_list)

    category_list = ["All"] + list(df['category'].unique())
    selected_category = st.selectbox('Select a category', category_list)

    df_selected = df[(df['year'] == selected_year)]
    if selected_month != "All":
        df_selected = df_selected[df_selected['month'] == selected_month]
    if selected_category != "All":
        df_selected = df_selected[df_selected['category'] == selected_category]
    #
    # st.sidebar.subheader("Login")
    # username = st.sidebar.text_input("Username")
    # password = st.sidebar.text_input("Password", type='password')
    # button_was_clicked = st.sidebar.button("SUBMIT")

alt.themes.enable("dark")
with st.sidebar:
    st_lottie(lottie_witch, height= 175, width=200, key="witch_sidebar")


bar_chart = create_category_cost_bar_chart(df_selected, selected_month, selected_year)
if bar_chart:
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.altair_chart(bar_chart, use_container_width=True)

    with row1_col2:
        rmse = plot_arima_forecast(df)
        image = Image.open('arima_forecast_plot.png')
        st.image(image)

    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        top_5_df = df_selected.sort_values(by='cost', ascending=False).head(9)
        top_5_df['cost'] = top_5_df['cost'].apply(lambda x: f"${x:,.2f}")
        st.write(top_5_df[['datetime', 'category', 'cost']].reset_index(drop=True))

    with row2_col2:
        category_cost_df = df_selected.groupby("category")["cost"].sum().reset_index()
        fig = px.pie(
            category_cost_df,
            values="cost",
            names="category",
            # title="Spending by Category",
            hole=0.4,
        )
        fig.update_traces(textinfo='percent')
        fig.update_layout(width=600, height=400)
        st.plotly_chart(fig)

else:
    st.write("No data available for the selected options.")


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("C:\\Users\\gaura\\PycharmProjects\\Tax Agents Chatbot\\style\\style.css")

# Loading Animation
animation_symbol = "🎃"

st.markdown(
    f"""
    <div class = "snowflake">{animation_symbol}</div>
    <div class = "snowflake">{animation_symbol}</div>
    <div class = "snowflake">{animation_symbol}</div>
    <div class = "snowflake">{animation_symbol}</div>
    <div class = "snowflake">{animation_symbol}</div>
    <div class = "snowflake">{animation_symbol}</div>
    <div class = "snowflake">{animation_symbol}</div>
    <div class = "snowflake">{animation_symbol}</div>
    <div class = "snowflake">{animation_symbol}</div>
    <div class = "snowflake">{animation_symbol}</div>
    <div class = "snowflake">{animation_symbol}</div>
    <div class = "snowflake">{animation_symbol}</div>
    <div class = "snowflake">{animation_symbol}</div>
    <div class = "snowflake">{animation_symbol}</div>
    <div class = "snowflake">{animation_symbol}</div>
    <div class = "snowflake">{animation_symbol}</div>
    <div class = "snowflake">{animation_symbol}</div>
    <div class = "snowflake">{animation_symbol}</div>
    <div class = "snowflake">{animation_symbol}</div>
    """,
    unsafe_allow_html= True
)
