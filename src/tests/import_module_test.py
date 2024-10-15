import sys
sys.path.insert(0, 'src')
from tkinter import filedialog
from import_module import *

if __name__ == '__main__':
    path = filedialog.askopenfilename(title='elige el archivo que quieres abrir', 
                                      filetypes=[('Todos los archivos', '*.*'),
                                                  ('Archivo SQL', '*.sqlite', '*.db'),
                                                    ('Archivo csv', '*.csv'),
                                                      ('Archivo excel', '*.xlx')])
    datos = load_file(path)