import sys
sys.path.insert(0, 'src')
from tabs.data_aux.dataset_calc import *
if __name__ == '__main__':
    data = DataFrame({'a': [1, 2, None], 'b': [4, None, 6,]})
    selected_input_columns = ['a', 'b']
    a = PreprocessApplier()
    a.set_current_method(value = 'delete')
    a.apply_preprocess(data, selected_input_columns)
    print(data)