from fastapi import FastAPI, HTTPException
import csv
import hashlib
import time
import json
import os

app = FastAPI()

# API Keys Storage File
API_KEYS_FILE = "api_keys.json"

# Function to load responses from CSV
def load_responses():
    responses = {}
    try:
        with open("responses.csv", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) >= 2:  # Ensure there are at least two columns
                    question, answer = row[0].strip(), row[1].strip()
                    responses[question.lower()] = answer  # Store in lowercase for case-insensitive matching
    except FileNotFoundError:
        print("⚠ responses.csv not found.")
    return responses

# Function to load existing API keys
def load_api_keys():
    if os.path.exists(API_KEYS_FILE):
        with open(API_KEYS_FILE, "r") as f:
            return json.load(f)
    return {}

# Function to save API keys
def save_api_keys(api_keys):
    with open(API_KEYS_FILE, "w") as f:
        json.dump(api_keys, f)

# Load data at startup
data = load_responses()
api_keys = load_api_keys()

# Chat endpoint
@app.get("/chat")
def chat(api_key: str, question: str):
    if api_key not in api_keys.values():
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    answer = data.get(question.lower(), "I don't know")
    return {"question": question, "answer": answer}

# API Key Generator
@app.post("/generate-key")
def generate_key(user_id: str):
    """Generate a unique API key for a user."""
    key = hashlib.md5((user_id + str(time.time())).encode()).hexdigest()
    api_keys[user_id] = key
    save_api_keys(api_keys)
    return {"api_key": key, "message": "Use this key to access the chatbot API."}

# Health Check
@app.get("/")
def root():
    return {"message": "Chatbot API is running!"}
