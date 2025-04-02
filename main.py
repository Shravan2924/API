import os
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

# Load CSV data at startup
data = load_responses()

@app.get("/")
def home():
    return {"message": "FastAPI is running on Railway!"}

@app.get("/chat")
def chat(api_key: str, question: str):
    if api_key != "6feff1c5bba2f782611dbd20efb9d169":
        return {"error": "Invalid API Key"}
    return {"question": question, "answer": data.get(question, "I don't know")}

@app.post("/generate-key")
def generate_key():
    key = hashlib.md5(str(time.time()).encode()).hexdigest()
    return {"api_key": key, "message": "Use this key to access the chatbot API."}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))  # Use Railway's dynamic port
    uvicorn.run(app, host="0.0.0.0", port=port)
