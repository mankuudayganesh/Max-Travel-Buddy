# ================= LOAD ENV =================
from dotenv import load_dotenv
load_dotenv()

# ================= IMPORTS =================
from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from travel_ai import generate_trip
import logging

# ================= APP CONFIG =================
app = FastAPI(
    title="AI Travel Planner API",
    description="Backend API for AI Travel Planner",
    version="1.0"
)

logging.basicConfig(level=logging.INFO)

# ================= CORS =================
# Allow frontend hosted on Vercel to access backend

origins = [
    "*",  # for development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= REQUEST MODEL =================
class TripRequest(BaseModel):
    destination: str
    days: int = Field(gt=0)

# ================= HOME ROUTE =================
@app.get("/")
def home():
    return {
        "status": "running",
        "service": "AI Travel Planner API"
    }

# ================= HEALTH CHECK =================
@app.get("/health")
def health():
    return {"status": "ok"}

# ================= GENERATE TRIP =================
@app.post("/generate-trip")
def generate_trip_api(data: TripRequest):

    destination = data.destination
    days = data.days

    logging.info(f"Generating trip for {destination} - {days} days")

    try:
        plan = generate_trip(destination, days)

        return {
            "destination": destination,
            "days": days,
            "plan": plan
        }

    except Exception as e:
        logging.error(f"Trip generation failed: {str(e)}")
        return {
            "error": "Trip generation failed",
            "details": str(e)
        }

# ================= LOCAL RUN =================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8001,
        reload=True
    )