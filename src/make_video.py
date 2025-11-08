import numpy as np
from moviepy.editor import AudioFileClip, VideoClip, CompositeVideoClip, ImageClip
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1920

def wave(t):
    y = np.linspace(0, H, H); x = np.linspace(0, W, W); X, Y = np.meshgrid(x, y)
    z = (np.sin((X/120)+(Y/180)+t*2) + np.sin((X/75)-(Y/140)+t)) * 127 + 128
    img = np.stack([z, z, z], axis=2).astype("uint8")
    return img

def _measure(draw, text, font):
    # Pillow safety: use textlength if available, else textbbox width
    if hasattr(draw, "textlength"):
        return draw.textlength(text, font=font)
    return draw.textbbox((0,0), text, font=font)[2]

def make_text_image(text, max_width=W-160, font_size=52, line_height=1.25):
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    try:
        font = ImageFont.truetype(font_path, font_size)
    except Exception:
        font = ImageFont.load_default()

    dummy = Image.new("RGB", (10, 10)); draw = ImageDraw.Draw(dummy)
    words, lines, cur = text.split(), [], []
    for w in words:
        test = " ".join(cur + [w])
        w_px = _measure(draw, test, font)
        if w_px <= max_width or not cur:
            cur.append(w)
        else:
            lines.append(" ".join(cur)); cur = [w]
    if cur: lines.append(" ".join(cur))

    lh = int(font_size * line_height)
    h_needed = 80 + lh*len(lines)
    img = Image.new("RGBA", (W, h_needed), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    x = (W - max_width)//2
    y = 40
    for line in lines:
        draw.text((x, y), line, font=font, fill=(255,255,255,255))
        y += lh
    return np.array(img)

def build(script_path, audio_path, out_path):
    aud = AudioFileClip(audio_path); dur = aud.duration + 2
    bg = VideoClip(lambda t: wave(t), duration=dur).set_fps(30)

    with open(script_path, "r", encoding="utf-8") as f:
        txt = f.read()

    txt_img = make_text_image(txt)
    txt_clip = ImageClip(txt_img).set_duration(dur).set_position(("center","center"))

    credit_img = make_text_image("Data: USGS (Public Domain) • Preliminary", max_width=W-200, font_size=36)
    credit_clip = ImageClip(credit_img).set_duration(dur).set_position(("center", H-180))

    v = CompositeVideoClip([bg, txt_clip, credit_clip]).set_audio(aud).set_duration(dur)
    v.write_videofile(out_path, fps=30, codec="libx264", audio_codec="aac", preset="medium", bitrate="3000k")

if __name__ == "__main__":
    import sys
    build(sys.argv[1], sys.argv[2], sys.argv[3])
