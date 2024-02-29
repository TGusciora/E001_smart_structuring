import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sklearn as sk
from sklearn import metrics

def prophet_plot_forecast(data: object, title: str, obs: int = 5):
    """
    Plots the actual and predicted stock prices using Prophet forecasting model.

    Parameters:
    - data (pandas.DataFrame): The dataframe containing the stock price data.
    - title (str): The title of the plot.
    - obs (int): The number of observations to consider for plotting.

    Returns:
    None
    """
    plt.figure(figsize=(12, 6))
    plt.plot(data['ds'][-5*obs:], data['y'][-5*obs:], label='Actual Stock Price', color='blue')
    plt.plot(data['ds'][-5*obs:], data['yhat'][-5*obs:], label='Predicted Stock Price', color='orange')

    # Shading the area for prediction intervals
    # Assuming the last obs observations have the forecast data
    plt.fill_between(data['ds'][-obs:], data['yhat_lower'][-obs:], data['yhat_upper'][-obs:], color='gray', alpha=0.3)

    # Adding labels, title and legend
    plt.xlabel('Date')
    plt.ylabel('Stock Price')
    plt.title(title + ' stock Price Prediction')
    plt.legend()

    # Show the plot
    plt.show()

def plot_forecast_error(data: object, title: str, savefig: bool = True, path: str = None):
    """
    Plots the forecast error metrics (MAE, MSE, RMSE) for a given dataset.

    Parameters:
    data (object): The dataset containing the actual and predicted values.
    title (str): The title of the plot.
    savefig (bool, optional): Whether to save the plot as an image. Defaults to True.

    Returns:
    None
    """
    actual = data[data['yhat'].notnull()]['y']
    predicted = data[data['yhat'].notnull()]['yhat']

    # Calculate MAE, MSE, and RMSE
    mae = sk.metrics.mean_absolute_error(actual, predicted)
    mse = sk.metrics.mean_squared_error(actual, predicted)
    rmse = np.sqrt(mse) # RMSE is the square root of MSE

    # Metrics and their names
    metrics = [mae, mse, rmse]
    metric_names = ['MAE', 'MSE', 'RMSE']

    # Plotting
    plt.figure(figsize=(8, 6))
    bars = plt.bar(metric_names, metrics, color=['red', 'green', 'blue'])

    # Adding the value on top of each bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

    # Adding labels and title
    plt.xlabel('Metric')
    plt.ylabel('Value')
    plt.title(title + ' prediction error metrics (MAE, MSE, RMSE)')

    # Saving the plot
    if savefig:
        plt.savefig(path+title+'_error_metrics.png')
    # Show the plot
    plt.show()

