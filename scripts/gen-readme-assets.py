#!/usr/bin/env python3
"""README visuals for dsh-qms-capa, derived from the plugin's own material.

Two figures, both read off the shipped source / samples rather than a template:

  hero 1440x576 — 4 files (zh/en x light/dark, WebP, Pillow)
      Left column: kicker, plugin name, two value lines, two subtitle lines,
      meta, footer. Right: one NCR event as an *impact field*. The five-field
      dedupe key is a token chain (P1 / M-1001 / L-1001 / D-101 / 2026-03-01)
      with the duplicate branch beside it, then the two snapshot lanes (stock,
      intransit) merge into one verdict plate (affected 2 / recall_hint true /
      evidence_sha256), and the two records opened from that NCR sit below
      (CAPA A opened, 8D at d1 with 8 disciplines missing).

  flow 1100x660 — 2 files (light/dark, hand-written SVG)
      Grammar: **spine + fork -> dual-lane confluence -> two state rails ->
      read-only read-back**. It is deliberately not a five-node chain:
        * a vertical ingest spine (ncrs.csv -> qms.ncr -> qms.batch_alias ->
          canonical_lot LOT-A) with a fork that splits 12 new rows from 3
          duplicates, the duplicate branch ending at "existing id, no upsert";
        * the canonical lot is scanned in two snapshot lanes (stock / intransit)
          that converge into one verdict plate, with the missing-snapshot
          boundary drawn as a dashed gate (E_QMS_IMPACT_INCOMPLETE);
        * two horizontal state rails (CAPA opened..closed, 8D d1..d8..closed)
          drawn as tick track + state labels, each carrying its gate note
          (grade-based due dates, E_QMS_STEP_ILLEGAL on an empty discipline);
        * two read-only review cards (qms.8d_check, qms.capa_effectiveness)
          below the rails, fed by short dashed read arrows -- they read state,
          they write nothing;
        * a storage strip and a boundary card fix the only write target and the
          "no network / no model / input untouched" boundary.

Values are not invented:
  samples/quickstart/expected/result.json      15 rows, 12 new, 3 dup,
      alias L-1001 -> LOT-A, affected 2, recall_hint true, CAPA A opened with
      blocker state_not_verified, 8D at d1 with 8 missing disciplines.
  samples/quickstart/input/snapshots.json      stock = LOT-A, L-2002, L-3003;
      intransit = LOT-A.
  src/plugin/tools.ts                          dedupeKey/5-field validation,
      canonical -> affected filter, recall_hint = intransit hit, grade due days
      A=7/B=14/C=30, CAPA & 8D state chains, E_QMS_IMPACT_INCOMPLETE,
      E_QMS_STEP_ILLEGAL on an empty current discipline, thin < 10 chars.
  src/core/qms.ts                              the five required fields.
The short hash bea8c688… shown on the hero is sha256 of the exact payload the
tool hashes: {"stock":["LOT-A","L-2002","L-3003"],"intransit":["LOT-A"]}.

The previous single-skin `dsh-qms-capa-flow.svg` and the first `flow-{light,
dark}.svg` pair are left on disk untouched so old external links keep working;
this script only rewrites the hero set and the flow-v5 pair.

Run:      python scripts/gen-readme-assets.py
Requires: Pillow + Windows fonts msyh.ttc / msyhbd.ttc / consola.ttf.
Chrome is only used for the visual self-check, not by this script.
"""
from __future__ import annotations

import os
from html import escape

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "assets")

FONT_CJK = r"C:\Windows\Fonts\msyh.ttc"
FONT_CJK_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_MONO = r"C:\Windows\Fonts\consola.ttf"
FONT_MONO_BOLD = r"C:\Windows\Fonts\consolab.ttf"
for _p in (FONT_CJK, FONT_CJK_BOLD, FONT_MONO, FONT_MONO_BOLD):
    if not os.path.exists(_p):
        raise SystemExit(f"FATAL: font missing: {_p}")

FONT_FILES = {"cjk": FONT_CJK, "cjk_bold": FONT_CJK_BOLD,
              "mono": FONT_MONO, "mono_bold": FONT_MONO_BOLD}

NAME = "dsh-qms-capa"

# --------------------------------------------------------------------- palette
SKIN = {
    "light": dict(
        bg_from="#f9f6fd", bg_to="#e4eaf8",
        card="#ffffff", edge="#e6e2ef",
        text="#141419", sub="#4d5261", faint="#8f94a4",
        accent="#4B67B4", green="#16a34a",
        pill="#ece7f9", band="#f5f2fb", rule="#e3dfee",
        hit="#eef1fb", mark="#b45309", mark_bg="#fdf3e9", mark_edge="#ecd3b6",
        shadow=(38, 29, 74), shadow_hex="#3a2c66", glow="#7a68c9",
        shadow_op="0.10",
    ),
    "dark": dict(
        bg_from="#131a2a", bg_to="#0c1016",
        card="#1b2231", edge="#2e374b",
        text="#f0f3f9", sub="#a8b1c4", faint="#737b8d",
        accent="#8496f5", green="#3fb950",
        pill="#242d42", band="#202839", rule="#2a3346",
        hit="#1d2740", mark="#d9a441", mark_bg="#2a2216", mark_edge="#5c4a24",
        shadow=(0, 0, 0), shadow_hex="#000000", glow="#8496f5",
        shadow_op="0.45",
    ),
}


