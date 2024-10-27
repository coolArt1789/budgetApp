import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error

# Load the dataset
data = pd.read_csv('transactions.csv')
data['datetime'] = pd.to_datetime(data['datetime'])

# Set the datetime as index for easy resampling
data.set_index('datetime', inplace=True)

# Resample to get total cost per month
monthly_cost = data['cost'].resample('M').sum()

# Filter the result to include only months up to October (month <= 10)
monthly_cost_till_october = monthly_cost[monthly_cost.index.month < 10]

# Display the filtered result
print(monthly_cost_till_october)

# Split the data into train and test
train_size = int(len(monthly_cost) * 0.8)  # Use the monthly cost data
train, test = monthly_cost[0:train_size], monthly_cost[train_size:]

# Fit the ARIMA model on the training dataset
model_train = ARIMA(train, order=(1, 0, 1))
model_train_fit = model_train.fit()

# Forecast on the test dataset
test_forecast = model_train_fit.get_forecast(steps=len(test))
test_forecast_series = pd.Series(test_forecast.predicted_mean, index=test.index)

# Forward fill NaN values in the test set and forecast series
test = test.ffill()  # Forward fill for the test set

# Check for NaN values in forecast series
print("NaN values in forecast series before fill:")
print(test_forecast_series.isna().sum())

# Forward fill for forecast series
test_forecast_series.ffill(inplace=True)

# Check again for NaN values after fill
print("NaN values in forecast series after fill:")
print(test_forecast_series.isna().sum())

# Ensure there are no NaN values before calculating RMSE
if test_forecast_series.isna().any() or test.isna().any():
    raise ValueError("NaN values found in forecast or test data. Please check the data.")

# Calculate the mean squared error
mse = mean_squared_error(test, test_forecast_series)
rmse = mse**0.5

# Create a plot to compare the forecast with the actual test data
plt.figure(figsize=(14, 7))
plt.plot(train, label='Training Data')
# plt.plot(test, label='Actual Data', color='orange')
# plt.plot(test_forecast_series, label='Forecasted Data', color='green')

# Add confidence intervals for the forecast
plt.plot(test_forecast_series.index, test_forecast_series, label='Forecasted Data', color='green')

# Optionally add confidence intervals for the forecast
plt.fill_between(test_forecast_series.index,
                 test_forecast.conf_int().iloc[:, 0],
                 test_forecast.conf_int().iloc[:, 1],
                 color='k', alpha=.15)

plt.title('ARIMA Model Evaluation')
plt.xlabel('Date')
plt.ylabel('Cost')
plt.legend()
plt.grid()
plt.show()
print('RMSE:', rmse)
