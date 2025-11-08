import shutil, subprocess, sys

def synth(text, out_path):
    # Use espeak-ng (or espeak) only — simple & reliable
    es = shutil.which("espeak-ng") or shutil.which("espeak")
    if not es:
        raise RuntimeError("espeak-ng not found")
    cmd = [es, "-w", out_path, "-s", "175", "-v", "en-us"]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=text.encode("utf-8"), timeout=120)
    if p.returncode != 0:
        raise RuntimeError(err.decode("utf-8", "ignore"))

if __name__ == "__main__":
    synth(sys.stdin.read(), sys.argv[1])
