import textwrap, sys, json

T = """Magnitude {mag} earthquake near {place}.
Time: {time_utc}. Depth about {depth} km.
Quick facts:
- Location: lat {lat:.2f}, lon {lon:.2f}
- What it means: {meaning}
Safety note: aftershocks are common after quakes of this size.
Follow for a 60-second quake update daily."""

def meaning(m):
    if m>=7.5: return "major event; severe damage near epicenter"
    if m>=6.5: return "strong shaking; local damage possible"
    if m>=5.5: return "moderate shaking; weak structures at risk"
    if m>=4.5: return "light shaking; usually minor effects"
    return "generally minor"

def main():
    info=json.load(sys.stdin)
    s=T.format(
        mag=info["mag"],
        place=info["place"] or "the epicenter",
        time_utc=info["time_utc"],
        depth=int(round(info.get("depth_km") or 10)),
        lat=info["lat"] or 0, lon=info["lon"] or 0,
        meaning=meaning(info["mag"])
    )
    print("\n".join(l.strip() for l in s.strip().splitlines()))

if __name__=="__main__":
    main()