def hx(s):
    if isinstance(s, tuple):
        return s
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def font(size: float, kind: str = "cjk_bold") -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_FILES[kind], int(round(size)))


def gradient(w: int, h: int, c1: str, c2: str) -> Image.Image:
    base = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(base)
    a, b = hx(c1), hx(c2)
    for y in range(h):
        t = 0.12 * (y / h) + 0.88 * (y / h) ** 1.3
        d.line([(0, y), (w, y)],
               fill=tuple(int(p + (q - p) * t) for p, q in zip(a, b)))
    return base


def glow(img: Image.Image, cx: int, cy: int, r: int, color: str,
         alpha: int = 34) -> Image.Image:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    c = hx(color)
    for i in range(10, 0, -1):
        rr = r * i / 10
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                  fill=c + (int(alpha * (1 - i / 11)),))
    layer = layer.filter(ImageFilter.GaussianBlur(26))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def card(img: Image.Image, box, s: dict, radius: int = 22,
         shadow: int = 24) -> Image.Image:
    x0, y0, x1, y1 = box
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    for i in range(shadow, 0, -2):
        sd.rounded_rectangle([x0 - i // 6, y0 + i // 2, x1 + i // 6, y1 + i],
                             radius=radius + i // 4,
                             fill=hx(s["shadow"]) + (int(8 * (1 - i / shadow)),))
    base = Image.alpha_composite(img.convert("RGBA"),
                                 sh.filter(ImageFilter.GaussianBlur(12)))
    d = ImageDraw.Draw(base)
    d.rounded_rectangle(box, radius=radius, fill=hx(s["card"]),
                        outline=hx(s["edge"]), width=2)
    return base.convert("RGB")


_SCRATCH = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def measure(text: str, size: float, kind: str) -> float:
    return _SCRATCH.textlength(text, font=font(size, kind))


def require_w(text: str, size: float, kind: str, max_w: float, what: str) -> None:
    w = measure(text, size, kind)
    if w > max_w + 0.4:
        raise SystemExit(
            f"FATAL: {what} overflows: {text!r} needs {w:.1f}px > {max_w}px")


def pill(img: Image.Image, xy, text: str, s: dict, size: float = 16,
         fg: str | None = None, bg: str | None = None,
         kind: str = "cjk_bold") -> tuple[int, int]:
    d = ImageDraw.Draw(img)
    f = font(size, kind)
    w = d.textlength(text, font=f)
    x, y = xy
    h = int(size + 20)
    d.rounded_rectangle([x, y, x + w + 30, y + h], radius=h // 2,
                        fill=hx(bg or s["pill"]))
    d.text((x + 15, y + h / 2), text, font=f, fill=hx(fg or s["accent"]),
           anchor="lm")
    return int(x + w + 30), int(y + h)


def chip(img: Image.Image, xy, text: str, s: dict, *, size: float = 11.5,
         kind: str = "cjk_bold", fg: str | None = None, bg: str | None = None,
         padx: int = 9, height: int = 20,
         outline: str | None = None) -> float:
    d = ImageDraw.Draw(img)
    f = font(size, kind)
    w = d.textlength(text, font=f)
    x, y = xy
    d.rounded_rectangle([x, y, x + w + padx * 2, y + height],
                        radius=height / 2, fill=hx(bg or s["band"]),
                        outline=hx(outline) if outline else None,
                        width=1 if outline else 0)
    d.text((x + padx, y + height / 2), text, font=f, fill=hx(fg or s["faint"]),
           anchor="lm")
    return w + padx * 2


def dot(img: Image.Image, cx: float, cy: float, r: float, color: str,
        filled: bool = True, width: int = 2) -> None:
    d = ImageDraw.Draw(img)
    if filled:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=hx(color))
    else:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=hx(color),
                  width=width)


def lane_chip(img: Image.Image, x: float, cy: float, text: str, s: dict,
              hit: bool) -> float:
    d = ImageDraw.Draw(img)
    f = font(13, "mono_bold")
    tw = d.textlength(text, font=f)
    w = 30 + tw + 12
    d.rounded_rectangle([x, cy - 13, x + w, cy + 13], radius=13,
                        fill=hx(s["hit"] if hit else s["band"]),
                        outline=hx(s["accent"] if hit else s["edge"]),
                        width=2 if hit else 1)
    dot(img, x + 13, cy, 3.6, s["accent"] if hit else s["faint"], filled=hit)
    d.text((x + 24, cy), text, font=f,
           fill=hx(s["accent"] if hit else s["sub"]), anchor="lm")
    return w


