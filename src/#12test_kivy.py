from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

class TestApp(App):
    def build(self):
        # Establecemos el fondo de la ventana
        Window.clearcolor = (0.18, 0.2, 0.25, 1)  # Color gris oscuro

        # Creamos un layout vertical principal
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)

        # Creamos una etiqueta estilizada
        self.label = Label(text="Escribe algo para comenzar",font_size=24,
            color=(1, 1, 1, 1),  # Texto en color blanco
            size_hint=(1, 0.2))

        # Cuadro de texto para la entrada del usuario
        self.text_input = TextInput(hint_text="Escribe aquí...", multiline=False,padding_y=(10, 10),
            background_color=(0.3, 0.3, 0.3, 1),  # Color de fondo del cuadro de texto
            foreground_color=(1, 1, 1, 1),  # Texto en color blanco
            cursor_color=(1, 1, 1, 1),size_hint=(1, 0.3))

        # Botón con un diseño personalizado
        button = Button(text="Mostrar texto",
            background_color=(0.1, 0.7, 0.5, 1),  # Color del botón (verde)
            font_size=20,
            color=(1, 1, 1, 1),  # Color del texto en el botón
            size_hint=(1, 0.3),bold=True)
        
        button.bind(on_press=self.on_button_press)

        # Añadimos los elementos al layout
        layout.add_widget(self.label)
        layout.add_widget(self.text_input)
        layout.add_widget(button)

        return layout

    # Método que se ejecuta cuando se presiona el botón
    def on_button_press(self, instance):
        entered_text = self.text_input.text
        if entered_text.strip() == "":
            self.label.text = "Por favor, escribe algo."
        else:
            self.label.text = f"Has escrito: {entered_text}"
        self.text_input.text = ""  # Limpiamos el cuadro de texto después de presionar

# Ejecutamos la aplicación
if __name__ == '__main__':
    test_app = TestApp()
    test_app.run() #Ejecuta los métodos de la clase
