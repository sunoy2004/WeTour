// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBgV_HTZnmaDd7pAYqCCRvatgHg_p3qyIs",
  authDomain: "ghoomindia-355e9.firebaseapp.com",
  projectId: "ghoomindia-355e9",
  storageBucket: "ghoomindia-355e9.firebasestorage.app",
  messagingSenderId: "416445254182",
  appId: "1:416445254182:web:cfd4a7103a6a956c97f4e7",
  measurementId: "G-7WQ5N26TMZ"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication and get a reference to the service
export const auth = getAuth(app);

// Initialize Cloud Firestore and get a reference to the service
export const db = getFirestore(app);

export default app;