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


@app.get("/search")
def search(query: str):

    results = []

    for i in range(8):
        results.append({
            "restaurant": f"{query.title()} Spot {i+1}",

            # ✅ ALWAYS WORKING IMAGE (BASED ON QUERY)
            "image": f"https://source.unsplash.com/400x300/?{query},food",

            "original_price": random.randint(200, 350),
            "final_price": random.randint(120, 250),
            "discount": random.choice([20, 30, 40, 50]),
            "delivery_time": random.randint(20, 45),
            "platform": random.choice(["Swiggy", "Zomato"])
        })

    # 🧠 sort by best deal
    results = sorted(results, key=lambda x: x["final_price"] + x["delivery_time"])

    return {
        "results": results,
        "ai_message": f"Showing best deals for {query}"
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
