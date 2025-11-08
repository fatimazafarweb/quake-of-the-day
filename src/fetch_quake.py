import requests, datetime

HEADERS = {"User-Agent": "QuakeOfTheDay/1.0 (+github)"}

# Try several summary feeds; if they fail, use the FDSN query API for the last 24h.
SUMMARY_FEEDS = [
    "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson",
    "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson",
    "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_day.geojson",
    "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson",
    "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_week.geojson",
    "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson",
]

def fetch():
    # Try summary feeds first
    for url in SUMMARY_FEEDS:
        try:
            r = requests.get(url, timeout=30, headers=HEADERS)
            if r.status_code == 200:
                feats = r.json().get("features", [])
                if feats:
                    return feats
        except Exception:
            continue

    # Fallback: query the last 24 hours ordered by magnitude
    end = datetime.datetime.utcnow()
    start = end - datetime.timedelta(days=1)
    params = {
        "format": "geojson",
        "orderby": "magnitude",
        "starttime": start.strftime("%Y-%m-%dT%H:%M:%S"),
        "endtime": end.strftime("%Y-%m-%dT%H:%M:%S"),
        "minmagnitude": 4.5,
    }
    r = requests.get("https://earthquake.usgs.gov/fdsnws/event/1/query",
                     params=params, timeout=45, headers=HEADERS)
    r.raise_for_status()
    return r.json().get("features", [])

def pick_top(features):
    def key(f):
        p=f.get("properties",{})
        return (p.get("mag") or 0.0, p.get("time") or 0)
    features=[f for f in features if f.get("properties",{}).get("type")=="earthquake"]
    features.sort(key=key, reverse=True)
    return features[0] if features else None

def simplify(f):
    p=f.get("properties",{}); g=f.get("geometry",{}); c=g.get("coordinates",[None,None,None])
    ts=p.get("time")
    ts_utc = (datetime.datetime.utcfromtimestamp(ts/1000).strftime("%Y-%m-%d %H:%M UTC")
              if ts else "")
    return {
      "place": p.get("place"),
      "mag": round(float(p.get("mag") or 0),1),
      "time_utc": ts_utc,
      "lat": c[1], "lon": c[0], "depth_km": c[2] if len(c)>2 else None,
      "url":
