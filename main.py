from fastapi.responses import HTMLResponse
from fastapi import Request, Form

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

@app.post("/get_response", response_class=HTMLResponse)
async def get_response(category: str = Form(...), subcategory: str = Form(...)):
    filtered = [
        entry for entry in data
        if entry["category"].lower() == category.lower()
        and entry["subcategory"].lower() == subcategory.lower()
    ]
    if not filtered:
        return f"<h3>No matching {category} found for type: {subcategory}</h3>"

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
