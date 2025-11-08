import os, sys, subprocess, shutil

MODEL = os.environ.get("PIPER_MODEL", "models/en_US-amy-medium.onnx")

def synth(text, out_path):
    # Use installed 'piper' if available; otherwise 'python -m piper'
    piper_bin = shutil.which("piper")
    if piper_bin:
        cmd = [piper_bin, "--model", MODEL, "--output_file", out_path, "--sentence_silence", "0.25"]
    else:
        cmd = [sys.executable, "-m", "piper", "--model", MODEL, "--output_file", out_path, "--sentence_silence", "0.25"]

    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=text.encode("utf-8"), timeout=180)
    if p.returncode != 0:
        raise RuntimeError(err.decode("utf-8", "ignore"))

if __name__ == "__main__":
    synth(sys.stdin.read(), sys.argv[1])
