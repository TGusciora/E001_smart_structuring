# import packages - \src\utils\start_wrapper.py
from src.utils.start_wrapper import *
wrapper_notebook_settings()

# Load dictionary of project paths
import src.utils.paths
paths = src.utils.paths.paths_dictionary()
print("Contents of paths dictionary:")
for key in paths:
    print(key, ": ", paths[key])


#  basic packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

# Load environment variables
import dotenv
import os
dotenv.load_dotenv(os.path.join(os.path.dirname(os.getcwd()), '.env'))

# project specific packages
import urllib.request
import seaborn as sns
import sklearn as sk
from sklearn import metrics
from prophet import Prophet