# =========================================================================== hero
HERO = {
    "zh": dict(
        kicker="DeepSeek Harness 插件 · 本地质量事件",
        value1="NCR 去重入库，批号沿别名归并",
        value2="库存与途中一次查清，再开 CAPA / 8D",
        sub1="输入固定八列 CSV 与库存/途中快照；五字段去重。",
        sub2="全程本地：七个工具只写 qms 域，不联网、不调模型。",
        meta="15 行 → 12 新增 / 3 重复 · L-1001 → LOT-A · 命中 2 · CAPA A · 8D d1",
        foot="Apache-2.0 · PerryLink DSH plugin family · 本地 · 无网络",
        card_title="一次 NCR 事件的影响面",
        card_chip="合成样例 · 非真实工厂数据",
        key_label="五字段去重键",
        tokens=["P1", "M-1001", "L-1001", "D-101", "2026-03-01"],
        dup_chip="dup ×3 · 返回已有编号",
        lanes_label="影响面：库存 / 途中 两份快照",
        impact_chip="qms.impact · R0",
        lane_stock="stock",
        lane_intransit="intransit",
        stock=["LOT-A", "L-2002", "L-3003"],
        intransit=["LOT-A"],
        verdict=("affected 2", "recall_hint true", "evidence_sha256",
                 "bea8c688…"),
        capa_title="CAPA",
        capa_chips=("A", "opened"),
        capa_lines=["due A+7 · B+14 · C+30 d", "blocker state_not_verified",
                    "review qms.capa_effectiveness"],
        eightd_title="8D",
        eightd_chips=("d1",),
        eightd_lines=["missing 8 · thin 0", "d1 has no evidence yet",
                      "advance → E_QMS_STEP_ILLEGAL"],
        caption="样例取自 samples/quickstart · 非真实工厂数据",
    ),
    "en": dict(
        kicker="DeepSeek Harness plugin · local quality events",
        value1="Dedupe NCRs, resolve lots by alias",
        value2="Scan stock + intransit, then CAPA / 8D",
        sub1="Fixed eight-column CSV plus stock/intransit snapshots.",
        sub2="Fully local: seven qms.* tools, one storage domain, no network.",
        meta="15 rows → 12 new / 3 dup · L-1001 → LOT-A · 2 hits · CAPA A · 8D d1",
        foot="Apache-2.0 · PerryLink DSH plugin family · local · no network",
        card_title="Impact field for one NCR",
        card_chip="synthetic sample · not plant data",
        key_label="five-field dedupe key",
        tokens=["P1", "M-1001", "L-1001", "D-101", "2026-03-01"],
        dup_chip="dup ×3 · existing id",
        lanes_label="impact: stock / intransit snapshots",
        impact_chip="qms.impact · R0",
        lane_stock="stock",
        lane_intransit="intransit",
        stock=["LOT-A", "L-2002", "L-3003"],
        intransit=["LOT-A"],
        verdict=("affected 2", "recall_hint true", "evidence_sha256",
                 "bea8c688…"),
        capa_title="CAPA",
        capa_chips=("A", "opened"),
        capa_lines=["due A+7 · B+14 · C+30 d", "blocker state_not_verified",
                    "review qms.capa_effectiveness"],
        eightd_title="8D",
        eightd_chips=("d1",),
        eightd_lines=["missing 8 · thin 0", "d1 evidence empty",
                      "advance → E_QMS_STEP_ILLEGAL"],
        caption="sample from samples/quickstart · not real plant data",
    ),
}


