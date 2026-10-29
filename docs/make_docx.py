# -*- coding: utf-8 -*-
"""生成《展会地图 Demo 实现思路》Word 文档。"""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "展会地图Demo实现思路.docx")

PINK = "FB7299"
DARK = "2B2F38"
GREY = "6B7280"
LIGHT_GREY = "F3F4F6"
PINK_BG = "FDEDF3"
BORDER = "E2E5EC"

EA = "微软雅黑"
LATIN = "Segoe UI"


def style_run(run, size=10.5, bold=False, color=DARK, east=EA, latin=LATIN):
    run.font.name = latin
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = RGBColor.from_string(color)
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    rFonts.set(qn("w:eastAsia"), east)
    rFonts.set(qn("w:ascii"), latin)
    rFonts.set(qn("w:hAnsi"), latin)


def para(doc, text="", size=10.5, bold=False, color=DARK, before=0, after=6,
         line=1.55, align=None, indent=None):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = line
    if align is not None:
        p.alignment = align
    if indent is not None:
        pf.left_indent = Cm(indent)
    if text:
        style_run(p.add_run(text), size, bold, color)
    return p


def h1(doc, text, num):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(18)
    pf.space_after = Pt(8)
    pf.keep_with_next = True
    style_run(p.add_run(f"{num}  "), 15, True, PINK)
    style_run(p.add_run(text), 15, True, DARK)
    # 下划线分隔
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "4")
    bottom.set(qn("w:color"), BORDER)
    pbdr.append(bottom)
    pPr.append(pbdr)
    return p


def h2(doc, text):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(12)
    pf.space_after = Pt(4)
    pf.keep_with_next = True
    style_run(p.add_run(text), 11.5, True, DARK)
    return p


def bullet(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style="List Bullet")
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(4)
    pf.line_spacing = 1.5
    pf.left_indent = Cm(0.75)
    if bold_prefix:
        style_run(p.add_run(bold_prefix), 10.5, True, DARK)
    style_run(p.add_run(text), 10.5, False, DARK)
    return p


def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)


def cell_text(cell, text, bold=False, color=DARK, size=9.5, align=None):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.35
    if align is not None:
        p.alignment = align
    style_run(p.add_run(text), size, bold, color)


def table_borders(table):
    tbl = table._tbl
    tblPr = tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), BORDER)
        borders.append(el)
    tblPr.append(borders)


def make_table(doc, headers, rows, widths):
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    table_borders(t)
    for i, w in enumerate(widths):
        for row in t.rows:
            row.cells[i].width = Cm(w)
    for i, htext in enumerate(headers):
        c = t.rows[0].cells[i]
        cell_text(c, htext, bold=True, color=DARK)
        shade(c, PINK_BG)
    for r, row_data in enumerate(rows, start=1):
        for i, val in enumerate(row_data):
            cell_text(t.rows[r].cells[i], val)
    return t


# ============================ 文档 ============================
doc = Document()

sec = doc.sections[0]
sec.page_height = Cm(29.7)
sec.page_width = Cm(21.0)
sec.top_margin = Cm(2.2)
sec.bottom_margin = Cm(2.2)
sec.left_margin = Cm(2.4)
sec.right_margin = Cm(2.4)

style = doc.styles["Normal"]
style.font.name = LATIN
style.font.size = Pt(10.5)
style.element.rPr.rFonts.set(qn("w:eastAsia"), EA)

# 标题
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(2)
style_run(p.add_run("展会地图 Demo"), 24, True, DARK)

p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(2)
style_run(p.add_run("实现思路说明"), 24, True, PINK)

p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(20)
style_run(p.add_run("面向产研的技术方案参考　|　2026 年 10 月"), 10, False, GREY)

# ---------- 一 ----------
h1(doc, "概述", "01")
para(doc, "本文说明「展会地图」Demo 的技术实现路径，覆盖定位、围栏解锁、地图渲染、方向指向与导航接入五个环节，"
          "供产研评估可行性，并作为正式方案设计的参考。")
para(doc, "Demo 为纯前端单页应用，零后端、零第三方地图 SDK，可部署在任意静态托管服务上，"
          "手机浏览器直接访问即可使用完整功能。")

# ---------- 二 ----------
h1(doc, "用户流程", "02")
para(doc, "用户从打开页面到发起导航，共经历六步。核心是第 4 步的围栏判定，它决定功能是否解锁。",
     after=10)
doc.add_picture(os.path.join(HERE, "user-flow.png"), width=Cm(8.0))
doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
doc.paragraphs[-1].paragraph_format.space_after = Pt(8)
doc.paragraphs[-1].paragraph_format.keep_with_next = True

# 显式取消图片边框（部分渲染器会给内联图片加默认描边）
try:
    shape = doc.inline_shapes[-1]
    spPr = shape._inline.graphic.graphicData.pic.spPr
    ln = OxmlElement("a:ln")
    ln.append(OxmlElement("a:noFill"))
    spPr.append(ln)
