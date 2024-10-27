import pandas as pd

def create_dataframe(file_path):
    file = open("transactions.csv", 'r')
    df = pd.read_csv(file_path, parse_dates=['datetime'])

    # Extract year and month from the 'datetime' column
    df['year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month_name()

    return df


def filter_dataframe(df, selected_year, selected_month, selected_category):

    df_selected_year = df[df['year'] == selected_year]

    if selected_month != "All":
        df_selected_year = df_selected_year[df_selected_year['month'] == selected_month]

    if selected_category != "All":
        df_selected_year = df_selected_year[df_selected_year['category'] == selected_category]

    df_selected_sorted = df_selected_year.sort_values(by="cost", ascending=False)

    return df_selected_sorted
