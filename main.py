from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
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

    try:
        with open("data.json") as f:
            data = json.load(f)
    except:
        data = []

    # filter results
    filtered = []
    for item in data:
        if query.lower() in item["restaurant"].lower():
            filtered.append(item)

    if not filtered:
        filtered = data

    # AI ranking (price + delivery)
    filtered = sorted(
        filtered,
        key=lambda x: x["final_price"] + x["delivery_time"]
    )

    return {
        "results": filtered,
        "ai_message": f"Top results for {query}"
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
