// Unsplash service for travel images
const UNSPLASH_API_KEY = process.env.UNSPLASH_API_KEY;
const BASE_URL = 'https://api.unsplash.com';

class UnsplashService {
  // Search for travel-related photos
  static async searchPhotos(query, perPage = 10) {
    try {
      const response = await fetch(
        `${BASE_URL}/search/photos?query=${encodeURIComponent(query)}&per_page=${perPage}&orientation=landscape`,
        {
          headers: {
            'Authorization': `Client-ID ${UNSPLASH_API_KEY}`
          }
        }
      );
      
      if (!response.ok) {
        throw new Error(`Unsplash API error: ${response.status}`);
      }
      
      const data = await response.json();
      return data.results.map(photo => ({
        id: photo.id,
        url: photo.urls.regular,
        thumb: photo.urls.thumb,
        description: photo.alt_description,
        photographer: {
          name: photo.user.name,
          profile: photo.user.links.html
        }
      }));
    } catch (error) {
      console.error('Error fetching photos:', error);
      throw error;
    }
  }
  
  // Get a random travel photo
  static async getRandomPhoto() {
    try {
      const response = await fetch(
        `${BASE_URL}/photos/random?query=travel&orientation=landscape`,
        {
          headers: {
            'Authorization': `Client-ID ${UNSPLASH_API_KEY}`
          }
        }
      );
      
      if (!response.ok) {
        throw new Error(`Unsplash API error: ${response.status}`);
      }
      
      const data = await response.json();
      return {
        id: data.id,
        url: data.urls.regular,
        thumb: data.urls.thumb,
        description: data.alt_description,
        photographer: {
          name: data.user.name,
          profile: data.user.links.html
        }
      };
    } catch (error) {
      console.error('Error fetching random photo:', error);
      throw error;
    }
  }
}

module.exports = UnsplashService;