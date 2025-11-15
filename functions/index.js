const functions = require('firebase-functions');
const admin = require('firebase-admin');
const axios = require('axios');

// Initialize Firebase Admin SDK
admin.initializeApp();

const db = admin.firestore();

// Function to handle chatbot predictions
exports.chatbotPredict = functions.https.onRequest(async (req, res) => {
  // Set CORS headers
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    // Send response to OPTIONS request
    res.status(204).send('');
    return;
  }

  try {
    const { message } = req.body;
    
    // TODO: Implement chatbot prediction logic
    // For now, we'll return a placeholder response
    const response = {
      answer: "I'm the Firebase-powered chatbot! Your message was: " + message
    };
    
    // Log the chat interaction to Firestore
    if (req.headers.authorization) {
      const token = req.headers.authorization.split('Bearer ')[1];
      const decodedToken = await admin.auth().verifyIdToken(token);
      const userId = decodedToken.uid;
      
      await db.collection('chats').add({
        userId: userId,
        message: message,
        response: response.answer,
        timestamp: admin.firestore.FieldValue.serverTimestamp()
      });
    }
    
    res.status(200).json(response);
  } catch (error) {
    console.error('Error in chatbotPredict:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Function to handle trip plan submissions
exports.submitTripPlan = functions.https.onRequest(async (req, res) => {
  // Set CORS headers
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    // Send response to OPTIONS request
    res.status(204).send('');
    return;
  }

  try {
    const { 
      destination, 
      startDate, 
      endDate, 
      budget, 
      travelers, 
      interests, 
      notes 
    } = req.body;
    
    // Validate required fields
    if (!destination) {
      return res.status(400).json({ error: 'Destination is required' });
    }
    
    // Save trip plan to Firestore
    const tripPlan = {
      destination: destination,
      startDate: startDate,
      endDate: endDate,
      budget: budget,
      travelers: travelers,
      interests: interests || [],
      notes: notes || '',
      createdAt: admin.firestore.FieldValue.serverTimestamp()
    };
    
    // If user is authenticated, associate with their account
    if (req.headers.authorization) {
      const token = req.headers.authorization.split('Bearer ')[1];
      const decodedToken = await admin.auth().verifyIdToken(token);
      tripPlan.userId = decodedToken.uid;
    }
    
    const docRef = await db.collection('tripPlans').add(tripPlan);
    
    res.status(200).json({ 
      message: 'Trip plan submitted successfully!', 
      id: docRef.id 
    });
  } catch (error) {
    console.error('Error in submitTripPlan:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Function to get travel information
exports.getTravelInfo = functions.https.onRequest(async (req, res) => {
  // Set CORS headers
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    // Send response to OPTIONS request
    res.status(204).send('');
    return;
  }

  try {
    // Get destination from query parameters
    const destination = req.query.destination || 'Goa';
    
    // TODO: Implement travel info retrieval from APIs
    // For now, we'll return mock data
    const travelInfo = {
      destination: destination,
      weather: {
        temperature: 28,
        condition: "Sunny",
        humidity: 65
      },
      attractions: [
        "Beaches",
        "Nightlife",
        "Water Sports",
        "Historical Sites"
      ],
      description: `Welcome to ${destination}, a beautiful destination known for its scenic beauty and vibrant culture.`
    };
    
    res.status(200).json(travelInfo);
  } catch (error) {
    console.error('Error in getTravelInfo:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});