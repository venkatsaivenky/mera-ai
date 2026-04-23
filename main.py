from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import random
import os

app = FastAPI()

# Enable CORS
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

    # 🔥 Sort by best deal
    results = sorted(results, key=lambda x: (x["final_price"], x["delivery_time"]))

    return {
        "query": query,
        "results": results[:5]
    }

# Render port fix
port = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)