def hero(lang: str, skin: str) -> str:
    s = SKIN[skin]
    t = HERO[lang]
    W, H = 1440, 576
    img = gradient(W, H, s["bg_from"], s["bg_to"])
    img = glow(img, 1210, 54, 420, s["glow"], 30 if skin == "light" else 22)
    img = glow(img, 150, 560, 380, s["glow"], 22 if skin == "light" else 16)

    # ---- left column ------------------------------------------------------
    require_w(t["kicker"], 16, "cjk_bold", 430, "kicker")
    pill(img, (88, 74), t["kicker"], s, size=16)
    require_w(NAME, 64, "mono_bold", 600, "title")
    ImageDraw.Draw(img).text((88, 178), NAME, font=font(64, "mono_bold"),
                             fill=hx(s["text"]), anchor="ls")
    for i, line in enumerate((t["value1"], t["value2"])):
        require_w(line, 30, "cjk_bold", 616, "value line")
        ImageDraw.Draw(img).text((88, 252 + i * 46), line,
                                 font=font(30, "cjk_bold"), fill=hx(s["text"]),
                                 anchor="ls")
    for i, line in enumerate((t["sub1"], t["sub2"])):
        require_w(line, 18, "cjk", 618, "subtitle")
        ImageDraw.Draw(img).text((88, 350 + i * 28), line, font=font(18),
                                 fill=hx(s["sub"]), anchor="ls")
    require_w(t["meta"], 16, "cjk", 618, "meta")
    ImageDraw.Draw(img).text((88, 442), t["meta"], font=font(16),
                             fill=hx(s["faint"]), anchor="ls")
    require_w(t["foot"], 14.5, "cjk", 600, "footer")
    ImageDraw.Draw(img).text((88, 514), t["foot"], font=font(14.5),
                             fill=hx(s["faint"]), anchor="ls")

    # ---- impact-field card ------------------------------------------------
    x0, x1, top = 748, 1336, 56
    img = card(img, (716, 56, 1368, 520), s, radius=22)
    d = ImageDraw.Draw(img)
    require_w(t["card_title"], 17, "cjk_bold", 380, "card title")
    d.text((x0, 98), t["card_title"], font=font(17, "cjk_bold"),
           fill=hx(s["text"]), anchor="ls")
    cw = measure(t["card_chip"], 11.5, "cjk") + 18
    chip(img, (x1 - cw, 80), t["card_chip"], s, size=11.5)
    d.line([(x0, 116), (x1, 116)], fill=hx(s["rule"]), width=1)

    # five-field key chain + duplicate branch
    require_w(t["key_label"], 11.5, "cjk", 330, "key label")
    d.text((x0, 140), t["key_label"], font=font(11.5), fill=hx(s["faint"]),
           anchor="ls")
    dcw = measure(t["dup_chip"], 11.5, "cjk") + 18
    chip(img, (x1 - dcw, 126), t["dup_chip"], s, size=11.5, fg=s["mark"],
         bg=s["mark_bg"], outline=s["mark_edge"])
    tx = x0
    for i, token in enumerate(t["tokens"]):
        require_w(token, 13, "mono_bold", 200, "key token")
        tw = measure(token, 13, "mono_bold") + 20
        d.rounded_rectangle([tx, 152, tx + tw, 182], radius=9,
                            fill=hx(s["band"]), outline=hx(s["edge"]),
                            width=1)
        d.text((tx + tw / 2, 167), token, font=font(13, "mono_bold"),
               fill=hx(s["accent"]), anchor="mm")
        tx += tw
        if i < len(t["tokens"]) - 1:
            d.line([(tx + 8, 159), (tx + 8, 175)], fill=hx(s["edge"]), width=1)
            tx += 16

    # two snapshot lanes -> one verdict plate
    require_w(t["lanes_label"], 12.5, "cjk", 300, "lanes label")
    d.text((x0, 210), t["lanes_label"], font=font(12.5), fill=hx(s["sub"]),
           anchor="ls")
    icw = measure(t["impact_chip"], 11, "mono_bold") + 18
    chip(img, (x1 - icw, 196), t["impact_chip"], s, size=11,
         kind="mono_bold", fg=s["accent"], bg=s["band"], outline=s["edge"])

    lane_x = 828
    lane1, lane2 = 244, 292
    cx = lane_x
    for lot in t["stock"]:
        w = lane_chip(img, cx, lane1, lot, s, hit=(lot == "LOT-A"))
        cx += w + 10
    lane_end = cx - 10
    lane_chip(img, lane_x, lane2, t["intransit"][0], s, hit=True)
    d.text((lane_x - 12, lane1), t["lane_stock"], font=font(12.5, "mono"),
           fill=hx(s["faint"]), anchor="rm")
    d.text((lane_x - 12, lane2), t["lane_intransit"], font=font(12.5, "mono"),
           fill=hx(s["faint"]), anchor="rm")

    merge_x = lane_end + 18
    d.line([(merge_x, lane1), (merge_x, lane2)], fill=hx(s["edge"]), width=2)
    d.line([(merge_x, (lane1 + lane2) / 2), (merge_x + 20, (lane1 + lane2) / 2)],
           fill=hx(s["sub"]), width=2)
    d.polygon([(merge_x + 20, (lane1 + lane2) / 2 - 5),
               (merge_x + 30, (lane1 + lane2) / 2),
               (merge_x + 20, (lane1 + lane2) / 2 + 5)], fill=hx(s["sub"]))

    vx = merge_x + 42
    vw = x1 - vx
    d.rounded_rectangle([vx, 218, x1, 342], radius=16, fill=hx(s["band"]),
                        outline=hx(s["edge"]), width=1)
    require_w(t["verdict"][0], 20, "mono_bold", vw - 36, "affected count")
    d.text((vx + 18, 268), t["verdict"][0], font=font(20, "mono_bold"),
           fill=hx(s["text"]), anchor="ls")
    require_w(t["verdict"][1], 13, "mono_bold", vw - 36, "recall hint")
    d.text((vx + 18, 294), t["verdict"][1], font=font(13, "mono_bold"),
           fill=hx(s["green"]), anchor="ls")
    require_w(t["verdict"][2], 11, "mono", vw - 36, "sha label")
    d.text((vx + 18, 318), t["verdict"][2], font=font(11, "mono"),
           fill=hx(s["faint"]), anchor="ls")
    require_w(t["verdict"][3], 11, "mono_bold", vw - 36, "sha prefix")
    d.text((vx + 18, 336), t["verdict"][3], font=font(11, "mono_bold"),
           fill=hx(s["faint"]), anchor="ls")

    # the two records opened from this NCR
    d.line([(x0, 350), (x1, 350)], fill=hx(s["rule"]), width=1)
    plates = [(x0, 1038, t["capa_title"], t["capa_chips"], t["capa_lines"]),
              (1048, x1, t["eightd_title"], t["eightd_chips"], t["eightd_lines"])]
    for px0, px1, title, chips, lines in plates:
        d.rounded_rectangle([px0, 362, px1, 474], radius=16, fill=hx(s["band"]),
                            outline=hx(s["edge"]), width=1)
        d.text((px0 + 18, 388), title, font=font(13.5, "cjk_bold"),
               fill=hx(s["text"]), anchor="ls")
        cx = px0 + 18 + measure(title, 13.5, "cjk_bold") + 10
        for c in chips:
            w = measure(c, 11, "mono_bold") + 16
            if cx + w > px1 - 16:
                raise SystemExit(f"FATAL: hero record chip overflows: {c!r}")
            d.rounded_rectangle([cx, 376, cx + w, 394], radius=9,
                                fill=hx(s["card"]), outline=hx(s["edge"]),
                                width=1)
            d.text((cx + w / 2, 386), c, font=font(11, "mono_bold"),
                   fill=hx(s["accent"]), anchor="mm")
            cx += w + 6
        for i, line in enumerate(lines):
            require_w(line, 11.5, "mono", px1 - px0 - 36, "record line")
            d.text((px0 + 18, 416 + i * 22), line, font=font(11.5, "mono"),
                   fill=hx(s["sub"]), anchor="ls")
    require_w(t["caption"], 11.5, "cjk", 560, "caption")
    d.text((x0, 502), t["caption"], font=font(11.5), fill=hx(s["faint"]),
           anchor="ls")

    name = f"{NAME}-hero-{lang}-{skin}.webp"
    assert img.size == (W, H), img.size
    img.save(os.path.join(OUT, name), "WEBP", quality=92, method=6)
    return name


