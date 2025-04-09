import os
import uvicorn
import csv
import random
from fastapi import FastAPI, Query

app = FastAPI()

# Function to load responses from CSV
def load_responses():
    data = []
    try:
        with open("responses.csv", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if "C1" in row and "C2" in row and "C3" in row:
                    data.append({
                        "category": row["C1"].strip(),
                        "subcategory": row["C2"].strip(),
                        "text": row["C3"].strip()
                    })
    except FileNotFoundError:
        print("responses.csv not found.")
    return data

# Load CSV data once at startup
data = load_responses()

# Home route
@app.get("/")
def home():
    return {"message": "Welcome to the Chat API!"}

# Favicon
@app.get("/favicon.ico")
def favicon():
    return {"message": "No favicon available"}

# New Chat endpoint
@app.get("/chat")
def chat(
    category: str = Query(..., description="Type: Joke or Shayari"),
    subcategory: str = Query(..., description="Subcategory like Food, Romantic, etc.")
):
    filtered = [entry for entry in data if entry["category"].lower() == category.lower() and entry["subcategory"].lower() == subcategory.lower()]
    
    if not filtered:
        return {"message": "No matching content found for your request."}
    
    selected = random.choice(filtered)
    return {
        "category": category,
        "subcategory": subcategory,
        "response": selected["text"]
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
