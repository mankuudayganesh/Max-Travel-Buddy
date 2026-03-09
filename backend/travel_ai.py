import json
import os
import random

# ================= LOAD JSON DATA =================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(BASE_DIR, "..", "frontend", "data", "india_places.json")

with open(json_path, encoding="utf-8") as f:
    travel_data = json.load(f)


# ================= GENERATE TRIP =================

def generate_trip(destination, days):

    destination = destination.lower().strip()

    places = []

    # ================= SMART SEARCH =================

    for state, districts in travel_data.items():

        for district, district_places in districts.items():

            state_name = state.lower()
            district_name = district.lower()

            # match state
            if destination in state_name:
                places.extend(district_places)

            # match district
            elif destination in district_name:
                places.extend(district_places)

            # match place names
            else:
                for place in district_places:

                    place_name = place.lower()

                    if destination in place_name or place_name in destination:
                        places.extend(district_places)
                        break


    # ================= REMOVE DUPLICATES =================

    places = list(dict.fromkeys(places))

    # ================= FALLBACK =================

    if not places:
        places = [
            "City Tour",
            "Local Market",
            "Temple Visit",
            "Food Street",
            "Nature Park"
        ]

    random.shuffle(places)

    
    # ================= FOOD =================

    foods = [
        "Famous Local Restaurant",
        "Street Food Market",
        "Traditional Food Street",
        "Popular Local Cafe"
    ]

    # ================= CREATE UNIQUE ITINERARY =================

    itinerary = []
    used_places = set()

    for day in range(days):

        available = [p for p in places if p not in used_places]

        if not available:
            break

        place = random.choice(available)
        used_places.add(place)

        nearby_options = [p for p in places if p not in used_places]

        nearby = random.choice(nearby_options) if nearby_options else "Local Area"

        itinerary.append({

            "day": day + 1,
            "place": place,
            "hotel": random.choice(hotels),
            "food": random.choice(foods),
            "nearby": nearby,
            "description": f"Explore {place} and enjoy the culture and attractions of {destination.title()}."

        })

    return itinerary