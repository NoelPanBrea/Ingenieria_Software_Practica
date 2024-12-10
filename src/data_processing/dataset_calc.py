from pandas import DataFrame


class PreprocessApplier():
    """
    Applies preprocessing methods to a DataFrame.

    This class allows the application of various preprocessing methods 
    to a dataset, specifically for handling null values in specified columns.

    Attributes 
    ----------
    _methods : dict[str, function]
        Dictionary associating method names with their functions.
    cte : list[float]
        List of constants to be used in certain methods.
    dataframe : pd.DataFrame
        The DataFrame on which preprocessing will be applied.
    columns : list[str]
        List of DataFrame columns to be processed.
    _current_method : function
        The current preprocessing method to be applied.
    """

    def __init__(self) -> None:
        """
        Initializes the PreprocessApplier object.

        Sets up the dictionary of preprocessing methods and 
        initializes state variables.
        """
        self._methods = {"delete": self.delete, "mean": self.mean,
                         "median": self.median, "constant": self.constant}
        self.cte = []
        self.dataframe = None
        self.columns = None
        self._current_method = None

    @property
    def methods(self) -> dict["function"]:
        """
        Gets the available preprocessing methods.

        Returns
        ----------
        dict
            Dictionary associating method names with their functions.
        """
        return self._methods

    def set_current_method(self, value: str, cte: list[float] = None):
        """
        Sets the current preprocessing method.

        Parameters
        ----------
        value : str
            Name of the preprocessing method to use.
        cte : list[float], optional
            List of constants for the "constant" method.
        """
        self._current_method = self._methods[value]
        self.cte = cte

    def delete(self) -> None:
        """
        Deletes rows with null values in the specified columns.

        Modifies the current DataFrame by removing rows that contain
        null values in the defined columns.
        """
        self.dataframe = self.dataframe.dropna(
            inplace=True, subset=self.columns)

    def mean(self) -> None:
        """
        Replaces null values with the mean of each column.

        Replaces null values in the specified columns with 
        the mean of each column.
        """
        for x in self.columns:
            self.dataframe[x] = self.dataframe[x].fillna(
                self.dataframe[x].mean(skipna=True))

    def median(self) -> None:
        """
        Replaces null values with the median of each column.

        Replaces null values in the specified columns with 
        the median of each column.
        """
        for x in self.columns:
            self.dataframe[x] = self.dataframe[x].fillna(
                self.dataframe[x].median(skipna=True))

    def constant(self) -> None:
        """
        Replaces null values with specified constants.

        Replaces null values in the specified columns with 
        constant values defined in the cte list.
        """
        for i, x in enumerate(self.columns):
            if self.cte[i]:
                self.dataframe[x] = self.dataframe[x].fillna(float(self.cte[i]))
            else:
                raise ValueError()

    def apply_preprocess(self, dataframe: DataFrame, columns: list[str]) -> None:
        """
        Modifies None values based on the current configuration.

        Parameters
        ----------
        dataframe : pd.DataFrame
            The DataFrame on which preprocessing will be applied.
        columns : list[str]
            List of columns to which preprocessing will be applied.

        Raises
        ------
        ValueError
            If no preprocessing configuration or columns are selected.
        """
        self.dataframe = dataframe
        self.columns = columns
        try:
            if self.columns is not None and self._current_method is not None:
                self._current_method()
            else:
                res = "Se debe elegir una configuración de preprocesado "
                res += "para aplicar"
                raise IndexError(res)
        except IndexError as e:
            raise Exception(f"{e}")
        except ValueError as e:
            res = "En el campo constantes se deben introducir números "
            raise ValueError(res + f"con '.' como separador de decimales")
        except Exception as e:
            raise Exception(f"Ha ocurrido un error inesperado: {e}")


def none_count(dataframe: DataFrame, columns: list[str]) -> list[int]:
    """
    Counts None values in the specified columns.

    Parameters
    ----------
    dataframe : pd.DataFrame
        DataFrame in which None values will be counted.
    columns : list[str]
        List of columns to count None values.

    Returns
    ----------
    list[int]
        List with the number of None values in the selected columns.
    """
    return [dataframe[x].isna().sum() for x in columns]