except Exception as e:
    print("border patch skipped:", e)

para(doc, "第 4 步为分支：用户不在围栏内时显示锁定卡片与实时距离；进入范围后自动解锁，"
          "地图放大至当前位置并接入方向指向；离开范围重新锁定。",
     size=9.5, color=GREY, after=4)

# ---------- 三 ----------
h1(doc, "技术实现", "03")

h2(doc, "3.1　定位与生命周期")
para(doc, "使用浏览器原生的 Geolocation API 连续定位，关键在于生命周期管理：", after=4)
bullet(doc, "，开启高精度模式，持续回调位置变化。", "watchPosition　")
bullet(doc, "：页面隐藏时停止监听并清空路线，恢复可见时自动重启。这是「只在 BWS 页面内调用导航」的落点。", "可见性驱动　")
bullet(doc, "：权限拒绝、位置不可用、超时三类错误分别映射为可读的操作提示，而不是暴露浏览器原始报错。", "错误处理　")

h2(doc, "3.2　地图渲染")
para(doc, "未接入第三方地图 SDK，自研了一个约 200 行的迷你瓦片引擎：", after=4)
bullet(doc, "：墨卡托投影把经纬度换算为世界像素坐标，按缩放级别请求 256px 瓦片并拼接。", "投影与瓦片　")
bullet(doc, "：高德瓦片为主，加载失败自动降级 OpenStreetMap。", "瓦片源　")
bullet(doc, "：系统定位返回 WGS84，高德瓦片使用 GCJ-02，两者混用会整体偏移数百米，内置双向转换。", "坐标系转换　")
bullet(doc, "：展会平面图按经纬度包围盒拉伸叠加，路径用 SVG 曲线绘制，均随缩放同步。", "叠加层　")

h2(doc, "3.3　方向指向（重点）")
para(doc, "这是整个项目投入最大、也最容易出问题的部分。浏览器的方向数据原始且不可靠，需要做四层处理。", after=6)

para(doc, "第一层：选择数据源", bold=True, after=3)
para(doc, "按可靠性排序，优先使用系统已融合的绝对方向：", after=4)
bullet(doc, "（系统融合，真北，最可靠）", "iOS · webkitCompassHeading")
bullet(doc, "（绝对 alpha，真北）", "Android · deviceorientationabsolute")
bullet(doc, "（相对 alpha，基准为打开页面时的朝向，界面标注「≈」）", "Android · deviceorientation")
para(doc, "规则：绝对方向一旦出现，立即丢弃所有相对事件——两者交替覆盖会产生固定角度偏差。",
     size=9.5, color=GREY, before=2, after=8)

para(doc, "第二层：解算角度", bold=True, after=3)
para(doc, "不能直接用 alpha 换算（只在手机平放时成立）。改用旋转矩阵，把设备的两根轴转到地理坐标系，"
          "再取水平投影的方位角：", after=4)
para(doc, "R = Rz(alpha) · Rx(beta) · Ry(gamma)", size=10, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, after=4)
para(doc, "平放时顶部轴水平、背面法线垂直；竖起时正好相反。两根轴按「背面法线偏离垂直的程度」做矢量加权融合，"
          "而不是在两者之间硬切换。实测硬切换在倾角临界区（约 45°）两轴方位角最多相差 84°，"
          "手部轻微抖动就会跳变，表现为「指针自转」；改融合后倾角 0→90° 扫描，单步最大跳变 0.25°。",
     after=8)

para(doc, "第三层：稳定性处理", bold=True, after=4)
make_table(doc,
           ["处理", "做法", "解决的问题"],
           [
               ["圆周平滑", "在 (sin, cos) 向量域做指数平滑，不在角度域插值", "抖动、±180° 插值错误"],
               ["跳变保护", "单帧超过 120° 且间隔小于 350ms 的跳变视为毛刺并丢弃", "传感器偶发翻转"],
               ["连续角度", "内部维护不取模的角度值，只把结果交给 CSS", "359°→1° 时 CSS 反向旋转整圈"],
               ["首帧保护", "等待绝对源、丢弃 0/0/0 空值、前 8 帧大跳变重置平滑", "初始方向错误、需移动后才纠正"],
               ["屏幕方向补偿", "减去 screen.orientation.angle", "横屏时整体偏差 90°"],
           ],
           widths=[3.2, 7.6, 5.4])

para(doc, "", after=6)
para(doc, "第四层：手动校准", bold=True, after=3)
para(doc, "设备磁力计基准差异无法靠算法消除，保留手动入口：左右翻转（应对 alpha 方向相反的机型）、"
          "角度偏移（±15° / ±90°），结果存入 localStorage，只影响本机。", after=4)

