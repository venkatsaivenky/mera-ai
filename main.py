from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import os
from openai import OpenAI

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔑 OPENAI CLIENT
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🧠 MEMORY
user_memory = {}

@app.get("/")
def home():
    return {"message": "Mera AI working ✅"}


@app.get("/search")
def search(query: str, user: str = "guest"):

    if user not in user_memory:
        user_memory[user] = {"cheap":1,"fast":1,"discount":1}

    prefs = user_memory[user]

    results = []

    for i in range(8):
        original = random.randint(150,400)
        discount = random.choice([20,30,40,50])
        final = round(original*(1-discount/100),2)

        results.append({
            "restaurant": f"Restaurant {i+1}",
            "original_price": original,
            "discount": discount,
            "final_price": final,
            "delivery_time": random.randint(20,45),
            "platform": random.choice(["Swiggy","Zomato"])
        })

    # SORT USING USER PREF
    def score(x):
        return (
            x["final_price"]*prefs["cheap"] +
            x["delivery_time"]*prefs["fast"] -
            x["discount"]*prefs["discount"]
        )

    results = sorted(results, key=score)

    # 🧠 AI REASONING
    try:
        ai_response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role":"system","content":"You are a food recommendation assistant like Swiggy AI."},
                {"role":"user","content":f"User searched: {query}. Explain best recommendation in 2 lines."}
            ]
        )

        explanation = ai_response.choices[0].message.content

    except:
        explanation = "Showing best results based on price, delivery time and discounts."

    return {
        "results": results,
        "ai_message": explanation
    }


@app.get("/feedback")
def feedback(user: str, type: str):
    if user not in user_memory:
        user_memory[user] = {"cheap":1,"fast":1,"discount":1}

    user_memory[user][type] += 1

    return {"message":"AI learned"}
