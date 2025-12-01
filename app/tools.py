# tools.py - deterministic utilities used by the planner
from datetime import timedelta
import math

def estimate_travel_time_km(distance_km, mode='walking'):
    speeds = {'walking':5, 'biking':15, 'driving':50, 'transit':30}  # km/h
    speed = speeds.get(mode, 5)
    hours = distance_km / speed if speed>0 else 0
    seconds = int(hours * 3600)
    return timedelta(seconds=seconds)

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    from math import radians, sin, cos, sqrt, atan2
    dlat = radians(lat2-lat1)
    dlon = radians(lon2-lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def simple_cost_estimate(days, persons=1, daily_budget=100):
    # returns total in USD (simple)
    return days * persons * daily_budget
