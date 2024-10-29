from pandas import DataFrame


class PreprocessApplier():
    def __init__(self) -> None:
        self._methods = {'delete': self.delete, 'mean': self.mean,
                        'median': self.median, 'constant': self.constant}
        self.cte = []
        self.dataframe = None
        self.columns = None
        self._current_method = None

    @property
    def methods(self) -> dict['function']:
        return self._methods

    def set_current_method(self, value: str, cte: list[float] = None):
        self._current_method = self._methods[value]
        self.cte = cte

    def delete(self) -> None:
        self.dataframe = self.dataframe.dropna(
            inplace=True, subset=self.columns)

    def mean(self) -> None:
        for x in self.columns:
            self.dataframe[x] = self.dataframe[x].fillna(
                self.dataframe[x].mean(skipna=True))

    def median(self) -> None:
        for x in self.columns:
            self.dataframe[x] = self.dataframe[x].fillna(
                self.dataframe[x].median(skipna=True))

    def constant(self) -> None:
        for i, x in enumerate(self.columns):
            self.dataframe[x] = self.dataframe[x].fillna(float(self.cte[i]))

    def apply_preprocess(self, dataframe: DataFrame, columns: list[str]) -> None:
        """
        Modifies the value of Nones according to the current configuration

        Returns
        -----------
            None
        """
        self.dataframe = dataframe
        self.columns = columns
        try:
            if self.columns is not None and self._current_method is not None:
                self._current_method()
            else:
                res = 'Se debe elegir una configuración de preprocesado '
                res += 'y columnas para aplicarla'
                raise ValueError(res)
        except Exception as e:
            raise Exception(f'{e}')

def none_count(dataframe: DataFrame, columns: list[str]) -> list[int]:
    """
    Counts the None values of the self.columns in self.columns

    Returns
    -----------
    [self.self.dataframe[x].isna().sum() for\
            x in self.self.columns]: list[int]
            List with the number of None values of the selected self.columns
    """
    return [dataframe[x].isna().sum() for
            x in columns]
