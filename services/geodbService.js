// GeoDB Cities service
const GEODB_API_KEY = process.env.GEODB_API_KEY;
const BASE_URL = 'https://wft-geo-db.p.rapidapi.com/v1/geo';

class GeoDBService {
  // Get cities matching a name prefix
  static async getCities(namePrefix, limit = 10) {
    try {
      const response = await fetch(
        `${BASE_URL}/cities?namePrefix=${encodeURIComponent(namePrefix)}&limit=${limit}`,
        {
          headers: {
            'X-RapidAPI-Key': GEODB_API_KEY,
            'X-RapidAPI-Host': 'wft-geo-db.p.rapidapi.com'
          }
        }
      );
      
      if (!response.ok) {
        throw new Error(`GeoDB API error: ${response.status}`);
      }
      
      const data = await response.json();
      return data.data.map(city => ({
        id: city.id,
        name: city.name,
        region: city.region,
        country: city.country,
        latitude: city.latitude,
        longitude: city.longitude,
        population: city.population
      }));
    } catch (error) {
      console.error('Error fetching cities:', error);
      throw error;
    }
  }
  
  // Get city details by ID
  static async getCityDetails(cityId) {
    try {
      const response = await fetch(
        `${BASE_URL}/cities/${cityId}`,
        {
          headers: {
            'X-RapidAPI-Key': GEODB_API_KEY,
            'X-RapidAPI-Host': 'wft-geo-db.p.rapidapi.com'
          }
        }
      );
      
      if (!response.ok) {
        throw new Error(`GeoDB API error: ${response.status}`);
      }
      
      const data = await response.json();
      return {
        id: data.data.id,
        name: data.data.name,
        region: data.data.region,
        country: data.data.country,
        latitude: data.data.latitude,
        longitude: data.data.longitude,
        population: data.data.population,
        elevation: data.data.elevationMeters,
        timezone: data.data.timezone
      };
    } catch (error) {
      console.error('Error fetching city details:', error);
      throw error;
    }
  }
}

module.exports = GeoDBService;