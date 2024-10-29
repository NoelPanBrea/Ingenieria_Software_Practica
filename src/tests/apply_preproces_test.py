import sys
sys.path.insert(0, 'src')
from dataset_calc import *
if __name__ == '__main__':
    data = DataFrame({'a': [1, 2, None], 'b': [4, None, 6,]})
    selected_input_columns = ['a', 'b']
    PreprocessApplier.current_method(PreprocessApplier._methods['delete'])
    PreprocessApplier().apply_preproces(data, selected_input_columns)
    print(data)