# ======================================================================= SVG kit
MONO_FAMILY = "'Consolas','SFMono-Regular','Menlo',ui-monospace,monospace"


class Svg:
    def __init__(self, s: dict):
        self.s = s
        self.parts: list[str] = []
        self.overflows: list[str] = []

    def add(self, text: str) -> None:
        self.parts.append(text)

    def _check(self, text: str, size: float, mono: bool, bold: bool,
               max_w: float | None) -> float:
        kind = ("mono_bold" if bold else "mono") if mono else (
            "cjk_bold" if bold else "cjk")
        w = measure(text, size, kind)
        if max_w is not None and w > max_w + 0.8:
            self.overflows.append(f"{text!r} {w:.1f} > {max_w:.0f}")
        return w

    def text(self, x: float, y: float, text: str, size: float, color: str,
             *, mono: bool = True, bold: bool = False, anchor: str = "start",
             max_w: float | None = None, spacing: float | None = None) -> float:
        w = self._check(text, size, mono, bold, max_w)
        attrs = [f'x="{x:g}"', f'y="{y:g}"', f'fill="{color}"',
                 f'font-family="{MONO_FAMILY}"', f'font-size="{size:g}"']
        if bold:
            attrs.append('font-weight="700"')
        if anchor != "start":
            attrs.append(f'text-anchor="{anchor}"')
        if spacing is not None:
            attrs.append(f'letter-spacing="{spacing:g}"')
        self.add(f'<text {" ".join(attrs)}>{escape(text)}</text>')
        return w

    def rect(self, x: float, y: float, w: float, h: float, *, fill: str,
             rx: float = 0, stroke: str | None = None, sw: float = 1,
             dash: str | None = None, shadow: bool = False) -> None:
        attrs = [f'x="{x:g}"', f'y="{y:g}"', f'width="{w:g}"', f'height="{h:g}"',
                 f'rx="{rx:g}"', f'fill="{fill}"']
        if stroke is not None:
            attrs.append(f'stroke="{stroke}" stroke-width="{sw:g}"')
        if dash is not None:
            attrs.append(f'stroke-dasharray="{dash}"')
        if shadow:
            attrs.append('filter="url(#soft)"')
        self.add(f'<rect {" ".join(attrs)}/>')

    def line(self, x1: float, y1: float, x2: float, y2: float, *, stroke: str,
             sw: float = 1, dash: str | None = None) -> None:
        attrs = [f'x1="{x1:g}"', f'y1="{y1:g}"', f'x2="{x2:g}"', f'y2="{y2:g}"',
                 f'stroke="{stroke}" stroke-width="{sw:g}"',
                 'stroke-linecap="round"']
        if dash is not None:
            attrs.append(f'stroke-dasharray="{dash}"')
        self.add(f'<line {" ".join(attrs)}/>')

    def path(self, dd: str, *, stroke: str | None = None, fill: str = "none",
             sw: float = 1, dash: str | None = None,
             marker: str | None = None) -> None:
        attrs = [f'd="{dd}"', f'fill="{fill}"']
        if stroke is not None:
            attrs.append(f'stroke="{stroke}" stroke-width="{sw:g}"')
            attrs.append('stroke-linecap="round" stroke-linejoin="round"')
        if dash is not None:
            attrs.append(f'stroke-dasharray="{dash}"')
        if marker is not None:
            attrs.append(f'marker-end="url(#{marker})"')
        self.add(f'<path {" ".join(attrs)}/>')

    def circle(self, cx: float, cy: float, r: float, *, fill: str = "none",
               stroke: str | None = None, sw: float = 1) -> None:
        attrs = [f'cx="{cx:g}"', f'cy="{cy:g}"', f'r="{r:g}"', f'fill="{fill}"']
        if stroke is not None:
            attrs.append(f'stroke="{stroke}" stroke-width="{sw:g}"')
        self.add(f'<circle {" ".join(attrs)}/>')

    def chip(self, x: float, y: float, text: str, *, fg: str, bg: str,
             size: float = 12, mono: bool = True, h: float = 20,
             pad: float = 8, bold: bool = True, stroke: str | None = None,
             rx: float | None = None) -> float:
        w = self._check(text, size, mono, bold, None) + pad * 2
        r = h / 2 if rx is None else rx
        self.rect(x, y, w, h, fill=bg, rx=r, stroke=stroke, sw=1)
        self.text(x + pad, y + h / 2 + size * 0.36, text, size, fg, mono=mono,
                  bold=bold)
        return w

    def svg(self, w: int, h: int, aria: str, defs: str) -> str:
        head = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" '
                f'height="{h}" viewBox="0 0 {w} {h}" role="img" '
                f'aria-label="{escape(aria)}">',
                f'<title>{escape(aria)}</title>', defs]
        return "\n".join(head + self.parts + ["</svg>"]) + "\n"


