from flask import Blueprint, jsonify, request
from services.travelInfoService import TravelInfoService

# Create blueprint
router = Blueprint('travel', __name__)

# Initialize travel service
travel_service = TravelInfoService()

@router.get('/weather/<city>')
def get_weather(city):
    """Get weather information for a city"""
    try:
        weather = travel_service.weather_service.get_current_weather(city)
        if weather:
            return jsonify(weather)
        else:
            return jsonify({'error': 'Could not fetch weather data'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@router.get('/cities/<name>')
def get_cities(name):
    """Get cities matching a name prefix"""
    try:
        limit = request.args.get('limit', 10, type=int)
        cities = travel_service.geodb_service.get_cities(name, limit)
        if cities:
            return jsonify(cities)
        else:
            return jsonify({'error': 'Could not fetch cities data'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@router.get('/photos/<query>')
def get_photos(query):
    """Get travel photos for a query"""
    try:
        per_page = request.args.get('per_page', 10, type=int)
        photos = travel_service.unsplash_service.search_photos(query, per_page)
        if photos:
            return jsonify(photos)
        else:
            return jsonify({'error': 'Could not fetch photos'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@router.get('/info/<destination>')
def get_destination_info(destination):
    """Get comprehensive information about a destination"""
    try:
        info = travel_service.get_destination_info(destination)
        return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@router.get('/details/<city_id>')
def get_city_details(city_id):
    """Get detailed information about a specific city"""
    try:
        details = travel_service.get_destination_details(city_id)
        if details:
            return jsonify(details)
        else:
            return jsonify({'error': 'Could not fetch city details'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500