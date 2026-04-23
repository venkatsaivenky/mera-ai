from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
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

# 🧠 USER MEMORY (AI)
user_memory = {}

@app.get("/")
def home():
    return {"message": "Mera AI working ✅"}

@app.get("/search")
def search(query: str, user: str = "guest"):

    if user not in user_memory:
        user_memory[user] = {
            "low_price": 1,
            "fast_delivery": 1,
            "high_discount": 1
        }

    prefs = user_memory[user]

    results = []

    for i in range(10):
        original_price = random.randint(150, 400)
        discount = random.choice([20, 30, 40, 50])
        final_price = round(original_price * (1 - discount/100), 2)

        results.append({
            "restaurant": f"Restaurant {i+1}",
            "original_price": original_price,
            "discount": discount,
            "final_price": final_price,
            "delivery_time": random.randint(20, 45),
            "platform": random.choice(["Swiggy", "Zomato"])
        })

    # 🧠 AI SCORING
    def score(item):
        return (
            item["final_price"] * prefs["low_price"] +
            item["delivery_time"] * prefs["fast_delivery"] -
            item["discount"] * prefs["high_discount"]
        )

    results = sorted(results, key=score)

    return {"results": results}

# 🧠 LEARNING API
@app.get("/feedback")
def feedback(user: str, type: str):

    if user not in user_memory:
        user_memory[user] = {
            "low_price": 1,
            "fast_delivery": 1,
            "high_discount": 1
        }

    if type == "cheap":
        user_memory[user]["low_price"] += 1
    elif type == "fast":
        user_memory[user]["fast_delivery"] += 1
    elif type == "discount":
        user_memory[user]["high_discount"] += 1

    return {"message": "AI learned ✅"}

port = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)
