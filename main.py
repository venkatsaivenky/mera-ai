from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
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

# ---------------- DB SETUP ----------------
conn = sqlite3.connect("mera.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
    username TEXT,
    query TEXT
)
""")

conn.commit()

# ---------------- AUTH ----------------

@app.post("/signup")
def signup(username: str, password: str):
    try:
        cursor.execute("INSERT INTO users VALUES (?,?)", (username, password))
        conn.commit()
        return {"msg": "User created"}
    except:
        raise HTTPException(400, "User exists")

@app.post("/login")
def login(username: str, password: str):
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username,password))
    user = cursor.fetchone()
    if user:
        return {"msg": "success"}
    else:
        raise HTTPException(401, "Invalid login")

# ---------------- SEARCH ----------------

FOOD_IMAGES = {
    "pizza": "https://upload.wikimedia.org/wikipedia/commons/d/d3/Supreme_pizza.jpg",
    "biryani": "https://upload.wikimedia.org/wikipedia/commons/3/35/Chicken_Biryani.jpg"
}

def get_image(q):
    for k in FOOD_IMAGES:
        if k in q.lower():
            return FOOD_IMAGES[k]
    return "https://via.placeholder.com/400x300"

@app.get("/search")
def search(query: str, user: str):

    # save history
    cursor.execute("INSERT INTO history VALUES (?,?)", (user, query))
    conn.commit()

    results = []

    for i in range(6):
        results.append({
            "restaurant": f"{query.title()} Hub {i+1}",
            "image": get_image(query),
            "final_price": random.randint(120,250),
            "original_price": random.randint(200,350),
            "discount": random.choice([20,30,40]),
            "delivery_time": random.randint(20,45),
            "platform": random.choice(["Swiggy","Zomato"])
        })

    results = sorted(results, key=lambda x: x["final_price"])

    return {
        "results": results,
        "ai_message": f"Top results for {query}"
    }

@app.get("/history")
def get_history(user: str):
    cursor.execute("SELECT query FROM history WHERE username=?", (user,))
    return [x[0] for x in cursor.fetchall()]
