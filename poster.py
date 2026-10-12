# -*- coding: utf-8 -*-
"""
生成马树梅 AI 名片「分享海报」(1080x1920 朋友圈竖图)。
二维码 = 指向 AI 名片网站链接（长按扫码直达主页），不是微信二维码。
真实素材：assets/portrait.jpg（头像）。微信二维码不放海报上。
"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import qrcode

# ============ 可配置项（改这里即可重生成）============
CARD_URL = "https://mashumei.github.io/?v=3"  # ?v=3 防微信缓存旧卡片页；下次改版升 v=4 即可
AVATAR   = "assets/portrait.jpg"
OUT      = "poster.png"

W, H = 1080, 1920
NAVY   = (15, 28, 54)
NAVY2  = (22, 40, 74)
WHITE  = (245, 247, 250)
GREY   = (165, 178, 198)
GOLD   = (200, 164, 92)
GOLD_S = (214, 184, 120)

def font(size, bold=False):
    try:
        if bold:
            return ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", size)
        return ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", size)
    except Exception:
        return ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", size)

def ctext(d, cx, y, txt, fnt, fill):
    l = d.textlength(txt, font=fnt)
    d.text((cx - l / 2, y), txt, font=fnt, fill=fill)

def rrect(d, box, r, fill):
    d.rounded_rectangle(box, radius=r, fill=fill)

# ---------- 背景 ----------
img = Image.new("RGB", (W, H), NAVY)
d = ImageDraw.Draw(img)
# 顶部柔光
halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(halo).ellipse([W - 640, -380, W + 360, 620], fill=(200, 164, 92, 55))
halo = halo.filter(ImageFilter.GaussianBlur(95))
img = Image.alpha_composite(img.convert("RGBA"), halo).convert("RGB")
d = ImageDraw.Draw(img)
# 底部柔光
halo2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(halo2).ellipse([-300, H - 380, 360, H + 260], fill=(200, 164, 92, 38))
halo2 = halo2.filter(ImageFilter.GaussianBlur(95))
img = Image.alpha_composite(img.convert("RGBA"), halo2).convert("RGB")
d = ImageDraw.Draw(img)

# ---------- 头像（圆形金边）----------
av = Image.open(AVATAR).convert("RGB")
s = 280
av = av.resize((s, s))
mask = Image.new("L", (s, s), 0)
ImageDraw.Draw(mask).ellipse([0, 0, s, s], fill=255)
ring = Image.new("RGBA", (s + 16, s + 16), (0, 0, 0, 0))
ImageDraw.Draw(ring).ellipse([0, 0, s + 16, s + 16], fill=GOLD + (255,))
ring.paste(av, (8, 8), mask)
img.paste(ring, ((W - s - 16) // 2, 150), ring)
ay = 150 + s + 16

# ---------- 姓名 / 头衔 ----------
ctext(d, W // 2, ay + 36, "马树梅", font(72, True), WHITE)
ctext(d, W // 2, ay + 128, "（梅子）", font(40, True), GOLD)
ctext(d, W // 2, ay + 196, "传统企业 AI 增长实践者", font(38), GREY)

# ---------- 主张 ----------
sy = ay + 300
ctext(d, W // 2, sy, "经营自己，也经营企业", font(52, True), WHITE)
ctext(d, W // 2, sy + 78, "让值得被看见的人和企业，更容易被看见", font(34), GREY)

# ---------- 网站二维码卡片 ----------
qsize = 380
qr = qrcode.QRCode(box_size=10, border=2,
                   error_correction=qrcode.constants.ERROR_CORRECT_M)
qr.add_data(CARD_URL)
qr.make(fit=True)
qimg = qr.make_image(fill_color="#0F1C36", back_color="white").convert("RGB")
qimg = qimg.resize((qsize, qsize))
qy = sy + 180
card_w, card_h = 560, qsize + 200
cx0 = (W - card_w) // 2
cy0 = qy - 50
rrect(d, [cx0, cy0, cx0 + card_w, cy0 + card_h], 28, (255, 255, 255))
qx = (W - qsize) // 2
img.paste(qimg, (qx, qy))
ctext(d, W // 2, qy + qsize + 26, "长按识别，进入我的 AI 名片", font(40, True), NAVY)
ctext(d, W // 2, qy + qsize + 84, "扫一扫，认识真实的我", font(30), GREY)

# ---------- 底部服务 / 署名 ----------
by = cy0 + card_h + 70
ctext(d, W // 2, by, "① 企业线上可见性检查   ② 老板 IP 与 AI 内容", font(30), GREY)
ctext(d, W // 2, by + 46, "③ 线上获客优化", font(30), GREY)
ctext(d, W // 2, by + 120, "微信：yizhimei569", font(30), GOLD_S)
ctext(d, W // 2, H - 70, "鸿雁归巢 · 马树梅", font(32, True), GOLD)

img.save(OUT, "PNG")
print("saved", OUT, img.size)
