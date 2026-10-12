# -*- coding: utf-8 -*-
"""生成独立二维码图 qr.png（指向 AI 名片网站），可嵌入公众号/纸质名片等。"""
import qrcode
from PIL import Image, ImageDraw, ImageFont

URL = "https://mashumei.github.io/"   # ← 与 poster.py 的 CARD_URL 保持一致

qr = qrcode.QRCode(box_size=12, border=4,
                   error_correction=qrcode.constants.ERROR_CORRECT_M)
qr.add_data(URL)
qr.make(fit=True)
img = qr.make_image(fill_color="#0F1C36", back_color="white").convert("RGB")

w, h = img.size
label_h = 96
try:
    f = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 40)
except Exception:
    f = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 40)
txt = "马树梅 · 鸿雁归巢 AI 名片"
# 先量文字宽度，画布宽度取二者较大值，避免文字被裁
tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
tl = tmp.textlength(txt, font=f)
canvas_w = max(w, int(tl) + 80)
canvas = Image.new("RGB", (canvas_w, h + label_h), "white")
canvas.paste(img, ((canvas_w - w) // 2, 0))
d = ImageDraw.Draw(canvas)
d.text(((canvas_w - tl) / 2, h + 22), txt, font=f, fill="#0F1C36")
canvas.save("qr.png", "PNG")
print("saved qr.png", canvas.size, "->", URL)
