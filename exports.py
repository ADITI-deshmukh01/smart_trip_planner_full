# exports.py - functions to create iCal content and CSV from itinerary
import csv, io, datetime, textwrap

def itinerary_to_csv(itinerary):
    # itinerary: list of day dicts with events list
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(['day','start','end','title','description','location'])
    for d in itinerary:
        day = d.get('day')
        for ev in d.get('events', []):
            writer.writerow([day, ev.get('start'), ev.get('end'), ev.get('title'), ev.get('description',''), ev.get('location','')])
    return out.getvalue()

def simple_ical(itinerary, uid='trip-1'):
    # minimal iCal generator, not full spec but adequate
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//SmartTripPlanner//EN"]
    for d in itinerary:
        for ev in d.get('events', []):
            start = ev.get('start')
            end = ev.get('end') or start
            # attempt to format ISO to basic YYYYMMDDTHHMMSSZ
            def fmt(t):
                try:
                    dt = datetime.datetime.fromisoformat(t)
                    return dt.strftime('%Y%m%dT%H%M%SZ')
                except Exception:
                    return t.replace('-', '').replace(':','') + 'Z'
            lines += [
                'BEGIN:VEVENT',
                f'UID:{uid}-{d.get("day")}-{ev.get("title").replace(" ", "_")}',
                f'DTSTAMP:{fmt(start)}',
                f'DTSTART:{fmt(start)}',
                f'DTEND:{fmt(end)}',
                f'SUMMARY:{ev.get("title")}',
                f'DESCRIPTION:{ev.get("description","")}', 
                'END:VEVENT'
            ]
    lines.append('END:VCALENDAR')
    return '\n'.join(lines)
