# import packages - \src\utils\start_wrapper.py
from src.utils.start_wrapper import *

# enable autoreload - that way you don't have to reload modules, when you change them
wrapper_notebook_settings()

# Load dictionary of project paths
# crawler from parent directory
import src.utils.paths
paths = src.utils.paths.paths_dictionary()
print("Contents of paths dictionary:")
for key in paths:
    print(key, ": ", paths[key])


# Project specific modules (reusable!)
import src.data.make_dataset
import src.utils.df_inspect
import src.visualization.visualize

# Load environment variables - safe way to load sensitive data
import dotenv
import os
dotenv.load_dotenv(os.path.join(os.path.dirname(os.getcwd()), '.env'))

# Why I dont have packages in utils.start_wrapper? Because pylint wouldn't recognize them
#  basic packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

# project specific packages
import urllib.request
import sklearn as sk
from sklearn import metrics

# FB (Hi Mark) module for forecasting
from prophet import Prophet
from prophet.serialize import model_to_json, model_from_json
