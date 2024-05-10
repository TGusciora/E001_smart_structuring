import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import metrics as sk_metrics


def prophet_plot_forecast(
    data: pd.DataFrame, title: str, obs: int = 5, y_start_0: int = 1, ax=None
):
    """
    Plots the actual and predicted stock prices using Prophet (Hi Mark) forecasting model.

    Parameters:
    - data (pandas.DataFrame): The dataframe containing the stock price data.
    - title (str): The title of the plot.
    - obs (int): The number of observations to consider for plotting.
    - y_start_0 (int): If set to 1, Y axis starts with 0. If set to 0, use default axis values.
    - ax (matplotlib.axes.Axes, optional): The axes on which to plot. If None, uses current axes.

    Returns:
    None
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(
        data["ds"][-5 * obs :],
        data["y"][-5 * obs :],
        label="Actual Stock Price",
        color="blue",
    )
    ax.plot(
        data["ds"][-5 * obs :],
        data["yhat"][-5 * obs :],
        label="Predicted Stock Price",
        color="orange",
    )

    ax.fill_between(
        data["ds"][-obs:],
        data["yhat_lower"][-obs:],
        data["yhat_upper"][-obs:],
        color="gray",
        alpha=0.3,
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Stock Price")
    ax.set_title(title)
    ax.legend(loc="lower left")

    if y_start_0 == 1:
        ax.set_ylim(bottom=0)

    if ax is None:  # Show the plot only if this function created the figure
        plt.show()


def prophet_plot_forecast_dual(data: pd.DataFrame, title: str, obs: int = 5):
    """
    Creates a figure with two subplots: the first in default scale, and the second with Y axis starting from 0.

    Parameters:
    - data (pandas.DataFrame): The dataframe containing the stock price data.
    - title (str): The title of the plot.
    - obs (int): The number of observations to consider for plotting.
    """
    fig, axs = plt.subplots(1, 2, figsize=(24, 6))

    # First subplot in default scale
    prophet_plot_forecast(
        data, title + " (default scale)", obs, y_start_0=0, ax=axs[0]
    )

    # Second subplot with Y axis starting from 0
    prophet_plot_forecast(
        data, title + " (true scale)", obs, y_start_0=1, ax=axs[1]
    )

    plt.tight_layout()
    plt.show()


def plot_forecast_error(
    data: object, title: str, savefig: bool = True, path: str = None
):
    """
    Plots the forecast error metrics (MAE, MSE, RMSE) for a given dataset.

    Parameters:
    data (object): The dataset containing the actual and predicted values.
    title (str): The title of the plot.
    savefig (bool, optional): Whether to save the plot as an image. Defaults to True.

    Returns:
    None
    """
    actual = data[data["yhat"].notnull()]["y"]
    predicted = data[data["yhat"].notnull()]["yhat"]

    # Calculate MAE, MSE, and RMSE
    mae = sk_metrics.mean_absolute_error(actual, predicted)
    mse = sk_metrics.mean_squared_error(actual, predicted)
    rmse = np.sqrt(mse)  # RMSE is the square root of MSE

    # Metrics and their names
    metrics = [mae, mse, rmse]
    metric_names = ["MAE", "MSE", "RMSE"]

    # Plotting
    plt.figure(figsize=(8, 6))
    bars = plt.bar(metric_names, metrics, color=["red", "green", "blue"])

    # Adding the value on top of each bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            yval,
            round(yval, 2),
            ha="center",
            va="bottom",
        )

    # Adding labels and title
    plt.xlabel("Metric")
    plt.ylabel("Value")
    plt.title(title + " prediction error metrics (MAE, MSE, RMSE)")

    # Saving the plot
    if savefig:
        plt.savefig(path + title + "_error_metrics.png")
    # Show the plot
    plt.show()
