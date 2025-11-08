import os, sys, subprocess

MODEL=os.environ.get("PIPER_MODEL","models/en_US-amy-medium.onnx")
def synth(text,out_path):
    cmd=["piper","--model",MODEL,"--output_file",out_path,"--sentence_silence","0.25"]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=p.communicate(input=text.encode("utf-8"),timeout=120)
    if p.returncode!=0:
        raise RuntimeError(err.decode())

if __name__=="__main__":
    synth(sys.stdin.read(), sys.argv[1])
