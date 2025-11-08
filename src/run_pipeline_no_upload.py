import json, pathlib, subprocess, textwrap, sys
from . import fetch_quake

OUT = pathlib.Path("work")
OUT.mkdir(exist_ok=True)

def main():
    feats = fetch_quake.fetch()
    top = fetch_quake.pick_top(feats) if feats else None

    if not top:
        info = {
            "place": "No significant events",
            "mag": 3.5,
            "time_utc": "",
            "lat": 0.0, "lon": 0.0, "depth_km": 10,
            "url": "https://earthquake.usgs.gov/"
        }
    else:
        info = fetch_quake.simplify(top)

    (OUT / "quake.json").write_text(json.dumps(info, indent=2), encoding="utf-8")

    script = subprocess.check_output(
        [sys.executable, "-m", "src.make_script"],
        input=json.dumps(info).encode("utf-8")
    ).decode("utf-8")
    (OUT / "script.txt").write_text(script, encoding="utf-8")

    voice = OUT / "voice.wav"
    subprocess.run(
        [sys.executable, "-m", "src.tts_piper", str(voice)],
        input=script.encode("utf-8"),
        check=True
    )

    video = OUT / "video.mp4"
    subprocess.run(
        [sys.executable, "-m", "src.make_video", str(OUT / "script.txt"), str(voice), str(video)],
        check=True
    )

    title = f"M{info['mag']} earthquake near {info['place'] or 'reported epicenter'} — quick update #Shorts"
    desc = textwrap.dedent(f"""\
    Time (UTC): {info.get('time_utc')}
    Location: lat {info.get('lat')}, lon {info.get('lon')} | Depth: {int(round(info.get('depth_km') or 0))} km
    USGS detail: {info.get('url')}

    Data: USGS Earthquake Hazards Program (Public Domain). Preliminary; subject to change.
    """).strip()
    tags = "shorts,earthquake,usgs,geology,geonews"

    (OUT / "title.txt").write_text(title, encoding="utf-8")
    (OUT / "description.txt").write_text(desc, encoding="utf-8")
    (OUT / "tags.txt").write_text(tags, encoding="utf-8")

if __name__ == "__main__":
    main()
