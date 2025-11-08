import requests, datetime

HEADERS = {"User-Agent": "QuakeOfTheDay/1.0 (+github)"}

def fetch():
    # Query last 24h, sorted by magnitude (stable FDSN API)
    end = datetime.datetime.utcnow()
    start = end - datetime.timedelta(days=1)
    params = {
        "format": "geojson",
        "orderby": "magnitude",
        "starttime": start.strftime("%Y-%m-%dT%H:%M:%S"),
        "endtime": end.strftime("%Y-%m-%dT%H:%M:%S"),
        "minmagnitude": 4.5,
    }
    r = requests.get(
        "https://earthquake.usgs.gov/fdsnws/event/1/query",
        params=params, timeout=45, headers=HEADERS
    )
    r.raise_for_status()
    return r.json().get("features", [])

def pick_top(features):
    def key(f):
        p = f.get("properties", {})
        return (p.get("mag") or 0.0, p.get("time") or 0)
    features = [f for f in features if f.get("properties", {}).get("type") == "]()
