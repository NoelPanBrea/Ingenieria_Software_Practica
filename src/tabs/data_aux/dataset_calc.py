from pandas import DataFrame


class PreprocessApplier():
    """
    Aplica métodos de preprocesamiento a un DataFrame.

    Esta clase permite aplicar diferentes métodos de preprocesamiento
    a un conjunto de datos, específicamente para manejar valores nulos
    en las columnas especificadas.

    Attributes 
    ----------
    _methods : dict[str, function]
        Diccionario que asocia los nombres de los métodos con sus funciones.
    cte : list[float]
        Lista de constantes que se usarán en algunos métodos.
    dataframe : pd.DataFrame
        El DataFrame en el que se aplicará el preprocesamiento.
    columns : list[str]
        Lista de columnas del DataFrame que se procesarán.
    _current_method : function
        Método de preprocesamiento actual que se aplicará.
    """

    def __init__(self) -> None:
        """
        Inicializa el objeto PreprocessApplier.

        Configura el diccionario de métodos de preprocesamiento y
        inicializa las variables de estado.
        """
        self._methods = {'delete': self.delete, 'mean': self.mean,
                         'median': self.median, 'constant': self.constant}
        self.cte = []
        self.dataframe = None
        self.columns = None
        self._current_method = None

    @property
    def methods(self) -> dict['function']:
        """
        Obtiene los métodos de preprocesamiento disponibles.

        Returns
        ----------
        dict
            Diccionario que asocia los nombres de los métodos con sus funciones.
        """
        return self._methods

    def set_current_method(self, value: str, cte: list[float] = None):
        """
        Establece el método de preprocesamiento actual.

        Parameters
        ----------
        value : str
            Nombre del método de preprocesamiento a utilizar.
        cte : list[float], optional
            Lista de constantes para el método 'constant'.
        """
        self._current_method = self._methods[value]
        self.cte = cte

    def delete(self) -> None:
        """
        Elimina filas con valores nulos en las columnas especificadas.

        Modifica el DataFrame actual eliminando las filas que contienen
        valores nulos en las columnas definidas.
        """
        self.dataframe = self.dataframe.dropna(
            inplace=True, subset=self.columns)

    def mean(self) -> None:
        """
        Reemplaza valores nulos con la media de cada columna.

        Reemplaza los valores nulos en las columnas especificadas por
        la media de cada columna.
        """
        for x in self.columns:
            self.dataframe[x] = self.dataframe[x].fillna(
                self.dataframe[x].mean(skipna=True))

    def median(self) -> None:
        """
        Reemplaza valores nulos con la mediana de cada columna.

        Reemplaza los valores nulos en las columnas especificadas por
        la mediana de cada columna.
        """
        for x in self.columns:
            self.dataframe[x] = self.dataframe[x].fillna(
                self.dataframe[x].median(skipna=True))

    def constant(self) -> None:
        """
        Reemplaza valores nulos con constantes especificadas.

        Reemplaza los valores nulos en las columnas especificadas
        por valores constantes definidos en la lista cte.
        """
        for i, x in enumerate(self.columns):
            if self.cte[i]:
                self.dataframe[x] = self.dataframe[x].fillna(float(self.cte[i]))
            else:
                raise ValueError()

    def apply_preprocess(self, dataframe: DataFrame, columns: list[str]) -> None:
        """
        Modifica los valores de Nones según la configuración actual.

        Parameters
        ----------
        dataframe : pd.DataFrame
            El DataFrame sobre el cual aplicar el preprocesamiento.
        columns : list[str]
            Lista de columnas a las que se aplicará el preprocesamiento.

        Raises
        ------
        ValueError
            Si no se elige una configuración de preprocesamiento o columnas.
        """
        self.dataframe = dataframe
        self.columns = columns
        try:
            if self.columns is not None and self._current_method is not None:
                self._current_method()
            else:
                res = 'Se debe elegir una configuración de preprocesado '
                res += 'para aplicar'
                raise IndexError(res)
        except IndexError as e:
            raise Exception(f'{e} + ')
        except ValueError as e:
            res = 'En el campo constantes se deben introducir números '
            raise ValueError(res + f'con "." como separador de decimales')
        except Exception as e:
            raise Exception(f'Ha ocurrido un error inesperado: {e}')


def none_count(dataframe: DataFrame, columns: list[str]) -> list[int]:
    """
    Cuenta los valores None en las columnas especificadas.

    Parameters
    ----------
    dataframe : pd.DataFrame
        DataFrame en el que se contarán los valores None.
    columns : list[str]
        Lista de columnas para contar los valores None.

    Returns
    ----------
    list[int]
        Lista con el número de valores None en las columnas seleccionadas.
    """
    return [dataframe[x].isna().sum() for x in columns]
