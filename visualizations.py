# visualizations.py
import altair as alt
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
def create_category_cost_bar_chart(df, selected_month, selected_year):

    if df.empty:
        return None


    category_cost = df.groupby('category')['cost'].sum().reset_index()

    color_scale = alt.Scale(domain=category_cost['category'].unique(),
                            range=["#ff9a00", "#000000", "#09ff00", "#9d0000", "#98FF98","#644b77"])


    bar_chart = alt.Chart(category_cost).mark_bar().encode(
        x='category:O',
        y='cost:Q',
        color=alt.Color('category:N', scale=color_scale),
        tooltip=['category:N', 'cost:Q']
    ).properties(
        # title=f'Total Cost per Category for {selected_month} {selected_year}' if selected_month != "All" else f'Total Cost per Category for {selected_year}',
        width=600,
        height=400
    )

    return bar_chart


def plot_arima_forecast(data):
    data['datetime'] = pd.to_datetime(data['datetime'])
    data.set_index('datetime', inplace=True)
    monthly_cost = data['cost'].resample('M').sum()
    train_size = int(len(monthly_cost) * 0.8)
    train, test = monthly_cost[0:train_size], monthly_cost[train_size:]
    model_train = ARIMA(train, order=(1, 0, 1))
    model_train_fit = model_train.fit()
    test_forecast = model_train_fit.get_forecast(steps=len(test))
    test_forecast_series = pd.Series(test_forecast.predicted_mean, index=test.index)
    test = test.ffill()
    test_forecast_series.ffill(inplace=True)
    if test_forecast_series.isna().any() or test.isna().any():
        raise ValueError("NaN values found in forecast or test data. Please check the data.")
    mse = mean_squared_error(test, test_forecast_series)
    rmse = mse ** 0.5

    plt.style.use('dark_background')
    plt.figure(figsize=(600 / 100, 400 / 100))
    plt.figure(figsize=(14, 7))
    plt.plot(train, label='Training Data', color='orange')
    # plt.plot(test, label='Actual Data', color='orange')
    plt.plot(test_forecast_series, label='Forecasted Data', color='purple')

    plt.fill_between(test_forecast_series.index,
                     test_forecast.conf_int().iloc[:, 0],
                     test_forecast.conf_int().iloc[:, 1],
                     color='k', alpha=.15)

    plt.title('ARIMA Model Evaluation', color='green', fontsize=16)
    plt.xlabel('Date', color='green', fontsize=16)
    plt.ylabel('Cost', color='green', fontsize=16)
    plt.legend(facecolor='black', edgecolor='white', fontsize=16)
    plt.savefig('arima_forecast_plot.png', facecolor='black')
    plt.close()

    return rmse