# ====================================================================== flow v5
FLOW_W, FLOW_H = 1100, 660
CAPA_STATES = ["opened", "contained", "root_cause", "corrective", "verified",
               "closed"]
EIGHTD_STATES = ["d1", "d2", "d3", "d4", "d5", "d6", "d7", "d8", "closed"]


def flow(skin: str) -> str:
    s = SKIN[skin]
    g = Svg(s)
    bg, card_c, edge, text, sub, faint = (s["bg_from"], s["card"], s["edge"],
                                         s["text"], s["sub"], s["faint"])
    accent, band, rule, green, mark = (s["accent"], s["band"], s["rule"],
                                       s["green"], s["mark"])
    defs = (
        f'<defs>\n'
        f'  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="{FLOW_H}" '
        f'gradientUnits="userSpaceOnUse">\n'
        f'    <stop offset="0" stop-color="{s["bg_from"]}"/>\n'
        f'    <stop offset="1" stop-color="{s["bg_to"]}"/>\n'
        f'  </linearGradient>\n'
        f'  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%">\n'
        f'    <feDropShadow dx="0" dy="5" stdDeviation="9" '
        f'flood-color="{s["shadow_hex"]}" flood-opacity="{s["shadow_op"]}"/>\n'
        f'  </filter>\n'
        f'  <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="7" markerHeight="7" orient="auto">'
        f'<path d="M0 0 L10 5 L0 10 z" fill="{sub}"/></marker>\n'
        f'  <marker id="arrA" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="7" markerHeight="7" orient="auto">'
        f'<path d="M0 0 L10 5 L0 10 z" fill="{accent}"/></marker>\n'
        f'  <marker id="arrF" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="6" markerHeight="6" orient="auto">'
        f'<path d="M0 0 L10 5 L0 10 z" fill="{faint}"/></marker>\n'
        f'</defs>\n'
        f'<rect width="{FLOW_W}" height="{FLOW_H}" fill="url(#bg)"/>'
    )

    # ---- header -----------------------------------------------------------
    g.text(44, 44, NAME, 24, text, bold=True)
    g.text(44, 64, "quality-event spine · ingest → impact → two state rails "
                   "→ read-only review", 12, sub, max_w=760)
    g.text(1056, 40, "storage domain qms v1 · 4 tables", 12, sub, anchor="end")
    g.text(1056, 62, "R1 local write · R0 read-only", 11.5, faint, anchor="end")
    g.line(44, 76, 1056, 76, stroke=rule, sw=1)

    # ======================= left spine: ingest + fork + alias ==============
    sx, sw_ = 44, 224
    g.rect(sx, 88, sw_, 116, fill=card_c, rx=14, stroke=edge, sw=1, shadow=True)
    g.text(62, 116, "ncrs.csv", 13, text, bold=True)
    s1_chip = "8 cols · 15 rows"
    cw = measure(s1_chip, 11, "mono_bold") + 16
    g.chip(250 - cw, 98, s1_chip, fg=faint, bg=band, size=11)
    g.text(62, 142, "plant · material · lot", 11, text, max_w=188)
    g.text(62, 158, "defect_code · found_date", 11, text, max_w=188)
    g.text(62, 174, "quantity · source", 11, faint, max_w=188)
    g.text(62, 190, "recurrence_of", 11, faint, max_w=188)
    g.path("M156 204 v10", stroke=sub, sw=1.6, marker="arr")

    g.rect(sx, 218, sw_, 112, fill=card_c, rx=14, stroke=edge, sw=1, shadow=True)
    g.text(62, 242, "qms.ncr", 13, text, bold=True)
    g.chip(221, 228, "R1", fg=accent, bg=band, size=11)
    g.text(62, 262, "key: 5 fields, all non-empty", 11, faint, max_w=188)
    g.circle(68, 282, 3.6, fill=accent)
    g.text(80, 286, "12 new", 13, accent, bold=True)
    g.text(250, 286, "→ ncrs", 11, faint, anchor="end")
    g.circle(68, 306, 3.6, fill=mark)
    g.text(80, 310, "3 dup", 13, mark, bold=True)
    g.text(250, 310, "→ existing id", 11, faint, anchor="end")
    g.text(62, 326, "no upsert · quantity kept", 11, sub, max_w=188)
    g.path("M96 330 v10", stroke=sub, sw=1.6, marker="arr")

    g.rect(sx, 342, sw_, 92, fill=card_c, rx=14, stroke=edge, sw=1, shadow=True)
    g.text(62, 366, "qms.batch_alias", 13, text, bold=True)
    g.chip(221, 352, "R1", fg=accent, bg=band, size=11)
    g.chip(62, 374, "L-1001", fg=sub, bg=band, size=13, h=26, stroke=edge)
    g.path("M128 387 h20", stroke=sub, sw=1.6, marker="arr")
    g.chip(156, 374, "LOT-A", fg=accent, bg=s["hit"], size=13, h=26,
           stroke=accent)
    g.text(62, 414, "set: canonical required", 11, faint, max_w=188)
    g.text(62, 428, "miss: returns the alias", 11, faint, max_w=188)
    g.path("M156 434 v8", stroke=sub, sw=1.6, marker="arr")

    g.rect(sx, 446, sw_, 44, fill=accent, rx=12)
    g.text(64, 474, "LOT-A", 16, card_c, bold=True)
    g.text(250, 474, "canonical_lot", 11, card_c, anchor="end")

    # canonical lot -> impact plate
    g.path("M268 468 h20 V190 h129", stroke=accent, sw=1.6, marker="arrA")

    # ======================= plate A: dual-lane confluence ==================
    ax0, ax1, ay0, ay1 = 312, 1056, 88, 296
    g.rect(ax0, ay0, ax1 - ax0, ay1 - ay0, fill=card_c, rx=16, stroke=edge,
           sw=1, shadow=True)
    g.text(332, 116, "qms.impact", 14, text, bold=True)
    g.chip(424, 102, "R0", fg=sub, bg=band, size=11)
    g.text(332, 136, "both snapshot lists are scanned for the canonical lot",
           11.5, sub, max_w=740)

    fork_x, lane_a, lane_b = 420, 176, 218
    g.path(f"M{fork_x} {lane_a} V{lane_b}", stroke=edge, sw=2)
    g.line(fork_x, lane_a, 826, lane_a, stroke=edge, sw=1.6)
    g.line(fork_x, lane_b, 826, lane_b, stroke=edge, sw=1.6)

    g.text(332, 181, "stock", 13, text, bold=True)
    cx = 440
    for lot in ("LOT-A", "L-2002", "L-3003"):
        w = g.chip(cx, lane_a - 13, lot, fg=accent if lot == "LOT-A" else sub,
                   bg=s["hit"] if lot == "LOT-A" else band, size=13, h=26,
                   stroke=accent if lot == "LOT-A" else edge)
        cx += w + 8
    g.text(332, 223, "intransit", 13, text, bold=True)
    g.chip(440, lane_b - 13, "LOT-A", fg=accent, bg=s["hit"], size=13, h=26,
           stroke=accent)
    g.text(524, 222, "(an intransit hit sets recall_hint)", 11, faint,
           max_w=300)

    g.line(826, lane_a, 826, lane_b, stroke=sub, sw=1.6)
    g.circle(826, (lane_a + lane_b) / 2, 3.4, fill=sub)
    g.path(f"M828 {(lane_a + lane_b) / 2} h16", stroke=sub, sw=1.6,
           marker="arr")

    g.rect(852, 150, 184, 116, fill=band, rx=14, stroke=edge, sw=1)
    g.text(870, 184, "affected 2", 18, text, bold=True, max_w=150)
    g.text(870, 210, "recall_hint true", 13, green, bold=True, max_w=150)
    g.text(870, 234, "evidence_sha256", 11, faint, max_w=150)
    g.text(870, 252, "sha256(stock + intransit)", 11, faint, max_w=160)

    g.rect(332, 262, 276, 26, fill="none", rx=8, stroke=mark, sw=1.2,
           dash="4 4")
    g.text(344, 279, "snapshot missing → E_QMS_IMPACT_INCOMPLETE", 11, mark,
           max_w=276)

    # impact verdict -> the two state rails
    g.path("M700 296 v10", stroke=sub, sw=1.6, marker="arr")
    g.text(712, 309, "impact verdict → open a CAPA or an 8D", 11, sub,
           max_w=330)

    # ======================= plate B: two state rails ======================
    bx0, bx1, by0, by1 = 312, 1056, 320, 492
    g.rect(bx0, by0, bx1 - bx0, by1 - by0, fill=card_c, rx=16, stroke=edge,
           sw=1, shadow=True)
    g.text(332, 348, "two state rails", 14, text, bold=True)
    g.text(470, 348, "advance one state, never skip", 11.5, sub, max_w=250)
    cw1 = g.chip(740, 334, "qms.capa · R1", fg=accent, bg=band, size=12)
    g.chip(740 + cw1 + 8, 334, "qms.8d · R1", fg=accent, bg=band, size=12)

    def rail(y: float, label: str, states: list[str], track_x0: float,
             track_x1: float, reached: int, note: str) -> None:
        g.text(332, y + 6, label, 13, text, bold=True)
        g.line(track_x0, y, track_x1, y, stroke=edge, sw=2)
        step = (track_x1 - track_x0) / (len(states) - 1)
        for i, st in enumerate(states):
            x = track_x0 + i * step
            g.line(x, y - 5, x, y + 5, stroke=edge, sw=1.6)
            g.text(x, y + 24, st, 13, sub, anchor="middle",
                   max_w=step - 6)
            if i == reached:
                g.circle(x, y, 5.6, fill=accent)
                g.circle(x, y, 9.4, fill="none", stroke=accent, sw=1.2)
        g.text(332, y + 44, note, 11, faint, max_w=1010 - 332)

    rail(374, "CAPA", CAPA_STATES, 382, 1010, 0,
         "grade A +7 d · B +14 d · C +30 d")
    g.text(780, 418, "close gate: verified / closed", 11, green, max_w=300)
    rail(438, "8D", EIGHTD_STATES, 382, 1010, 0,
         "current discipline empty → E_QMS_STEP_ILLEGAL")

    # ======================= read-only review cards ========================
    for x0, x1, title, line1, line2 in (
            (312, 676, "qms.8d_check · R0",
             "missing 8 · thin 0 · ready_to_close false",
             "thin = evidence under 10 characters"),
            (688, 1056, "qms.capa_effectiveness · R0",
             "blockers [state_not_verified] · ready false",
             "state gate · overdue · recurrence")):
        g.rect(x0, 504, x1 - x0, 82, fill=card_c, rx=14, stroke=edge, sw=1,
               shadow=True)
        g.chip(x0 + 18, 518, title, fg=sub, bg=band, size=12, stroke=edge)
        g.text(x0 + 18, 558, line1, 11.5, text, max_w=x1 - x0 - 36)
        g.text(x0 + 18, 576, line2, 11, faint, max_w=x1 - x0 - 36)
    g.path("M494 492 v8", stroke=faint, sw=1.4, dash="3 3", marker="arrF")
    g.path("M872 492 v8", stroke=faint, sw=1.4, dash="3 3", marker="arrF")

    # ======================= boundary card =================================
    g.rect(44, 500, 224, 84, fill=card_c, rx=14, stroke=edge, sw=1, shadow=True)
    g.text(62, 522, "BOUNDARY", 11, faint, bold=True, spacing=1.2)
    g.text(62, 546, "no network request", 11, sub, max_w=188)
    g.text(62, 562, "no model call", 11, sub, max_w=188)
    g.text(62, 578, "input CSV never modified", 11, sub, max_w=188)

    # ======================= storage strip =================================
    g.rect(44, 602, 1012, 38, fill=band, rx=12, stroke=accent, sw=1.4)
    g.text(62, 626, "$DSH_HOME/storages/qms", 13, accent, bold=True,
           max_w=240)
    g.text(300, 626, "storage domain qms v1 · ncrs 12 · aliases 1 · "
                     "capas 1 · eightd 1", 11.5, sub, max_w=600)
    g.text(1036, 626, "R1 writes land here", 11, faint, anchor="end")

    if g.overflows:
        raise SystemExit("FATAL: flow text overflow: " + "; ".join(g.overflows))

    aria = ("dsh-qms-capa structure: a vertical ingest spine (ncrs.csv with its "
            "eight columns, qms.ncr splitting 12 new rows from 3 duplicates "
            "that keep their existing id, qms.batch_alias turning L-1001 into "
            "the canonical lot LOT-A) feeds an impact plate where the stock and "
            "intransit snapshot lanes converge on one verdict (affected 2, "
            "recall_hint true, evidence_sha256), with a dashed gate for a "
            "missing snapshot; below, two state rails (CAPA opened to closed, "
            "8D d1 to closed) carry the grade-based due dates and the "
            "empty-discipline gate; two read-only review cards read those rails "
            "back without writing, and every R1 write lands in the local qms "
            "storage domain, with no network and no model call")
    return g.svg(FLOW_W, FLOW_H, aria, defs)


# =========================================================================== main
def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    written: list[str] = []
    for lang in ("zh", "en"):
        for skin in ("light", "dark"):
            written.append(hero(lang, skin))
    for skin in ("light", "dark"):
        name = f"{NAME}-flow-v5-{skin}.svg"
        with open(os.path.join(OUT, name), "w", encoding="utf-8",
                  newline="\n") as fh:
            fh.write(flow(skin))
        written.append(name)
    for name in written:
        path = os.path.join(OUT, name)
        print(f"wrote docs/assets/{name} ({os.path.getsize(path)} bytes)")
    print(f"done: {len(written)} assets")


if __name__ == "__main__":
    main()
