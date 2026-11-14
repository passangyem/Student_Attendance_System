from kivy.app import App
from kivy.uix.label import Label

class HelloWorldApp(App):

    def build(self):
        return Label(
            text="Hello World!",
            font_size=30
        )

# Run the application
HelloWorldApp().run()