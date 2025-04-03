import os
import uvicorn
import csv
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

# Chat endpoint (No API Key Required)
@app.get("/chat")
def chat(question: str):
    return {"question": question, "answer": data.get(question, "I don't know")}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
