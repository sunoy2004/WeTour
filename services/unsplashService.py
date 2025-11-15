import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class UnsplashService:
    def __init__(self):
        self.api_key = os.getenv('UNSPLASH_API_KEY')
        self.base_url = 'https://api.unsplash.com'
    
    def search_photos(self, query, per_page=10):
        """Search for photos related to a query"""
        try:
            url = f"{self.base_url}/search/photos"
            params = {
                'query': query,
                'per_page': per_page,
                'orientation': 'landscape'
            }
            headers = {
                'Authorization': f'Client-ID {self.api_key}'
            }
            
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            photos = []
            
            for photo in data.get('results', []):
                photos.append({
                    'id': photo['id'],
                    'url': photo['urls']['regular'],
                    'thumb': photo['urls']['thumb'],
                    'description': photo['alt_description'],
                    'photographer': {
                        'name': photo['user']['name'],
                        'profile': photo['user']['links']['html']
                    }
                })
            
            return photos
        except requests.exceptions.RequestException as e:
            print(f"Error fetching photos: {e}")
            return None
        except KeyError as e:
            print(f"Error parsing photos data: {e}")
            return None
    
    def get_random_photo(self, query=None):
        """Get a random photo, optionally related to a query"""
        try:
            url = f"{self.base_url}/photos/random"
            params = {
                'orientation': 'landscape'
            }
            if query:
                params['query'] = query
            headers = {
                'Authorization': f'Client-ID {self.api_key}'
            }
            
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            return {
                'id': data['id'],
                'url': data['urls']['regular'],
                'thumb': data['urls']['thumb'],
                'description': data['alt_description'],
                'photographer': {
                    'name': data['user']['name'],
                    'profile': data['user']['links']['html']
                }
            }
        except requests.exceptions.RequestException as e:
            print(f"Error fetching random photo: {e}")
            return None
        except KeyError as e:
            print(f"Error parsing random photo data: {e}")
            return None

# Example usage
if __name__ == "__main__":
    unsplash_service = UnsplashService()
    
    # Test searching for travel photos
    photos = unsplash_service.search_photos("travel", 5)
    if photos:
        print("Travel photos found:")
        for photo in photos:
            print(f"- {photo['description']} by {photo['photographer']['name']}")