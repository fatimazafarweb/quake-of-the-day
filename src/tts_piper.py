import os, sys, subprocess, shutil, pathlib

MODEL = pathlib.Path(os.environ.get("PIPER_MODEL", "models/en_US-amy-medium.onnx"))

def _find_config():
    # Try common names for the config next to the model
    candidates = [
        MODEL.with_suffix(MODEL.suffix + ".json"),  # foo.onnx.json (our download)
        MODEL.with_suffix(".json"),                 # foo.json
        pathlib.Path(str(MODEL) + ".json"),         # also foo.onnx.json
    ]
    for p in candidates:
        if p.exists():
            return str(p)
    return None

def synth(text, out_path):
    cfg = _find_config()

    # Prefer Piper CLI if installed, else python -m piper
    piper_bin = shutil.which("piper")
    if piper_bin:
        cmd = [piper_bin, "--model", str(MODEL), "--output_file", out_path, "--sentence_silence", "0.25"]
        if cfg: cmd += ["--config", cfg]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate(input=text.encode("utf-8"), timeout=180)
        if p.returncode != 0:
            raise RuntimeError(err.decode("utf-8", "ignore"))
        return

    # Fallback: python -m piper
    pycmd = [sys.executable, "-m", "piper", "--model", str(MODEL), "--output_file", out_path, "--sentence_silence", "0.25"]
    if cfg: pycmd += ["--config", cfg]
    p = subprocess.Popen(pycmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=text.encode("utf-8"), timeout=180)
    if p.returncode != 0:
        raise RuntimeError(err.decode("utf-8", "ignore"))

if __name__ == "__main__":
    synth(sys.stdin.read(), sys.argv[1])
