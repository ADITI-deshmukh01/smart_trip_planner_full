import uuid
from datetime import datetime, timedelta
import requests
from geopy.distance import geodesic

# ------------------------
# Geocoding (OpenStreetMap Nominatim)
# ------------------------
def geocode_city(city_name):
    """Return latitude, longitude, and display name for an Indian city."""
    user_agent = {"User-Agent": "smart-trip-planner/1.0"}
    query_list = [
        f"{city_name}, India",
        f"{city_name} city India",
        f"{city_name} district India"
    ]
    for query in query_list:
        try:
            r = requests.get(
                "https://nominatim.openstreetmap.org/search",
                params={"q": query, "format": "json", "limit": 1},
                headers=user_agent,
                timeout=10
            )
            r.raise_for_status()
            data = r.json()
            if data:
                return float(data[0]["lat"]), float(data[0]["lon"]), data[0]["display_name"]
        except Exception:
            continue
    return None, None, None

# ------------------------
# Fetch POIs from Overpass API
# ------------------------
def fetch_pois(lat, lon, radius=5000):
    """Fetch attractions, hotels, restaurants, markets using Overpass API."""
    overpass_url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json][timeout:25];
    (
      node["tourism"="attraction"](around:{radius},{lat},{lon});
      node["tourism"="museum"](around:{radius},{lat},{lon});
      node["tourism"="hotel"](around:{radius},{lat},{lon});
      node["amenity"="restaurant"](around:{radius},{lat},{lon});
      node["shop"="supermarket"](around:{radius},{lat},{lon});
      node["shop"="mall"](around:{radius},{lat},{lon});
    );
    out center 50;
    """
    try:
        r = requests.get(overpass_url, params={"data": query}, timeout=30)
        r.raise_for_status()
        data = r.json()
        pois = {"attractions": [], "hotels": [], "restaurants": [], "markets": []}
        for el in data.get("elements", []):
            tags = el.get("tags", {})
            name = tags.get("name")
            if not name:
                continue
            lat_el = el.get("lat") or el.get("center", {}).get("lat")
            lon_el = el.get("lon") or el.get("center", {}).get("lon")
            if tags.get("tourism") in ["attraction", "museum"]:
                pois["attractions"].append({"name": name, "lat": lat_el, "lon": lon_el})
            elif tags.get("tourism") == "hotel":
                pois["hotels"].append({"name": name, "lat": lat_el, "lon": lon_el})
            elif tags.get("amenity") == "restaurant":
                pois["restaurants"].append({"name": name, "lat": lat_el, "lon": lon_el})
            elif tags.get("shop") in ["supermarket", "mall"]:
                pois["markets"].append({"name": name, "lat": lat_el, "lon": lon_el})
        return pois
    except Exception:
        return {"attractions": [], "hotels": [], "restaurants": [], "markets": []}

# ------------------------
# Calculate distances and travel times
# ------------------------
def calculate_travel_details(attractions):
    travel_details = []
    for i in range(len(attractions)-1):
        start = attractions[i]
        end = attractions[i+1]
        if start.get("lat") and end.get("lat"):
            start_coords = (start["lat"], start["lon"])
            end_coords = (end["lat"], end["lon"])
            distance_km = round(geodesic(start_coords, end_coords).km, 2)
            travel_time_min = round(distance_km / 25 * 60)  # driving estimate
            travel_details.append({
                "from": start["name"],
                "to": end["name"],
                "distance_km": distance_km,
                "travel_time_min": travel_time_min
            })
    return travel_details

# ------------------------
# Orchestrator
# ------------------------
def orchestrate(user_id: str, user_prefs: dict, trip_params: dict):
    destination = trip_params.get("destination")
    num_days = int(trip_params.get("num_days", 3))
    persons = int(trip_params.get("persons", 1))
    start_date_str = trip_params.get("start_date")

    try:
        start_date = datetime.fromisoformat(start_date_str)
    except Exception:
        start_date = datetime.now()

    lat, lon, display_name = geocode_city(destination)
    if not lat or not lon:
        return {"error": "Could not geocode destination"}

    pois = fetch_pois(lat, lon)

    # Skeleton plan
    plan_skeleton = [{"day": i+1, "summary": f"Activities planned in {destination}"} for i in range(num_days)]

    # Detailed itinerary (simple: max 2 attractions per day)
    itinerary = []
    for i in range(num_days):
        day_date = start_date + timedelta(days=i)
        events = []
        for j, poi in enumerate(pois.get("attractions", [])):
            if j >= 2:
                break
            events.append({
                "day": i+1,
                "title": poi["name"],
                "description": f"Visit {poi['name']} in {destination}",
                "location": destination,
                "start": (day_date.replace(hour=9 + j*3, minute=0)).isoformat(),
                "end": (day_date.replace(hour=11 + j*3, minute=0)).isoformat()
            })
        itinerary.append({"day": i+1, "events": events})

    # Cost estimate
    hotel_per_night = 2000
    food_per_day = 500
    transport_per_day = 300
    total = (hotel_per_night + food_per_day + transport_per_day) * num_days * persons

    travel_details = calculate_travel_details(pois.get("attractions", []))

    return {
        "trip_id": f"trip_{uuid.uuid4().hex[:8]}",
        "user_id": user_id,
        "destination_display": display_name,
        "destination": destination,
        "currency": "₹",
        "estimated_cost": total,
        "cost_breakdown": {
            "hotel_per_night": hotel_per_night,
            "hotel_total": hotel_per_night*num_days*persons,
            "food_total": food_per_day*num_days*persons,
            "transport_total": transport_per_day*num_days*persons,
            "total": total
        },
        "plan_skeleton": plan_skeleton,
        "itinerary": itinerary,
        "packing_list": ["Comfortable shoes", "Backpack", "Weather-appropriate clothes", "Personal essentials"],
        "booking_checklist": ["Book hotel", "Plan transport", "Buy attraction tickets", "Carry travel documents", "Check weather"],
        **pois,
        "travel_details": travel_details,
        "travel_estimates": [{"day": i+1, "approx_travel_minutes": 60} for i in range(num_days)]
    }
