import nltk
from nltk.stem import WordNetLemmatizer
import numpy as np
import json
import pickle
from tensorflow.keras.models import load_model
import random

lemmatizer = WordNetLemmatizer()
# --- Load the saved assets ---
model = load_model('backend/ai_module/chatbot_model.h5')
intents = json.loads(open('backend/ai_module/intents.json').read())
words = pickle.load(open('backend/ai_module/words.pkl', 'rb'))
classes = pickle.load(open('backend/ai_module/classes.pkl', 'rb'))

def clean_up_sentence(sentence):
    """Tokenize and lemmatize the user input."""
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    """Convert the input sentence into a bag-of-words array."""
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    """Predict the intent class (tag) of the user input."""
    bow = bag_of_words(sentence)
    # Filter out predictions below a threshold
    results = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(results) if r > ERROR_THRESHOLD]
    # Sort by probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def get_chatbot_response(msg):
    """Get a random response based on the highest predicted intent."""
    ints = predict_class(msg)
    if not ints:
        # If no intent matches the threshold, use the fallback tag
        tag = 'fallback'
    else:
        tag = ints[0]['intent']

    # Retrieve the response from the intents.json file
    for intent in intents['intents']:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])
    
    # Final fallback just in case
    return "I am sorry, I am currently unavailable. Please check the college website."