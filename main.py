from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import random

app = FastAPI()

# FIX CORS (important)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Mera AI working ✅"}

@app.get("/search")
def search(query: str):

    results = []

    for i in range(5):
        results.append({
            "restaurant": f"Restaurant {i+1}",
            "price": random.randint(150, 300),
            "platform": random.choice(["Swiggy", "Zomato"])
        })

    return {"query": query, "results": results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
