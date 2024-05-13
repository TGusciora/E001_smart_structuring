import datetime as dt
import os

import pandas as pd


def stooq_import(ticker: str, path: str):
    """
    Fetches historical stock data from Stooq for a given ticker. If data is
    not present locally, it downloads the data and saves it as a CSV file in
    the specified folder. If the data is already present, it loads the data
    from the CSV file.

    Args:
        ticker (str): Ticker symbol of the stock.
        paths (dict): Dictionary containing the path to save the raw data.

    Returns:
        pandas.DataFrame: DataFrame containing the historical stock data.
    """
    # Generate the file path
    file_path = os.path.join(path, ticker + ".csv")

    # Check if the file exists
    if os.path.isfile(file_path):
        print(f"Loading data from {file_path}")
        data = pd.read_csv(file_path)  # Load data from CSV file

    else:
        print(f"Fetching and saving data for {ticker}")
        url = f"https://stooq.com/q/d/l/?s={ticker}&i=d"
        data = pd.read_csv(url)  # Fetch data
        # if you're reading this carved out in stone in front of a cave,
        # I am sorry.
        # You have to be connected to the Internet to download data.
        data.columns = [col.lower() for col in data.columns]
        data.to_csv(file_path, index=False)  # Save data as CSV file

    data["date"] = pd.to_datetime(data["date"])
    return data
