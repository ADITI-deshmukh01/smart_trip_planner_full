import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Returns distance in kilometers between two coordinates.
    """
    R = 6371  # Earth radius (km)
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c


def estimate_travel_time(distance_km):
    """
    Returns travel time in minutes assuming average city driving speed = 40 km/h.
    """
    if distance_km <= 0:
        return 0
    speed_kmph = 40
    return (distance_km / speed_kmph) * 60
