import json, pathlib, subprocess, textwrap
from . import fetch_quake

OUT=pathlib.Path("work"); OUT.mkdir(exist_ok=True)

def main():
    feats=fetch_quake.fetch()
    top=fetch_quake.pick_top(feats)
    info=fetch_quake.simplify(top)
    (OUT/"quake.json").write_text(json.dumps(info,indent=2))

    script=subprocess.check_output(["python","-m","src.make_script"],input=json.dumps(info).encode()).decode()
    (OUT/"script.txt").write_text(script,encoding="utf-8")

    voice = OUT / "voice.wav"
subprocess.run(
    ["python", "-m", "src.tts_piper", str(voice)],
    input=script.encode("utf-8"),
    check=True
)


    video=OUT/"video.mp4"
    subprocess.check_call(["python","-m","src.make_video",str(OUT/"script.txt"),str(voice),str(video)])

    title=f"M{info['mag']} earthquake near {info['place'] or 'reported epicenter'} — quick update #Shorts"
    desc=textwrap.dedent(f"""
    Time (UTC): {info.get('time_utc')}
    Location: lat {info.get('lat')}, lon {info.get('lon')} | Depth: {int(round(info.get('depth_km') or 0))} km
    USGS detail: {info.get('url')}

    Data: USGS Earthquake Hazards Program (Public Domain). Preliminary; subject to change.
    """).strip()
    tags="shorts,earthquake,usgs,geology,geonews"

    (OUT/"title.txt").write_text(title)
    (OUT/"description.txt").write_text(desc)
    (OUT/"tags.txt").write_text(tags)

if __name__=="__main__":
    main()
