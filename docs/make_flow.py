# -*- coding: utf-8 -*-
"""生成用户流程图（PNG），用于文档嵌入。"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 760, 900
img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

FONT = "C:/Windows/Fonts/msyh.ttc"
f_num = ImageFont.truetype(FONT, 26)
f_title = ImageFont.truetype(FONT, 26)
f_sub = ImageFont.truetype(FONT, 18)

PINK = (251, 114, 153)
PINK_L = (255, 240, 245)
GREY = (140, 148, 165)
DARK = (40, 44, 54)

steps = [
    ("打开页面", "加载地图与配置"),
    ("请求定位授权", "geolocation · watchPosition"),
    ("计算与展馆的距离", "Haversine 公式"),
    ("围栏判定", "范围内解锁 · 范围外锁定"),
    ("显示蓝点与朝向箭头", "deviceorientation · 旋转矩阵解算"),
    ("点击导航", "调用已有路径规划接口"),
]

box_x, box_w, box_h = 96, 568, 96
gap = 46
top = 34

def rounded(draw, xy, r, fill, outline, width=2):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)

for i, (title, sub) in enumerate(steps):
    y = top + i * (box_h + gap)
    rounded(d, [box_x, y, box_x + box_w, y + box_h], 14, PINK_L, PINK, 2)

    # 序号圆
    cx, cy, r = box_x + 40, y + box_h // 2, 20
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PINK)
    tw = d.textlength(str(i + 1), font=f_num)
    d.text((cx - tw / 2, cy - 17), str(i + 1), font=f_num, fill="white")

    d.text((box_x + 78, y + 20), title, font=f_title, fill=DARK)
    d.text((box_x + 78, y + 56), sub, font=f_sub, fill=GREY)

    # 箭头
    if i < len(steps) - 1:
        ax = box_x + box_w // 2
        y1 = y + box_h + 6
        y2 = y + box_h + gap - 8
        d.line([ax, y1, ax, y2 - 8], fill=(190, 196, 210), width=2)
        d.polygon([(ax - 6, y2 - 10), (ax + 6, y2 - 10), (ax, y2)], fill=(190, 196, 210))


# 画一圈极淡的外框，让图片在任何阅读器里都像一个带框的图
from PIL import ImageDraw as _ID
d.rectangle([0, 0, W - 1, H - 1], outline=(229, 231, 235), width=1)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user-flow.png")
img.save(out, "PNG")
print("saved:", out, img.size)
