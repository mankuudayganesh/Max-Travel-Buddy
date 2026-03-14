# ================= LOAD ENV =================
from dotenv import load_dotenv
load_dotenv()

# ================= IMPORTS =================
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from travel_ai import generate_trip
import logging
import asyncio

# ================= APP CONFIG =================
app = FastAPI(
    title="AI Travel Planner API",
    description="Backend API for AI Travel Planner",
    version="2.0"
)

logging.basicConfig(level=logging.INFO)

# ================= CORS =================
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= WARM UP FLAG =================
is_warm = False

# ================= REQUEST MODEL =================
class TripRequest(BaseModel):
    destination: str
    days: int = Field(gt=0)

class FeedbackRequest(BaseModel):
    name: str
    email: str
    rating: int
    message: str

# ================= STARTUP EVENT =================
@app.on_event("startup")
async def startup_event():
    global is_warm
    logging.info("🔥 Warming up the server...")
    # Pre-load any heavy modules
    try:
        # Warm up by making a dummy call
        generate_trip("test", 1)
        is_warm = True
        logging.info("✅ Server is warm and ready!")
    except Exception as e:
        logging.error(f"Warm up failed: {e}")

# ================= HOME ROUTE =================
@app.get("/")
def home():
    return {
        "status": "running",
        "service": "AI Travel Planner API",
        "warm": is_warm
    }

# ================= HEALTH CHECK =================
@app.get("/health")
def health():
    return {"status": "ok", "warm": is_warm}

# ================= WARM UP ENDPOINT =================
@app.get("/warmup")
def warmup():
    global is_warm
    if not is_warm:
        try:
            generate_trip("warmup", 1)
            is_warm = True
        except:
            pass
    return {"status": "warm", "ready": True}

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
            "plan": plan,
            "status": "success"
        }
    except Exception as e:
        logging.error(f"Trip generation failed: {str(e)}")
        return {
            "error": "Trip generation failed",
            "details": str(e),
            "status": "error"
        }

# ================= FEEDBACK ENDPOINT =================
@app.post("/feedback")
def submit_feedback(data: FeedbackRequest):
    logging.info(f"Feedback from {data.name}: {data.rating}/5")
    # Store feedback (you can add database later)
    return {
        "status": "success",
        "message": "Thank you for your feedback!"
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