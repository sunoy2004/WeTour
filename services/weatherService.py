import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.base_url = 'https://api.openweathermap.org/data/2.5'
    
    def get_current_weather(self, city):
        """Get current weather for a city"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': round(data['main']['temp']),
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'icon': data['weather'][0]['icon']
            }
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None
        except KeyError as e:
            print(f"Error parsing weather data: {e}")
            return None
    
    def get_forecast(self, city, days=5):
        """Get weather forecast for a city"""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            forecasts = []
            
            # Get one forecast per day
            for i in range(0, min(days * 8, len(data['list'])), 8):
                item = data['list'][i]
                forecasts.append({
                    'datetime': item['dt_txt'],
                    'temperature': round(item['main']['temp']),
                    'description': item['weather'][0]['description'],
                    'icon': item['weather'][0]['icon']
                })
            
            return forecasts
        except requests.exceptions.RequestException as e:
            print(f"Error fetching forecast data: {e}")
            return None
        except KeyError as e:
            print(f"Error parsing forecast data: {e}")
            return None

# Example usage
if __name__ == "__main__":
    weather_service = WeatherService()
    
    # Test with a city
    city = "London"
    weather = weather_service.get_current_weather(city)
    if weather:
        print(f"Weather in {weather['city']}, {weather['country']}:")
        print(f"Temperature: {weather['temperature']}°C")
        print(f"Description: {weather['description']}")
        print(f"Humidity: {weather['humidity']}%")
        print(f"Wind Speed: {weather['wind_speed']} m/s")