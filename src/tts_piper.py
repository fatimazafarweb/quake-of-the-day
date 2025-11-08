import os, sys, subprocess, shutil

MODEL = os.environ.get("PIPER_MODEL", "models/en_US-amy-medium.onnx")

def synth(text, out_path):
    # 1) Try Piper CLI
    piper_bin = shutil.which("piper")
    if piper_bin:
        cmd = [piper_bin, "--model", MODEL, "--output_file", out_path, "--sentence_silence", "0.25"]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate(input=text.encode("utf-8"), timeout=180)
        if p.returncode != 0:
            raise RuntimeError(err.decode("utf-8", "ignore"))
        return
    # 2) Fallback: espeak-ng / espeak
    es = shutil.which("espeak-ng") or shutil.which("espeak")
    if es:
        cmd = [es, "-w", out_path, "-s", "175", "-v", "en-us"]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate(input=text.encode("utf-8"), timeout=120)
        if p.returncode != 0:
            raise RuntimeError(err.decode("utf-8", "ignore"))
        return
    raise RuntimeError("No TTS engine found (piper or espeak-ng).")

if __name__ == "__main__":
    synth(sys.stdin.read(), sys.argv[1])
