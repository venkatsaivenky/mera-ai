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


# ✅ STABLE IMAGE LINKS (NO UNSPLASH)
FOOD_IMAGES = {
    "biryani": "https://upload.wikimedia.org/wikipedia/commons/3/35/Chicken_Biryani.jpg",
    "pizza": "https://upload.wikimedia.org/wikipedia/commons/d/d3/Supreme_pizza.jpg",
    "burger": "https://upload.wikimedia.org/wikipedia/commons/4/4f/Cheeseburger.jpg",
    "dosa": "https://upload.wikimedia.org/wikipedia/commons/9/9b/Dosa.jpg",
    "waffle": "https://upload.wikimedia.org/wikipedia/commons/1/1c/Waffles_with_Strawberries.jpg"
}

def get_image(query):
    q = query.lower()
    for key in FOOD_IMAGES:
        if key in q:
            return FOOD_IMAGES[key]

    return "https://upload.wikimedia.org/wikipedia/commons/6/64/Food_placeholder.png"


@app.get("/search")
def search(query: str):

    results = []

    for i in range(8):
        results.append({
            "restaurant": f"{query.title()} Spot {i+1}",
            "image": get_image(query),  # ✅ ALWAYS WORKS
            "original_price": random.randint(200, 350),
            "final_price": random.randint(120, 250),
            "discount": random.choice([20, 30, 40, 50]),
            "delivery_time": random.randint(20, 45),
            "platform": random.choice(["Swiggy", "Zomato"])
        })

    results = sorted(results, key=lambda x: x["final_price"] + x["delivery_time"])

    return {
        "results": results,
        "ai_message": f"Showing best deals for {query}"
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
