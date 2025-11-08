import numpy as np
from moviepy.editor import AudioFileClip, VideoClip, CompositeVideoClip, TextClip
W,H=1080,1920

def wave(t):
    import numpy as np
    y=np.linspace(0,H,H); x=np.linspace(0,W,W); X,Y=np.meshgrid(x,y)
    z=(np.sin((X/120)+(Y/180)+t*2)+np.sin((X/75)-(Y/140)+t))*127+128
    img=np.stack([z,z,z],axis=2).astype('uint8')
    return img

def build(script,audio,out):
    aud=AudioFileClip(audio); dur=aud.duration+2
    bg=VideoClip(lambda t: wave(t), duration=dur).set_fps(30)
    with open(script,'r',encoding='utf-8') as f: txt=f.read()
    txtc=(TextClip(txt,fontsize=52,color="white",method="caption",size=(W-160,None),align="West")
          .set_position(("center","center")).set_duration(dur))
    credit=(TextClip("Data: USGS (Public Domain) • Preliminary",fontsize=32,color="white")
            .set_opacity(0.7).set_position(("center",H-100)).set_duration(dur))
    v=CompositeVideoClip([bg,txtc,credit]).set_audio(aud).set_duration(dur)
    v.write_videofile(out,fps=30,codec="libx264",audio_codec="aac",preset="medium",bitrate="3000k")

if __name__=="__main__":
    import sys; build(sys.argv[1],sys.argv[2],sys.argv[3])
