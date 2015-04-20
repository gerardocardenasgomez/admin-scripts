from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class AddLocationForm(BoxLayout):
    def search_location(self, window_size):
        print "Explicit is better than not explicit heh {0}".format(window_size)

class WeatherApp(App):
    pass

if __name__ == '__main__':
    WeatherApp().run()
