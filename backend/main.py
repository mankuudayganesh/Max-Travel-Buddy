from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from travel_ai import generate_trip

app = FastAPI(
    title="AI Travel Planner API",
    description="Backend API for AI Travel Planner",
    version="1.0"
)

# ================= CORS =================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= MODELS =================

class TripRequest(BaseModel):
    destination: str
    days: int = Field(gt=0)

# ================= HOME =================

@app.get("/")
def home():
    return {"message": "AI Travel Planner API Running"}

# ================= GENERATE TRIP =================

@app.post("/generate-trip")
def generate_trip_api(data: TripRequest):

    destination = data.destination
    days = data.days

    print("Generating trip:", destination, days)

    plan = generate_trip(destination, days)

    return {
        "destination": destination,
        "days": days,
        "plan": plan
    }

# ================= RUN SERVER =================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)