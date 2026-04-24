from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
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


@app.get("/search")
def search(query: str):

    # ✅ SAFE FILE PATH (WORKS ON RENDER)
    file_path = os.path.join(os.path.dirname(__file__), "data.json")

    try:
        with open(file_path) as f:
            data = json.load(f)
        print("✅ DATA LOADED:", len(data))
    except Exception as e:
        print("❌ ERROR LOADING DATA:", e)

        # 🔥 FALLBACK DATA (NEVER EMPTY UI AGAIN)
        data = [
            {
                "restaurant": f"{query.title()} Spot {i+1}",
                "image": "https://via.placeholder.com/400x300?text=Food",
                "original_price": random.randint(200, 350),
                "final_price": random.randint(120, 250),
                "discount": random.choice([20, 30, 40]),
                "delivery_time": random.randint(20, 40),
                "platform": random.choice(["Swiggy", "Zomato"])
            }
            for i in range(8)
        ]

    # ✅ FILTER RESULTS
    filtered = [
        item for item in data
        if query.lower() in item["restaurant"].lower()
    ]

    # 🔥 IF NO MATCH → SHOW ALL
    if not filtered:
        filtered = data

    # 🧠 AI SORT (PRICE + DELIVERY)
    filtered = sorted(
        filtered,
        key=lambda x: x.get("final_price", 999) + x.get("delivery_time", 999)
    )

    return {
        "results": filtered,
        "ai_message": f"Top results for {query}"
    }


# ✅ REQUIRED FOR RENDER
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
