def generate_itinerary(attractions, days):
    """
    Create a simple itinerary distributing attractions across the given days.
    """
    if not attractions:
        return {}

    itinerary = {}
    per_day = max(1, len(attractions) // days)

    index = 0
    for day in range(1, days + 1):
        day_key = f"Day {day}"
        itinerary[day_key] = []
        for _ in range(per_day):
            if index < len(attractions):
                itinerary[day_key].append(attractions[index])
                index += 1

    # Add remaining attractions
    if index < len(attractions):
        itinerary[f"Day {days}"].extend(attractions[index:])

    return itinerary
