import uuid
from datetime import datetime, timedelta

def orchestrate(user_id: str, user_prefs: dict, trip_params: dict):
    """
    Main orchestrator for multiple trips and multiple users.
    Always returns a fresh, fully structured result dictionary.
    """

    required_trip_fields = ["destination", "start_date", "days"]
    for field in required_trip_fields:
        if field not in trip_params or not trip_params[field]:
            return {"error": f"Missing required field: {field}"}

    destination = trip_params["destination"]
    num_days = int(trip_params["days"])

    try:
        start_date = datetime.fromisoformat(trip_params["start_date"])
    except Exception:
        start_date = datetime.now()

    trip_id = f"trip_{uuid.uuid4().hex[:10]}"

    neighborhoods = [
        f"Central {destination}",
        f"Old Town {destination}",
        f"Riverside {destination}"
    ]

    attractions = [
        {"name": f"{destination} Museum", "reason": "Top history attraction"},
        {"name": f"{destination} Market", "reason": "Iconic shopping"},
        {"name": f"{destination} Lakefront", "reason": "Scenic views"},
    ]

    plan_skeleton = []
    for i in range(1, num_days + 1):
        plan_skeleton.append({
            "day": i,
            "title": f"Day {i} Activities in {destination}",
            "items": [
                {"time": "09:00", "activity": "Visit to attraction"},
                {"time": "14:00", "activity": "City walk"},
            ]
        })

    itinerary = []
    for i in range(1, num_days + 1):
        day_events = []
        base = start_date + timedelta(days=i - 1)

        day_events.append({
            "start": base.replace(hour=9).isoformat(),
            "end": base.replace(hour=11).isoformat(),
            "title": "Morning Visit",
            "description": f"Explore the top spot in {destination}",
            "location": destination
        })

        day_events.append({
            "start": base.replace(hour=14).isoformat(),
            "end": base.replace(hour=17).isoformat(),
            "title": "Afternoon Walk",
            "description": "Leisurely walk through popular streets",
            "location": "City Center"
        })

        itinerary.append({"day": i, "events": day_events})

    packing = ["comfortable shoes", "umbrella", "power bank"]
    bookings = ["confirm hotel reservation", "buy attraction tickets"]

    estimated_cost = trip_params.get("daily_budget", 100) * num_days

    return {
        "estimated_cost_usd": estimated_cost,
        "recommender": {
            "top_neighborhoods": neighborhoods,
            "top_attractions": attractions,
        },
        "plan": {"days": plan_skeleton},
        "itinerary": {
            "itinerary": itinerary,
            "packing": packing,
            "booking_checklist": bookings
        }
    }
