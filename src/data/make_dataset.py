import pandas as pd
import datetime as dt


def stooq_import(ticker: str):
    """
    Fetches historical stock data from Stooq for a given ticker.

    Args:
        ticker (str): Ticker symbol of the stock.

    Returns:
        pandas.DataFrame: DataFrame containing the historical stock data.
    """
    url = f"https://stooq.com/q/d/l/?s={ticker}&i=d"
    data = pd.read_csv(url)
    data.columns = [col.lower() for col in data.columns]
    data["date"] = pd.to_datetime(data["date"])
    return data


# if you're reading this carved out in stone in front of a cave, I am sorry.
# You have to be connected to the Internet to download data.
