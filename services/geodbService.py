import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeoDBService:
    def __init__(self):
        self.api_key = os.getenv('GEODB_API_KEY')
        self.base_url = 'https://wft-geo-db.p.rapidapi.com/v1/geo'
        self.headers = {
            'X-RapidAPI-Key': self.api_key,
            'X-RapidAPI-Host': 'wft-geo-db.p.rapidapi.com'
        }
    
    def get_cities(self, name_prefix, limit=10):
        """Get cities matching a name prefix"""
        try:
            url = f"{self.base_url}/cities"
            params = {
                'namePrefix': name_prefix,
                'limit': limit
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            cities = []
            
            for city in data.get('data', []):
                cities.append({
                    'id': city['id'],
                    'name': city['name'],
                    'region': city['region'],
                    'country': city['country'],
                    'latitude': city['latitude'],
                    'longitude': city['longitude'],
                    'population': city['population']
                })
            
            return cities
        except requests.exceptions.RequestException as e:
            print(f"Error fetching cities: {e}")
            return None
        except KeyError as e:
            print(f"Error parsing cities data: {e}")
            return None
    
    def get_city_details(self, city_id):
        """Get detailed information about a city"""
        try:
            url = f"{self.base_url}/cities/{city_id}"
            
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            city = data.get('data', {})
            
            return {
                'id': city.get('id'),
                'name': city.get('name'),
                'region': city.get('region'),
                'country': city.get('country'),
                'latitude': city.get('latitude'),
                'longitude': city.get('longitude'),
                'population': city.get('population'),
                'elevation': city.get('elevationMeters'),
                'timezone': city.get('timezone')
            }
        except requests.exceptions.RequestException as e:
            print(f"Error fetching city details: {e}")
            return None
        except KeyError as e:
            print(f"Error parsing city details: {e}")
            return None

# Example usage
if __name__ == "__main__":
    geodb_service = GeoDBService()
    
    # Test searching for cities
    cities = geodb_service.get_cities("London", 5)
    if cities:
        print("Cities found:")
        for city in cities:
            print(f"- {city['name']}, {city['country']}")