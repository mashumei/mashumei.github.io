# -*- coding: utf-8 -*-
"""
批量生成「马树梅 AI 名片」推广海报（1080x1920 朋友圈竖图）。
每一张都是同一品牌模板，按名片内容拆出不同推广角度；
二维码均指向名片网站 https://mashumei.github.io/（长按扫码直达）。
真实素材：assets/portrait.jpg（头像）。微信二维码不放海报上。
"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import qrcode, os

CARD_URL = "https://mashumei.github.io/?v=3"
AVATAR   = "assets/portrait.jpg"
W, H     = 1080, 1920

NAVY   = (15, 28, 54)
NAVY2  = (22, 40, 74)
WHITE  = (245, 247, 250)
GREY   = (165, 178, 198)
GOLD   = (200, 164, 92)
GOLD_S = (214, 184, 120)

def font(size, bold=False):
    try:
        return ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc", size)
    except Exception:
        return ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", size)

def ctext(d, cx, y, txt, fnt, fill):
    d.text((cx - d.textlength(txt, font=fnt) / 2, y), txt, font=fnt, fill=fill)

def rrect(d, box, r, fill):
    d.rounded_rectangle(box, radius=r, fill=fill)

def make_qr(size):
    qr = qrcode.QRCode(box_size=10, border=2, error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(CARD_URL)
    qr.make(fit=True)
    q = qr.make_image(fill_color="#0F1C36", back_color="white").convert("RGB").resize((size, size))
    return q

def build(theme, out):
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    # 顶部柔光
    halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse([W - 640, -380, W + 360, 620], fill=(200, 164, 92, 55))
    img = Image.alpha_composite(img.convert("RGBA"), halo.filter(ImageFilter.GaussianBlur(95))).convert("RGB")
    d = ImageDraw.Draw(img)
    # 底部柔光
    halo2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(halo2).ellipse([-300, H - 380, 360, H + 260], fill=(200, 164, 92, 38))
    img = Image.alpha_composite(img.convert("RGBA"), halo2.filter(ImageFilter.GaussianBlur(95))).convert("RGB")
    d = ImageDraw.Draw(img)

    # 头像（圆形金边）
    av = Image.open(AVATAR).convert("RGB").resize((280, 280))
    mask = Image.new("L", (280, 280), 0); ImageDraw.Draw(mask).ellipse([0, 0, 280, 280], fill=255)
    ring = Image.new("RGBA", (296, 296), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse([0, 0, 296, 296], fill=GOLD + (255,))
    ring.paste(av, (8, 8), mask)
    img.paste(ring, ((W - 296) // 2, 150), ring)
    ay = 150 + 296

    # 姓名 / 头衔
    ctext(d, W // 2, ay + 36, "马树梅", font(72, True), WHITE)
    ctext(d, W // 2, ay + 128, "（梅子）", font(40, True), GOLD)
    ctext(d, W // 2, ay + 196, "传统企业 AI 增长实践者", font(36), GREY)

    # 主题标签
    ctext(d, W // 2, 700, "▍" + theme["tag"], font(34, True), GOLD)

    # 主标题（1~2 行）
    lines = theme["head"]
    hy = 766
    for ln in lines:
        ctext(d, W // 2, hy, ln, font(50, True), WHITE)
        hy += 66
    # 副标题
    sub_y = hy + 18
    ctext(d, W // 2, sub_y, theme["sub"], font(33), GREY)

    # 网站二维码卡片
    qsize = 360
    qy = max(1000, sub_y + 110)
    card_w, card_h = 540, qsize + 196
    cx0 = (W - card_w) // 2
    cy0 = qy - 48
    rrect(d, [cx0, cy0, cx0 + card_w, cy0 + card_h], 28, (255, 255, 255))
    qimg = make_qr(qsize)
    img.paste(qimg, ((W - qsize) // 2, qy))
    ctext(d, W // 2, qy + qsize + 24, "长按识别，进入我的 AI 名片", font(38, True), NAVY)
    ctext(d, W // 2, qy + qsize + 78, theme["cta"], font(30), GREY)

    # 底部署名
    by = cy0 + card_h + 56
    ctext(d, W // 2, by, "微信：yizhimei569", font(30), GOLD_S)
    ctext(d, W // 2, H - 70, "鸿雁归巢 · 马树梅", font(32, True), GOLD)

    img.save(out, "PNG")
    print("saved", out, img.size)

# ============ 6 张推广海报（均来自名片内容）============
THEMES = [
    {
        "out": "posters/01-main.png",
        "tag": "鸿雁归巢 · 个人 AI 名片",
        "head": ["经营自己，也经营企业"],
        "sub": "让值得被看见的人和企业，更容易被看见",
        "cta": "扫一扫，认识真实的我",
    },
    {
        "out": "posters/02-enterprise.png",
        "tag": "企业服务",
        "head": ["企业有好产品，", "却不容易被看见？"],
        "sub": "线上可见性检查 · 帮客户找到你",
        "cta": "扫码了解企业服务",
    },
    {
        "out": "posters/03-ip.png",
        "tag": "老板 IP 与 AI 内容",
        "head": ["想做老板个人 IP，", "却不知从哪开始？"],
        "sub": "定位 · 选题 · AI 工作流 · 复盘",
        "cta": "扫码聊聊你的方向",
    },
    {
        "out": "posters/04-growth.png",
        "tag": "40+ 女性自我成长",
        "head": ["40 岁以后，", "重新认识自己、管理自己"],
        "sub": "晨跑 · 身体管理 · 阅读思考",
        "cta": "扫码看我的生活实践",
    },
    {
        "out": "posters/05-story.png",
        "tag": "创业经历",
        "head": ["2009 创业 → 2026 再出发", "17 年实战，AI 时代探索"],
        "sub": "不讲热点，只从真实问题出发",
        "cta": "扫码听我的真实经历",
    },
    {
        "out": "posters/06-method.png",
        "tag": "我的工作方法",
        "head": ["不讲空话，", "从真实问题开始"],
        "sub": "现状→问题→方案→行动→观察",
        "cta": "扫码看我的工作方法",
    },
]

if __name__ == "__main__":
    os.makedirs("posters", exist_ok=True)
    for t in THEMES:
        build(t, t["out"])
    # 主海报同时输出为 poster.png（对外统一封面）
    build(THEMES[0], "poster.png")
    print("全部生成完成，共", len(THEMES) + 1, "张")
