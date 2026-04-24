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
    return {"message": "Mera AI running 🚀"}


# 🔥 FOOD IMAGE MAP
FOOD_IMAGES = {
    "biryani": "https://upload.wikimedia.org/wikipedia/commons/3/35/Chicken_Biryani.jpg",
    "pizza": "https://upload.wikimedia.org/wikipedia/commons/d/d3/Supreme_pizza.jpg",
    "burger": "https://upload.wikimedia.org/wikipedia/commons/4/4f/Cheeseburger.jpg",
    "dosa": "https://upload.wikimedia.org/wikipedia/commons/9/9b/Dosa.jpg",
    "waffle": "https://upload.wikimedia.org/wikipedia/commons/1/1c/Waffles_with_Strawberries.jpg"
}


# 🔥 FOOD VARIATIONS (AI suggestions)
FOOD_VARIANTS = {
    "biryani": ["chicken biryani", "mutton biryani", "veg biryani", "paneer biryani"],
    "pizza": ["cheese pizza", "farmhouse pizza", "pepperoni pizza", "margherita pizza"],
    "burger": ["chicken burger", "veg burger", "cheese burger"],
    "dosa": ["masala dosa", "plain dosa", "rava dosa"],
}


def get_image(query):
    for key in FOOD_IMAGES:
        if key in query.lower():
            return FOOD_IMAGES[key]
    return "https://via.placeholder.com/400x300?text=Food"


# 🔥 AI SCORING
def score(item):
    return item["final_price"] * 0.5 + item["delivery_time"] * 0.3 - item["discount"] * 0.2


@app.get("/search")
def search(query: str):

    base = query.lower()
    image = get_image(base)

    results = []

    # generate realistic dishes
    for i in range(10):
        results.append({
            "restaurant": f"{query.title()} Hub {i+1}",
            "image": image,
            "original_price": random.randint(200, 350),
            "final_price": random.randint(120, 250),
            "discount": random.choice([20, 30, 40, 50]),
            "delivery_time": random.randint(20, 45),
            "platform": random.choice(["Swiggy", "Zomato"])
        })

    # AI ranking
    results = sorted(results, key=score)

    # suggestions
    suggestions = []
    for key in FOOD_VARIANTS:
        if key in base:
            suggestions = FOOD_VARIANTS[key]

    return {
        "results": results,
        "ai_message": f"Top smart recommendations for {query}",
        "suggestions": suggestions
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
