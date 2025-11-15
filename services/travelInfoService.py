import asyncio
from services.weatherService import WeatherService
from services.geodbService import GeoDBService
from services.unsplashService import UnsplashService

class TravelInfoService:
    def __init__(self):
        self.weather_service = WeatherService()
        self.geodb_service = GeoDBService()
        self.unsplash_service = UnsplashService()
    
    def get_destination_info(self, destination):
        """Get comprehensive information about a destination"""
        # Get information from all services
        weather = self.weather_service.get_current_weather(destination)
        cities = self.geodb_service.get_cities(destination, 5)
        photos = self.unsplash_service.search_photos(destination, 6)
        
        return {
            'destination': destination,
            'weather': weather,
            'cities': cities,
            'photos': photos
        }
    
    def get_destination_details(self, city_id):
        """Get detailed information about a specific city"""
        city_details = self.geodb_service.get_city_details(city_id)
        if city_details:
            photos = self.unsplash_service.search_photos(city_details['name'], 4)
            weather = self.weather_service.get_current_weather(city_details['name'])
            
            return {
                'city': city_details,
                'photos': photos,
                'weather': weather
            }
        return None

# Example usage
if __name__ == "__main__":
    travel_service = TravelInfoService()
    
    # Test getting information about a destination
    destination_info = travel_service.get_destination_info("Paris")
    if destination_info:
        print(f"Information about {destination_info['destination']}:")
        if destination_info['weather']:
            print(f"Weather: {destination_info['weather']['temperature']}°C, {destination_info['weather']['description']}")
        if destination_info['cities']:
            print(f"Found {len(destination_info['cities'])} cities")
        if destination_info['photos']:
            print(f"Found {len(destination_info['photos'])} photos")