import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

class LinearModel:
    def __init__(self, data, input_columns, output_column):
        """
        A class for creating and managing a linear regression model.

        This class includes methods for fitting the model, making predictions,
        evaluating the model's performance, and generating a regression formula.

        Attributes
        ----------
        data : pd.DataFrame
            The dataset containing input and output columns.
        input_columns : list of str
            List of column names for input features.
        output_column : str
            Column name for the output feature.
        x : array-like
            Input features as a NumPy array.
        y : array-like
            Output feature as a NumPy array.
        model : LinearRegression
            The linear regression model from sklearn.
        coef_ : array-like
            Coefficients of the regression model.
        intercept_ : float
            Intercept of the regression model.
        y_pred : array-like
            Predicted values based on the regression model.
        mse_ : float
            Mean Squared Error of the model's predictions.
        r2_ : float
            R-squared score of the model's predictions.
        formula : str
            Formula representation of the regression model.
        """

        self.data = data
        self.input_columns = input_columns
        self.output_column = output_column
        # Extract input (x) and output (y) data from the dataset
        self.x = None if data is None else self.data[input_columns].values
        self.y = None if data is None else self.data[output_column].values
        # Initialize the linear regression model
        self.model = LinearRegression()
        # Initialize placeholders for model parameters and metrics
        self.coef_ = None
        self.intercept_ = None
        self.y_pred = None
        self.mse_ = None
        self.r2_ = None
        self.formula = None

    def set_model_params(self, coefficients, intercept, formula):
        """
        Sets the parameters of a preloaded model.

        Parameters
        ----------
        coefficients : array-like
            Coefficients of the regression model.
        intercept : float
            Intercept of the regression model.
        formula : str
            Formula representation of the regression model.

        Returns
        -------
        self : LinealModel
            The updated LinealModel instance.
        """
        self.coef_ = coefficients
        self.intercept_ = intercept
        self.formula = formula
        return self

    def fit(self):
        """
        Fits the linear regression model to the input data.

        The method also calculates predictions, evaluates the model's 
        performance, and generates the regression formula.
        """
        # Fit the model using sklearn's LinearRegression
        self.model.fit(self.x, self.y)

        # Store the coefficients and intercept
        self.coef_ = self.model.coef_
        self.intercept_ = self.model.intercept_

        # Ensure predictions are generated using the training data
        self.y_pred = self.predict(self.x)  # Use the predict method
        self.evaluate()
        self.calc_formula()
    
    def predict(self, data_to_predict: np.ndarray = None) -> np.ndarray:
        """
        Makes predictions using the fitted model.

        If `data_to_predict` is not provided, it defaults to the training data.

        Parameters
        ----------
        data_to_predict : np.ndarray, optional
            Data for which predictions are required.

        Returns
        -------
        np.ndarray
            Predicted values.
        """
        if data_to_predict is None:
            data_to_predict = self.x  # Usa los datos de entrenamiento si no se especifican otros

        # Return predictions for the input data
        return self.model.predict(data_to_predict)

    def evaluate(self):      
        """
        Evaluates the performance of the model.

        Calculates the Mean Squared Error (MSE) and R-squared (R²) score
        based on the model's predictions and actual values.

        Raises
        ------
        ValueError
            If predictions have not been generated before calling this method.
        """
        if self.y_pred is None:
            raise ValueError("Predicciones no generadas. Asegúrate de llamar a 'fit' antes de evaluar.")
        
        # Calculate MSE and R² score
        self.mse_ = mean_squared_error(self.y, self.y_pred)
        self.r2_ = r2_score(self.y, self.y_pred)

    def calc_formula(self):
        """
        Generates the formula for the linear regression model.

        The formula represents the regression equation with the calculated
        coefficients and intercept.
        """
        # Start the formula with the intercept
        self.formula = f"{self.output_column} = {self.intercept_:.2f}"
        
        # Add terms for each input column and its corresponding coefficient
        for i, col in enumerate(self.input_columns):
            self.formula += f" + ({self.coef_[i]:.2f} * {col})"