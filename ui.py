import streamlit as st
from orchestrator import orchestrate
from datetime import datetime

# Streamlit page config
st.set_page_config(page_title="🧭 Smart Trip Planner (India Edition)", layout="wide")

# Main render function
def render():
    st.title("🧭 Smart Trip Planner (India Edition)")
    st.write("Plan trips in India with real-world data from OpenStreetMap.")

    st.sidebar.header("Trip Settings")

    # User Inputs
    destination = st.sidebar.text_input("Destination city", "Banaras")
    start_date = st.sidebar.date_input("Start Date", datetime.now())
    num_days = st.sidebar.number_input("Number of Days", min_value=1, max_value=30, value=3)
    persons = st.sidebar.number_input("Number of Travellers", min_value=1, max_value=10, value=1)
    daily_budget = st.sidebar.number_input("Daily Budget (INR per person)", min_value=100, value=500)

    submitted = st.sidebar.button("Generate Trip Plan")

    if submitted:
        with st.spinner("Building your smart travel plan..."):
            trip_params = {
                "destination": destination,
                "start_date": str(start_date),
                "num_days": num_days,
                "persons": persons
            }

            prefs = {"daily_budget": daily_budget}

            res = orchestrate(
                user_id="test_user",
                user_prefs=prefs,
                trip_params=trip_params
            )

        if "error" in res:
            st.error(res["error"])
            return

        st.success(f"Trip Plan Ready for {res['destination_display']}!")

        # -----------------------------
        # City Highlights
        # -----------------------------
        st.header("🏙️ City Highlights")
        with st.expander("Top Attractions"):
            for a in res.get("attractions", []):
                st.write("•", a["name"])

        with st.expander("Hotels Nearby"):
            for h in res.get("hotels", []):
                st.write(f"🏨 {h['name']} — ({h['lat']}, {h['lon']})")

        with st.expander("Restaurants"):
            for r in res.get("restaurants", []):
                st.write("🍽️", r["name"])

        with st.expander("Markets"):
            for m in res.get("markets", []):
                st.write("🛍️", m["name"])

        # -----------------------------
        # Travel distances and times
        # -----------------------------
        st.header("🛣️ Distances & Travel Times Between Attractions")
        for t in res.get("travel_details", []):
            st.write(f"{t['from']} → {t['to']}: {t['distance_km']} km, approx {t['travel_time_min']} min driving")

        # -----------------------------
        # Cost Estimation
        # -----------------------------
        st.header("💰 Cost Estimate")
        st.write(f"Total Estimated Cost: {res.get('currency', '₹')}{res.get('estimated_cost', 0)}")
        with st.expander("Full Cost Breakdown"):
            cb = res.get("cost_breakdown", {})
            st.write("Hotel per night:", cb.get("hotel_per_night", 0))
            st.write("Hotel total:", cb.get("hotel_total", 0))
            st.write("Food:", cb.get("food_total", 0))
            st.write("Transport:", cb.get("transport_total", 0))
            st.write("Grand Total:", cb.get("total", 0))

        # -----------------------------
        # Day-by-Day Plan
        # -----------------------------
        st.header("📅 Day-by-Day Plan")
        for d in res.get("plan_skeleton", []):
            st.subheader(f"Day {d['day']}: {d['summary']}")

        # -----------------------------
        # Detailed Itinerary
        # -----------------------------
        st.header("📝 Detailed Itinerary")
        for d in res.get("itinerary", []):
            st.subheader(f"Day {d['day']}")
            for event in d.get("events", []):
                start_dt = datetime.fromisoformat(event.get("start"))
                end_dt = datetime.fromisoformat(event.get("end"))
                start_str = start_dt.strftime("%d %b %Y, %I:%M %p")
                end_str = end_dt.strftime("%d %b %Y, %I:%M %p")
                st.write(f"### {event.get('title', '')}")
                st.write(f"🕒 {start_str} → {end_str}")
                st.write(f"📍 {event.get('location', '')}")
                st.write(event.get("description", ""))
                st.divider()

        # -----------------------------
        # Travel Time Estimates
        # -----------------------------
        st.header("⏱ Travel Time Estimates")
        for t in res.get("travel_estimates", []):
            st.write(f"Day {t['day']}: approx {t['approx_travel_minutes']} minutes of travel")

        # -----------------------------
        # Packing List & Booking Checklist
        # -----------------------------
        st.header("🎒 Packing List")
        for item in res.get("packing_list", []):
            st.write("•", item)

        st.header("📌 Booking Checklist")
        for item in res.get("booking_checklist", []):
            st.write("✓", item)

# Run render if executed
if __name__ == "__main__":
    render()
