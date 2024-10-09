# Importamos las clases necesarias de kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

# Clase principal de la aplicación
class SimpleApp(App):
    def build(self):
        # Creamos un layout vertical para colocar los elementos
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Creamos una etiqueta para mostrar el mensaje
        self.label = Label(text="Escribe algo y presiona el botón")
        
        # Creamos un cuadro de texto para ingresar datos
        self.text_input = TextInput(hint_text="Escribe aquí...", size_hint=(1, 0.3))
        
        # Creamos un botón que al presionarlo muestra el contenido del cuadro de texto en la etiqueta
        button = Button(text="Mostrar texto", size_hint=(1, 0.3))
        button.bind(on_press=self.on_button_press)
        
        # Añadimos la etiqueta, cuadro de texto y botón al layout
        layout.add_widget(self.label)
        layout.add_widget(self.text_input)
        layout.add_widget(button)
        
        return layout

    # Método que se ejecuta cuando el botón es presionado
    def on_button_press(self, instance):
        # Obtenemos el texto ingresado y lo mostramos en la etiqueta
        entered_text = self.text_input.text
        self.label.text = f"Has escrito: {entered_text}"

# Ejecutamos la aplicación
if __name__ == '__main__':
    SimpleApp().run()