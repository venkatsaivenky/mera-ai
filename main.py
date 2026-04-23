# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import os

# ✅ Safe OpenAI import (prevents crash)
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except:
    client = None

app = FastAPI()

# ✅ CORS (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Dummy food generator
def generate_results(query):
    results = []
    for i in range(10):
        original_price = random.randint(150, 350)
        discount = random.choice([10, 20, 30, 40, 50])
        final_price = round(original_price * (1 - discount/100), 1)

        results.append({
            "restaurant": f"{query.title()} Spot {i+1}",
            "original_price": original_price,
            "final_price": final_price,
            "discount": discount,
            "delivery_time": random.randint(20, 45),
            "platform": random.choice(["Swiggy", "Zomato"])
        })

    return results


@app.get("/")
def home():
    return {"message": "Mera AI working ✅"}


@app.get("/search")
def search(query: str, user: str = "guest"):

    results = generate_results(query)

    # Sort by best price
    results = sorted(results, key=lambda x: x["final_price"])

    # ✅ AI Message (safe fallback)
    ai_message = f"Showing best deals for {query}"

    if client:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a food recommendation AI."},
                    {"role": "user", "content": f"Suggest best {query} options for {user}"}
                ],
                max_tokens=60
            )

            ai_message = response.choices[0].message.content

        except Exception as e:
            ai_message = f"AI suggestion unavailable (error handled)"

    return {
        "query": query,
        "user": user,
        "results": results,
        "ai_message": ai_message
    }
