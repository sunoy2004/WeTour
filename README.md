# WeTour - Travel Experience Platform

WeTour is a modern travel platform that helps users discover and plan trips across India. The platform features an intelligent chatbot, real-time travel information, and a comprehensive trip planning system.

## Features

### 🌟 Modern UI/UX
- Responsive design with Bootstrap 5
- AOS animations for smooth transitions
- Dark mode support
- Modern hero section and consistent design language

### 💬 Intelligent Chatbot
- Custom PyTorch neural network chatbot
- Enhanced tokenization with NLTK and fuzzy matching
- Confidence threshold logic for better responses
- Typing indicators and loading animations

### 🌍 Real-Time Travel Information
- Weather data from OpenWeather API
- City information from GeoDB Cities API
- High-quality travel images from Unsplash API
- Dynamic content for destinations

### 🔥 Firebase Backend
- Firebase Authentication (Email/Password & Google OAuth)
- Firestore for data storage (chat logs, trip plans, user data)
- Firebase Functions for serverless backend logic
- Firebase Hosting for deployment

### 🎯 Advanced Features
- Autocomplete city search
- "Plan My Trip" smart form
- User dashboard with saved itineraries
- Image sliders and lazy loading
- Loading skeletons for API content

## Tech Stack

### Frontend
- HTML5, CSS3, JavaScript
- Bootstrap 5
- AOS Animations
- Firebase SDK

### Backend
- Flask (Python)
- Firebase Functions
- Firebase Authentication
- Firebase Firestore

### AI/ML
- PyTorch for chatbot neural network
- NLTK for natural language processing
- FuzzyWuzzy for fuzzy matching

### APIs
- OpenWeather API
- GeoDB Cities API
- Unsplash API

## Setup Instructions

### Prerequisites
- Node.js (v14 or higher)
- Python (v3.8 or higher)
- Firebase account
- API keys for OpenWeather, GeoDB, and Unsplash

### Installation

1. Clone the repository:
```bash
git clone https://github.com/sunoy2004/WeTour.git
cd WeTour
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install Node.js dependencies:
```bash
cd functions
npm install
cd ..
```

4. Set up environment variables:
Create a `.env` file in the root directory with your API keys:
```env
# Firebase Configuration
FIREBASE_API_KEY=your_firebase_api_key
FIREBASE_AUTH_DOMAIN=your_firebase_auth_domain
FIREBASE_PROJECT_ID=your_firebase_project_id
FIREBASE_STORAGE_BUCKET=your_firebase_storage_bucket
FIREBASE_MESSAGING_SENDER_ID=your_firebase_messaging_sender_id
FIREBASE_APP_ID=your_firebase_app_id
FIREBASE_MEASUREMENT_ID=your_firebase_measurement_id

# API Keys for Travel Services
OPENWEATHER_API_KEY=your_openweather_api_key
GEODB_API_KEY=your_geodb_api_key
UNSPLASH_API_KEY=your_unsplash_api_key
```

5. Train the chatbot:
```bash
python train.py
```

### Running the Application

#### Development Mode
1. Start the Flask server:
```bash
python app.py
```

2. Visit `http://localhost:5000` in your browser

#### Firebase Deployment
1. Deploy Firebase functions:
```bash
firebase deploy --only functions
```

2. Deploy frontend:
```bash
firebase deploy --only hosting
```

## Project Structure

```
WeTour/
├── standalone-frontend/     # Static frontend files
│   ├── index.html          # Main page
│   ├── plan-trip.html      # Trip planning page
│   ├── dashboard.html      # User dashboard
│   ├── app.js              # Frontend JavaScript
│   └── style.css           # Custom styles
├── functions/              # Firebase functions
│   └── index.js            # Cloud functions
├── services/               # API service wrappers
│   ├── weatherService.py   # OpenWeather API
│   ├── geodbService.py     # GeoDB Cities API
│   └── unsplashService.py  # Unsplash API
├── routes/                 # Flask routes
│   └── travelRoutes.py     # Travel API endpoints
├── templates/              # Flask templates
│   └── base.html           # Base template
├── static/                 # Static assets
│   ├── app.js              # Chatbot JavaScript
│   └── style.css           # Styles
├── app.py                  # Flask application
├── chat.py                 # Chatbot logic
├── model.py                # Neural network model
├── train.py                # Model training
├── nltk_utils.py           # NLP utilities
├── intents.json            # Chatbot intents
├── firebase.json           # Firebase configuration
└── requirements.txt        # Python dependencies
```

## API Endpoints

### Chatbot
- `POST /predict` - Get chatbot response

### Travel Information
- `GET /api/travel-info/<destination>` - Get destination information
- `GET /api/weather/<city>` - Get weather information
- `GET /api/cities/<name>` - Search for cities
- `GET /api/photos/<query>` - Search for travel photos

### Forms
- `POST /submit-form` - Submit contact form
- `POST /submit-trip-plan` - Submit trip plan

## Firebase Functions

1. `chatbotPredict` - Handle chatbot predictions
2. `submitTripPlan` - Handle trip plan submissions
3. `getTravelInfo` - Retrieve travel information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Bootstrap for the frontend framework
- Firebase for backend services
- OpenWeather, GeoDB, and Unsplash for APIs
- PyTorch and NLTK for AI/ML components