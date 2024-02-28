import pandas as pd


class DataFrameInspector():
    """
    A utility class for inspecting and analyzing pandas DataFrames.
    """

    def __init__(self, df):
        self.df = df
        self._get_dataframe_info()
        self._get_dataframe_head()
        self._get_dataframe_tail()
        self._get_dataframe_shape()
        self._identify_primary_key()

    def _get_dataframe_info(self):
        """
        Prints information about the DataFrame, including column names, non-null counts, and data types.
        """
        print("DataFrame Info:")
        print(self.df.info(),'\n')
        return None

    def _get_dataframe_head(self, n=5):
        """
        Prints the first n rows of the DataFrame.
        """
        print(f"First {n} Rows of the DataFrame:")
        print(self.df.head(n),'\n')
        return None

    def _get_dataframe_tail(self, n=5):
        """
        Prints the last n rows of the DataFrame.
        """
        print(f"Last {n} Rows of the DataFrame:")
        print(self.df.tail(n),'\n')
        return None

    def _get_dataframe_shape(self):
        """
        Prints the number of rows and columns in the DataFrame.
        """
        rows, cols = self.df.shape
        print(f"The DataFrame has {rows} rows and {cols} columns.\n")
        return None

    def _identify_primary_key(self):
        """
        Identifies the primary key column(s) in the DataFrame, if any.
        """
        for col in self.df.columns:
            if self.df[col].is_unique:
                print(f"The primary key for the DataFrame is: {col}\n")
                return col
        print("No primary key found.\n")
        return None
