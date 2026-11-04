import base64, html, io, os
from PIL import Image  # pip install pillow

NAME, TITLE = "Author Name", "Author headline"
OUT = "./posts"
POSTS = {  # filename: (title, image_path, text)
    "post-example.html": ("Example", "/path/to/image.jpg", "Line one.\n\nLine two."),
}

def small_b64(p):
    im = Image.open(p).convert("RGB"); im.thumbnail((640, 640))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=70, optimize=True)
    return base64.b64encode(buf.getvalue()).decode()

os.makedirs(OUT, exist_ok=True)
initials = "".join(w[0] for w in NAME.split()[:2]).upper()
for fn, (title, img, text) in POSTS.items():
    b = small_b64(img)
    js = text.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><style>
body{{margin:0;background:#f3f2ef;font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#1d1d1d;display:flex;justify-content:center;padding:32px 12px}}
.card{{background:#fff;border-radius:10px;box-shadow:0 1px 3px rgba(0,0,0,.12);max-width:560px;width:100%;overflow:hidden}}
.head{{display:flex;align-items:center;gap:12px;padding:16px 16px 8px}}
.av{{width:48px;height:48px;border-radius:50%;background:#0a66c2;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700}}
.name{{font-weight:600}}.sub{{font-size:12px;color:#666}}
.text{{white-space:pre-wrap;padding:8px 16px 16px;font-size:15px;line-height:1.45}}
img{{display:block;width:100%}}
.bar{{padding:12px 16px;border-top:1px solid #eee}}
button{{border:1px solid #0a66c2;color:#0a66c2;background:#fff;border-radius:16px;padding:6px 14px;font-weight:600;cursor:pointer}}
</style></head><body><div class="card">
<div class="head"><div class="av">{initials}</div><div><div class="name">{html.escape(NAME)}</div><div class="sub">{html.escape(TITLE)}</div></div></div>
<div class="text">{html.escape(text)}</div>
<img src="data:image/jpeg;base64,{b}" alt="{html.escape(title)}">
<div class="bar"><button onclick="navigator.clipboard.writeText(`{js}`);this.textContent='Copied'">Copy text</button></div>
</div></body></html>"""
    open(os.path.join(OUT, fn), "w").write(page)
    print(fn, len(page) // 1024, "KB")
