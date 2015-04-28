from kivy.factory import Factory
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest
from kivy.uix.listview import ListItemButton
import re

class LocationButton(ListItemButton):
    pass

class WeatherRoot(BoxLayout):
    def show_current_weather(self, location):
        self.clear_widgets()
        
        current_weather = Factory.CurrentWeather()
        current_weather.location = location
        current_weather.day_of_week = "tuesday"

        self.add_widget(current_weather)

    def show_add_location_form(self):
        self.clear_widgets()
        self.add_widget(AddLocationForm())

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

            # The clear() feature is for Python3        
            #self.search_results.adapter.data.clear()
            # using del instead

            del self.search_results.adapter.data[:]

            self.search_results.adapter.data.extend(cities)
            self.search_results._trigger_reset_populate()
        else:
            self.search_results.item_strings = ["No cities found!"]

class WeatherApp(App):
    pass

if __name__ == '__main__':
    WeatherApp().run()
