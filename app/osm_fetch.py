import requests

def fetch_city_data(lat, lon, radius=5000):
    """Fetch attractions, hotels, restaurants, markets from Overpass."""
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
    out center;
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
                pois["markets"].append({"name": name})

        return pois
    except Exception:
        return {"attractions": [], "hotels": [], "restaurants": [], "markets": []}
