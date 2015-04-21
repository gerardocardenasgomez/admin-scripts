from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest
import re

class AddLocationForm(BoxLayout):
    search_input = ObjectProperty()

    def cleanse_input(self, dangerous_string):
        clean_string = re.sub('\W+', '', dangerous_string)
        if clean_string.isalnum():
            return clean_string
        else:
            raise SystemExit("Unable to clean the string!")

    def search_location(self):
        dangerous_string = self.search_input.text
        clean_query = self.cleanse_input(dangerous_string)

        search_template = "http://api.openweathermap.org/data/2.5/find?q={0}&type=like"
        search_url = search_template.format(clean_query)

        request = UrlRequest(search_url, self.found_location)

    def found_location(self, request, data):
        cities = ["{0} ({1})".format(d['name'], d['sys']['country']) for d in data['list']]

        if cities:
            self.search_results.item_strings = cities        
        else:
            self.search_results.item_strings = ["No cities found!"]

class WeatherApp(App):
    pass

if __name__ == '__main__':
    WeatherApp().run()
