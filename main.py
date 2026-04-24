from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

foods = {
    "biryani": ["Chicken Biryani", "Hyderabadi Biryani", "Veg Biryani"],
    "pizza": ["Margherita Pizza", "Farmhouse Pizza", "Cheese Burst Pizza"],
    "burger": ["Chicken Burger", "Veg Burger", "Cheese Burger"],
    "dosa": ["Masala Dosa", "Plain Dosa", "Butter Dosa"],
    "pasta": ["White Sauce Pasta", "Red Sauce Pasta"],
    "noodles": ["Hakka Noodles", "Schezwan Noodles"],
}

@app.get("/")
def home():
    return {"message": "Mera AI working ✅"}

@app.get("/search")
def search(query: str):

    query_lower = query.lower()

    food_type = None
    for key in foods:
        if key in query_lower:
            food_type = key
            break

    if not food_type:
        food_type = random.choice(list(foods.keys()))

    results = []

    for i in range(10):
        original_price = random.randint(150, 350)
        discount = random.choice([20, 30, 40, 50])
        delivery_time = random.randint(20, 45)

        final_price = round(original_price * (1 - discount / 100), 1)

        # 🧠 AI SCORE
        score = (100 - final_price) + (50 - delivery_time)

        results.append({
            "restaurant": f"{random.choice(foods[food_type])} Spot {i+1}",
            "original_price": original_price,
            "final_price": final_price,
            "discount": discount,
            "delivery_time": delivery_time,
            "platform": random.choice(["Zomato", "Swiggy"]),
            "score": score
        })

    # 🔥 SORT BY AI LOGIC
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return {
        "query": query,
        "results": results,
        "ai_message": f"Top recommendations for {query} based on price & delivery time"
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
