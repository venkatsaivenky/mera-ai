from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import random
import logging
from openai import OpenAI

# ✅ Setup logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ OpenAI client (safe init)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Food images
FOOD_IMAGES = {
    "biryani": "https://upload.wikimedia.org/wikipedia/commons/3/35/Chicken_Biryani.jpg",
    "pizza": "https://upload.wikimedia.org/wikipedia/commons/d/d3/Supreme_pizza.jpg",
    "burger": "https://upload.wikimedia.org/wikipedia/commons/4/4f/Cheeseburger.jpg",
    "dosa": "https://upload.wikimedia.org/wikipedia/commons/9/9b/Dosa.jpg",
}

def get_image(query):
    q = query.lower()
    for key in FOOD_IMAGES:
        if key in q:
            return FOOD_IMAGES[key]
    return "https://via.placeholder.com/400x300?text=Food"


# ✅ AI SAFE CALL
def get_ai_response(query, results):
    try:
        prompt = f"""
User query: {query}

Options:
{results}

Give a short recommendation:
- best option
- why
- mention price and delivery
"""

        res = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[{"role": "user", "content": prompt}],
            timeout=5  # ✅ prevents hanging
        )

        return res.choices[0].message.content

    except Exception as e:
        logging.error(f"AI error: {e}")
        return f"Showing best available deals for '{query}'"


@app.get("/")
def home():
    return {"status": "ok", "message": "Mera AI running 🚀"}


@app.get("/search")
def search(query: str):

    if not query or len(query) < 2:
        raise HTTPException(status_code=400, detail="Invalid query")

    image = get_image(query)

    results = []

    for i in range(6):
        results.append({
            "restaurant": f"{query.title()} Hub {i+1}",
            "image": image,
            "original_price": random.randint(200, 350),
            "final_price": random.randint(120, 250),
            "discount": random.choice([20, 30, 40, 50]),
            "delivery_time": random.randint(20, 45),
            "platform": random.choice(["Swiggy", "Zomato"])
        })

    # ✅ smart ranking
    results = sorted(results, key=lambda x: x["final_price"] + x["delivery_time"])

    # ✅ AI (safe)
    ai_message = get_ai_response(query, results[:3])

    return {
        "success": True,
        "query": query,
        "results": results,
        "ai_message": ai_message
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
