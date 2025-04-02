import os
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI is running on Railway!"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Use Railway's assigned port
    uvicorn.run(app, host="0.0.0.0", port=port)
