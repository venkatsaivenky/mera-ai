from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import random

app = FastAPI()

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


# ✅ FIXED FOOD IMAGES (NO BROKEN LINKS)
food_images = {
    "biryani": "https://images.unsplash.com/photo-1604908176997-431c3e7a9b0f?auto=format&fit=crop&w=800&q=80",
    "pizza": "https://images.unsplash.com/photo-1548365328-9f547fb0953a?auto=format&fit=crop&w=800&q=80",
    "burger": "https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=800&q=80",
    "dosa": "https://images.unsplash.com/photo-1668236543090-82eba5ee5976?auto=format&fit=crop&w=800&q=80",
    "waffle": "https://images.unsplash.com/photo-1504754524776-8f4f37790ca0?auto=format&fit=crop&w=800&q=80"
}


def get_image(query):
    for key in food_images:
        if key in query.lower():
            return food_images[key]

    return "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=800&q=80"


@app.get("/search")
def search(query: str):

    results = []

    for i in range(8):
        results.append({
            "restaurant": f"{query.title()} Spot {i+1}",
            "image": get_image(query),
            "original_price": random.randint(200, 350),
            "final_price": random.randint(120, 250),
            "discount": random.choice([20, 30, 40, 50]),
            "delivery_time": random.randint(20, 45),
            "platform": random.choice(["Swiggy", "Zomato"])
        })

    # AI-style sorting
    results = sorted(results, key=lambda x: x["final_price"] + x["delivery_time"])

    return {
        "results": results,
        "ai_message": f"Showing best deals for {query}"
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
