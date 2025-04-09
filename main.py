import os
import uvicorn
import csv
import random
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

# Load responses from CSV
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

data = load_responses()

# Home page – Ask for Joke/Shayari
@app.get("/", response_class=HTMLResponse)
async def home_form():
    return """
    <html>
        <head><title>Railway Chat</title></head>
        <body>
            <h2>What do you want to hear?</h2>
            <form action="/select_type" method="post">
                <input type="text" name="category" placeholder="Joke or Shayari" required>
                <button type="submit">Next</button>
            </form>
        </body>
    </html>
    """

# Ask for subcategory
@app.post("/select_type", response_class=HTMLResponse)
async def select_type(category: str = Form(...)):
    return f"""
    <html>
        <head><title>Select Subcategory</title></head>
        <body>
            <h2>What kind of {category}?</h2>
            <form action="/get_response" method="post">
                <input type="hidden" name="category" value="{category}">
                <input type="text" name="subcategory" placeholder="e.g. Food, Romantic, College" required>
                <button type="submit">Get {category}</button>
            </form>
        </body>
    </html>
    """

# Show response
@app.post("/get_response", response_class=HTMLResponse)
async def get_response(category: str = Form(...), subcategory: str = Form(...)):
    filtered = [
        entry for entry in data
        if entry["category"].lower() == category.lower()
        and entry["subcategory"].lower() == subcategory.lower()
    ]
    if not filtered:
        return f"""
        <html>
            <head><title>No Match</title></head>
            <body>
                <h3>No matching {category} found for type: {subcategory}</h3>
                <a href="/">Try Again</a>
            </body>
        </html>
        """

    selected = random.choice(filtered)
    return f"""
    <html>
        <head><title>Your {category}</title></head>
        <body>
            <h2>Here's your {category} ({subcategory}):</h2>
            <p>{selected['text']}</p>
            <br>
            <a href="/">Try Again</a>
        </body>
    </html>
    """

# API fallback for /chat (if needed)
@app.get("/chat")
def chat(category: str, subcategory: str):
    filtered = [
        entry for entry in data
        if entry["category"].lower() == category.lower()
        and entry["subcategory"].lower() == subcategory.lower()
    ]
    if not filtered:
        return {"message": f"No {category} found for {subcategory}"}

    selected = random.choice(filtered)
    return {
        "category": category,
        "subcategory": subcategory,
        "response": selected["text"]
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
