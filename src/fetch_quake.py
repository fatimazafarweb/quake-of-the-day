import requests, datetime, json

USGS = [
  "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/5.0_day.geojson",
  "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson",
  "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson",
]

def fetch():
    for url in USGS:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        data = r.json().get("features", [])
        if data:
            return data
    return []

def pick_top(features):
    def key(f):
        p=f.get("properties",{})
        return (p.get("mag") or 0.0, p.get("time") or 0)
    features=[f for f in features if f.get("properties",{}).get("type")=="earthquake"]
    features.sort(key=key, reverse=True)
    return features[0] if features else None

def simplify(f):
    p=f.get("properties",{}); g=f.get("geometry",{}); c=g.get("coordinates",[None,None,None])
    ts=p.get("time"); ts_utc=datetime.datetime.utcfromtimestamp(ts/1000).strftime("%Y-%m-%d %H:%M UTC") if ts else ""
    return {
      "place": p.get("place"),
      "mag": round(float(p.get("mag") or 0),1),
      "time_utc": ts_utc,
      "lat": c[1], "lon": c[0], "depth_km": c[2] if len(c)>2 else None,
      "url": p.get("url")
    }
