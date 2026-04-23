from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import uvicorn
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🧠 USER MEMORY (AI)
user_memory = {}

# 🍽️ SUGGESTION DATABASE
suggestions_db = {
    "biryani": ["chicken biryani", "mutton biryani", "veg biryani"],
    "pizza": ["cheese pizza", "pepperoni pizza", "farmhouse pizza"],
    "burger": ["chicken burger", "veg burger", "cheese burger"],
    "dosa": ["masala dosa", "plain dosa", "rava dosa"],
    "waffle": ["chocolate waffle", "nutella waffle", "strawberry waffle"]
}

@app.get("/")
def home():
    return {"message": "Mera AI working ✅"}

# 🔍 SEARCH (AI powered)
@app.get("/search")
def search(query: str, user: str = "guest"):

    if user not in user_memory:
        user_memory[user] = {
            "cheap": 1,
            "fast": 1,
            "discount": 1
        }

    prefs = user_memory[user]

    results = []

    for i in range(10):
        original = random.randint(150, 400)
        discount = random.choice([20, 30, 40, 50])
        final = round(original * (1 - discount / 100), 2)

        results.append({
            "restaurant": f"Restaurant {i+1}",
            "original_price": original,
            "discount": discount,
            "final_price": final,
            "delivery_time": random.randint(20, 45),
            "platform": random.choice(["Swiggy", "Zomato"])
        })

    # 🧠 AI scoring
    def score(x):
        return (
            x["final_price"] * prefs["cheap"] +
            x["delivery_time"] * prefs["fast"] -
            x["discount"] * prefs["discount"]
        )

    results = sorted(results, key=score)

    return {"results": results}


# 🧠 LEARNING API
@app.get("/feedback")
def feedback(user: str, type: str):

    if user not in user_memory:
        user_memory[user] = {"cheap":1,"fast":1,"discount":1}

    user_memory[user][type] += 1

    return {"message": "AI learned"}


# 🔥 AUTOSUGGEST API
@app.get("/suggest")
def suggest(query: str):

    for key in suggestions_db:
        if key in query.lower():
            return {"suggestions": suggestions_db[key]}

    return {"suggestions": []}


# PORT FIX FOR RENDER
port = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)
