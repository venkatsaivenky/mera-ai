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

@app.get("/")
def home():
    return {"message": "Mera AI working ✅"}

@app.get("/search")
def search(query: str):
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

    # 🔥 SMART AI SCORING
    def score(item):
        return (
            item["final_price"] * 0.6 +
            item["delivery_time"] * 0.3 -
            item["discount"] * 0.1
        )

    results = sorted(results, key=score)

    return {
        "query": query,
        "results": results[:10]
    }

port = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)
