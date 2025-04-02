import os
import uvicorn
import csv
import hashlib
import time
from fastapi import FastAPI

app = FastAPI()

# Function to load responses from CSV
def load_responses():
    responses = {}
    try:
        with open("responses.csv", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) >= 2:
                    question, answer = row[0].strip(), row[1].strip()
                    responses[question] = answer
    except FileNotFoundError:
        print("responses.csv not found.")
    return responses

# Load CSV data once at startup
data = load_responses()

# Function to load API keys from a file
def load_api_keys():
    try:
        with open("api_keys.txt", "r") as f:
            return set(line.strip() for line in f.readlines())
    except FileNotFoundError:
        return set()

# Function to save a new API key
def save_api_key(api_key):
    with open("api_keys.txt", "a") as f:
        f.write(api_key + "\n")

# Chat endpoint
@app.get("/chat")
def chat(api_key: str, question: str):
    valid_keys = load_api_keys()
    
    if api_key not in valid_keys:
        return {"error": "Invalid API Key"}

    return {"question": question, "answer": data.get(question, "I don't know")}

# API Key Generator
@app.post("/generate-key")
def generate_key():
    key = hashlib.md5(str(time.time()).encode()).hexdigest()
    save_api_key(key)  # Save the key automatically
    return {"api_key": key, "message": "Use this key to access the chatbot API."}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