h2(doc, "3.4　导航接入")
para(doc, "Demo 没有重写导航能力，只提供接入钩子。点击「开始导航」时依次校验三个条件——是否已解锁、"
          "页面是否可见、是否在活动时间窗口内——通过后调用：", after=4)
para(doc, "window.ExpoMap_RoutePlan({ from, to })", size=10, bold=True,
     align=WD_ALIGN_PARAGRAPH.CENTER, after=4)
para(doc, "把已有路径规划返回的折线点串替换占位曲线即可，其余交互（目的地图钉、距离与时间提示）已就绪。",
     after=6)

# ---------- 四 ----------
h1(doc, "关键问题与解法", "04")
para(doc, "以下是开发过程中实际遇到并向产品侧可见的问题，建议直接纳入正式方案的风险项。", after=6)
make_table(doc,
           ["现象", "根因", "解法"],
           [
               ["位置整体偏移数百米", "WGS84 与 GCJ-02 混用", "双向坐标转换"],
               ["方向只在手机平放时准确", "直接使用 alpha 计算", "旋转矩阵 + 倾角补偿"],
               ["固定偏 45°", "绝对与相对事件交替覆盖", "绝对源优先，丢弃相对事件"],
               ["固定偏 180°", "部分机型倾角符号与标准相反", "检测顶部轴朝下时自动翻转"],
               ["绕一圈后指针乱转", "CSS 角度回绕", "内部使用连续角度"],
               ["轻微移动即自转", "两根轴在临界点硬切换", "矢量加权融合"],
               ["打开时方向错、动一下才对", "传感器仅在变化时上报，首帧空值被固化", "等待绝对源 + 丢弃空值 + 重置平滑"],
           ],
           widths=[5.0, 6.4, 4.8])

# ---------- 五 ----------
h1(doc, "上线建议", "05")
para(doc, "一、方向计算下沉到原生", bold=True, after=3)
para(doc, "上述多层处理，本质是在弥补浏览器传感器原始数据的缺陷。若为 App 内嵌 H5，建议原生计算好感向角后传给页面；"
          "独立 App 直接使用 CLHeading（iOS）或 ROTATION_VECTOR（Android），可省去绝大部分兼容性成本。", after=8)

para(doc, "二、室内定位需要另一套方案", bold=True, after=3)
para(doc, "展馆内 GPS 误差可达数十米，无法支撑「走到 A1 馆」级别的指引。可行组合是：场馆平面图（自绘）+ "
          "二维码或蓝牙锚点确认位置 + 路网图寻路。其本质是静态地图上的路径规划，而非实时定位导航。", after=8)

para(doc, "三、正式环境使用成熟地图 SDK", bold=True, after=3)
para(doc, "自研瓦片引擎的优势是零依赖、完全可控，适合原型验证。上线建议接入高德或腾讯 SDK，"
          "室内图、POI 检索、真实路径规划均为现成能力，可显著降低维护成本。", after=8)

# ---------- 六 ----------
h1(doc, "附录：可配置项", "06")
para(doc, "以下参数集中在页面顶部的 CONFIG 对象中，无需改动逻辑即可调整：", after=6)
make_table(doc,
           ["配置项", "说明"],
           [
               ["venues", "场地列表：名称、经纬度、解锁半径（正式场地 / 演示场地可切换）"],
               ["activeVenue", "默认使用的场地"],
               ["window", "活动起止时间，超出后地图整体不可用"],
               ["overlayUrl", "展会平面图地址，留空则使用内置示例图"],
               ["overlaySpanMeters", "平面图覆盖的边长（米），用于与实际场馆对齐"],
               ["lockShowsSelf", "未解锁时是否显示灰色自身点位（调试用）"],
           ],
           widths=[4.4, 11.8])

para(doc, "", after=10)
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(12)
style_run(p.add_run("Demo 地址："), 9, False, GREY)
style_run(p.add_run("https://mreswn.github.io/expo-map-demo/"), 9, False, "2F7BFF")


# ---------- 页脚页码 ----------
def add_field(run, code):
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = code
    fld_sep = OxmlElement("w:fldChar")
    fld_sep.set(qn("w:fldCharType"), "separate")
    txt = OxmlElement("w:t")
    txt.text = "1"
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    for el in (fld_begin, instr, fld_sep, txt, fld_end):
        run._r.append(el)


fp = doc.sections[0].footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
style_run(fp.add_run("展会地图 Demo · 实现思路说明　　"), 8, False, GREY)
r1 = fp.add_run(); style_run(r1, 8, False, GREY); add_field(r1, " PAGE ")
style_run(fp.add_run(" / "), 8, False, GREY)
r2 = fp.add_run(); style_run(r2, 8, False, GREY); add_field(r2, " NUMPAGES ")

doc.save(OUT)
print("saved:", OUT)
print("paragraphs:", len(doc.paragraphs), "tables:", len(doc.tables))
