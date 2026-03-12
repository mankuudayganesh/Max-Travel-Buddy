import json
import os
import random
from functools import lru_cache
from groq import Groq

# ================= LOAD PLACES JSON =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(BASE_DIR, "..", "frontend", "data", "india_places.json")

with open(json_path, encoding="utf-8") as f:
    travel_data = json.load(f)

# ================= GROQ CLIENT =================
def _get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    return Groq(api_key=api_key)

# ================= FAST HOTEL GENERATOR =================
@lru_cache(maxsize=500)
def get_hotels_fast(district, state):

    hotels = [
        {"hotel": f"{district} Grand Hotel", "rating": 4.5, "area": district},
        {"hotel": f"{district} Palace Residency", "rating": 4.4, "area": district},
        {"hotel": f"{district} Comfort Inn", "rating": 4.3, "area": district},
        {"hotel": f"{district} Royal Stay", "rating": 4.2, "area": district},
        {"hotel": f"{district} City Lodge", "rating": 4.1, "area": district},
    ]

    return hotels

# ================= GENERATE TRIP =================
def generate_trip(destination: str, days: int):

    dest = destination.lower().strip()

    candidates = []

    # ================= FIND MATCHING PLACES =================
    for state, districts in travel_data.items():

        for district, district_places in districts.items():

            state_name = state.lower()
            district_name = district.lower()

            if dest in state_name or dest in district_name:

                for p in district_places:
                    candidates.append({
                        "state": state,
                        "district": district,
                        "place": p
                    })

            else:

                for p in district_places:

                    pn = p.lower()

                    if dest in pn or pn in dest:

                        for x in district_places:
                            candidates.append({
                                "state": state,
                                "district": district,
                                "place": x
                            })

                        break

    # ================= REMOVE DUPLICATES =================
    seen = set()
    unique = []

    for c in candidates:

        key = (c["state"], c["district"], c["place"])

        if key not in seen:
            seen.add(key)
            unique.append(c)

    # ================= FALLBACK PLACES =================
    if not unique:

        unique = [
            {"state": "", "district": "", "place": p}
            for p in [
                "City Tour",
                "Local Market",
                "Temple Visit",
                "Food Street",
                "Nature Park"
            ]
        ]

    random.shuffle(unique)

    itinerary = []
    used_places = set()

    # ================= GENERATE DAY-WISE PLAN =================
    for day in range(days):

        available = [c for c in unique if c["place"] not in used_places]

        if not available:
            break

        chosen = random.choice(available)

        used_places.add(chosen["place"])

        remaining_places = [
            c["place"] for c in unique if c["place"] not in used_places
        ]

        nearby = random.choice(remaining_places) if remaining_places else "Local Area"

        # FAST HOTEL LOOKUP
        hotels = get_hotels_fast(chosen["district"], chosen["state"])

        selected = random.choice(hotels)

        hotel_string = f"{selected['hotel']} ({selected['rating']}★, {selected['area']})"

        itinerary.append({

            "day": day + 1,

            "place": chosen["place"],

            "hotel": hotel_string,

            "nearby": nearby,

            "description": f"Explore {chosen['place']} and enjoy the culture and attractions of {destination.title()}."

        })

    return itinerary