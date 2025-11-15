import random
import json

import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize, expand_synonyms

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"

# Confidence threshold for responses
CONFIDENCE_THRESHOLD = 0.75

# Fallback responses for low confidence
fallback_responses = [
    "I'm not sure I understand. Could you rephrase that?",
    "I didn't quite catch that. Can you ask in a different way?",
    "I'm still learning! Can you provide more details?",
    "Let me connect you with a human agent who can help better.",
    "I'm not confident about this answer. Would you like to try a different question?"
]

# Context memory for follow-up questions
class ChatContext:
    def __init__(self):
        self.context = {}
        self.last_tag = None
        self.last_confidence = 0.0
    
    def set_context(self, key, value):
        self.context[key] = value
    
    def get_context(self, key):
        return self.context.get(key, None)
    
    def clear_context(self):
        self.context = {}
        self.last_tag = None
        self.last_confidence = 0

# Global context instance
chat_context = ChatContext()

def get_response(msg):
    # Expand sentence with synonyms to improve matching
    expanded_msg = expand_synonyms(msg)
    
    # Tokenize both original and expanded sentences
    sentence = tokenize(msg)
    expanded_sentence = tokenize(expanded_msg)
    
    # Use expanded sentence for bag of words
    X = bag_of_words(expanded_sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][int(predicted.item())]
    prob_value = prob.item()
    
    # Store context
    chat_context.last_tag = tag
    chat_context.last_confidence = prob_value
    
    # Check confidence threshold
    if prob.item() > CONFIDENCE_THRESHOLD:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                response = random.choice(intent['responses'])
                
                # Add context-specific information if needed
                if tag == "destination_info":
                    destination = chat_context.get_context("destination")
                    if destination:
                        response += f"\n\nYou mentioned {destination}. Would you like specific information about this destination?"
                
                return response
    else:
        # Use fallback response for low confidence
        return random.choice(fallback_responses) + f" (Confidence: {prob.item():.2f})"
    
    return "I do not understand..."


if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(f"{bot_name}: {resp}")

