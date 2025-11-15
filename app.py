from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from chat import get_response
from routes.travelRoutes import router as travel_routes
from services.travelInfoService import TravelInfoService

app = Flask(__name__)
CORS(app)

# Register routes
app.register_blueprint(travel_routes, url_prefix='/api/travel')

@app.get("/")
def index_get():
    # Serve the new standalone frontend index.html
    return send_from_directory('standalone-frontend', 'index.html')

@app.get("/dashboard")
@app.get("/dashboard.html")
def dashboard_get():
    # Serve the dashboard page
    return send_from_directory('standalone-frontend', 'dashboard.html')

@app.get("/plan-trip")
@app.get("/plan-trip.html")
def plan_trip_get():
    # Serve the plan trip page
    return send_from_directory('standalone-frontend', 'plan-trip.html')

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    # TODO: check if text is valid 
    response = get_response(text)
    message={"answer":response}
    return jsonify(message)

# Form submission endpoint
@app.post("/submit-form")
def submit_form():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        destination = data.get('destination')
        
        # TODO: Save to Firebase or database
        # For now, just return success
        return jsonify({
            "message": f"Thank you {name}! Your trip to {destination} has been registered. We'll contact you at {email} shortly.",
            "status": "success"
        })
    except Exception as e:
        return jsonify({
            "message": "Failed to submit form",
            "error": str(e),
            "status": "error"
        }), 500

# Serve static files from standalone-frontend subdirectories
@app.route('/css/<path:filename>')
def css_files(filename):
    return send_from_directory('standalone-frontend/css', filename)

@app.route('/js/<path:filename>')
def js_files(filename):
    return send_from_directory('standalone-frontend/js', filename)

@app.route('/img/<path:filename>')
def img_files(filename):
    return send_from_directory('standalone-frontend/img', filename)

@app.route('/lib/<path:filename>')
def lib_files(filename):
    return send_from_directory('standalone-frontend/lib', filename)

@app.route('/scss/<path:filename>')
def scss_files(filename):
    return send_from_directory('standalone-frontend/scss', filename)

@app.route('/mail/<path:filename>')
def mail_files(filename):
    return send_from_directory('standalone-frontend/mail', filename)

# Trip plan submission endpoint
@app.post("/submit-trip-plan")
def submit_trip_plan():
    try:
        data = request.get_json()
        destination = data.get('destination')
        start_date = data.get('startDate')
        end_date = data.get('endDate')
        budget = data.get('budget')
        travelers = data.get('travelers')
        interests = data.get('interests', [])
        notes = data.get('notes', '')
        
        # TODO: Save to Firebase or database
        # For now, just return success
        return jsonify({
            "message": f"Your trip plan to {destination} has been submitted successfully! We'll create a customized itinerary for your travel dates from {start_date} to {end_date}.",
            "status": "success"
        })
    except Exception as e:
        return jsonify({
            "message": "Failed to submit trip plan",
            "error": str(e),
            "status": "error"
        }), 500

# Travel info endpoint
@app.get("/api/travel-info/<destination>")
def get_travel_info(destination):
    try:
        travel_service = TravelInfoService()
        info = travel_service.get_destination_info(destination)
        return jsonify(info)
    except Exception as e:
        return jsonify({
            "message": "Failed to fetch travel information",
            "error": str(e)
        }), 500

if __name__=="__main__":
    app.run(debug=True)