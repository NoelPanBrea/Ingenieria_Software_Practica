import numpy as np 
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

#1.Cargar datos
#Tensorflow no puede cargar datos desde una ruta
#así que usamos dee forma auxiliar pandas
ruta_archivo= r'ruta/al/archivo.csv'

datos = pd.read_csv(ruta_archivo)

X = datos['longitud'].values
Y = datos['latitud'].values

#2.MODELO LINEAL TENSORFLOW
#Utilizamos Sequential para definin la 'estructura' del modelo

modelo = Sequential([Dense(units=1, input_shape=(1,))])

#Compilamos el modelo
modelo.compile(optimizer='sgd', loss ='mean_squared_error')

#Entrenamos el modelo
modelo.fit(X,Y,epochs=100)

#Predicciones
predicciones = modelo.predict(X)
print(predicciones)

#Calcular el MSE
mse = tf.keras.losses.mean_squared_error(Y, predicciones).numpy().mean()
print(f"Error Cuadrático Medio (MSE): {mse}")
