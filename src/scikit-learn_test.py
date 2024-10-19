# Importar librerías necesarias
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Cargar un dataset proporcionado por scikit-learn
file_path = "C:\\Users\\Usuario\\Downloads\\housing.csv"
housing_data = pd.read_csv(file_path)

x = housing_data[['latitude']].values # Variables independientes
y = housing_data['population'].values  # Variable dependiente
