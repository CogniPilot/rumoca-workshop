"""One editable Markdown source -> editable PPTX and matching vector-text PDF."""
from __future__ import annotations
import re
import hashlib
from pathlib import Path
from slide_assets import build_assets
from common import ROOT, write_json

W, H = 13.333333, 7.5
INK, TEAL, GOLD, PAPER, WHITE = "23252A", "007C91", "B59A55", "F7F5F0", "FFFFFF"


def parse():
    text = (ROOT/"slides/workshop.md").read_text()
    slides = []
    for part in re.split(r"^## ", text, flags=re.M)[1:]:
        title, rest = part.split("\n", 1)
        number, title = title.split(" · ", 1)
        before, notes = rest.split("Notes:\n", 1)
        meta, bullets = {}, []
        for line in before.splitlines():
            if line.startswith("- "):
                bullets.append(line[2:])
            elif ": " in line:
                key, value = line.split(": ", 1)
                meta[key.lower()] = value
        slides.append({"number": number, "title": title, "bullets": bullets,
                       "notes": notes.strip(), **meta})
    previous = 600
    for slide in slides[:22]:
        a, b = slide["time"].split("–")
        minutes = lambda x: int(x.split(":")[0])*60+int(x.split(":")[1])
        assert minutes(a) == previous, slide
        assert minutes(a) % 5 == 0 and minutes(b) % 5 == 0, slide
        previous = minutes(b)
    assert previous == 780 and len(slides) == 26
    return slides


def main():
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from PIL import Image
    from matplotlib.font_manager import findfont, FontProperties
    build_assets()
    slides = parse()
    out = ROOT/"slides"
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    prs.core_properties.title = "Hands-On with Rumoca"
    prs.core_properties.author = "James Goppert · Purdue University"
    prs.core_properties.subject = "American Modelica Conference · Georgia Tech · October 12, 2026"
    for name, family, weight in [("Workshop", "DejaVu Sans", "normal"), ("WorkshopBold", "DejaVu Sans", "bold"), ("WorkshopMono", "DejaVu Sans Mono", "normal")]:
        pdfmetrics.registerFont(TTFont(name, findfont(FontProperties(family=family, weight=weight))))
    pdf = canvas.Canvas(str(out/"workshop.pdf"), pagesize=(W*72, H*72))
    pdf.setTitle(prs.core_properties.title); pdf.setAuthor(prs.core_properties.author)
    audit = []
    for spec in slides:
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        slide.background.fill.solid(); slide.background.fill.fore_color.rgb = RGBColor.from_string(PAPER)
        pdf.setFillColor("#"+PAPER); pdf.rect(0, 0, W*72, H*72, fill=1, stroke=0)
        def rect(x, y, w, h, color, rounded=False):
            shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
                                           Inches(x), Inches(y), Inches(w), Inches(h))
            shape.fill.solid(); shape.fill.fore_color.rgb = RGBColor.from_string(color)
            shape.line.fill.background()
            pdf.setFillColor("#"+color)
            pdf.rect(x*72, (H-y-h)*72, w*72, h*72, fill=1, stroke=0)
        def text(value, x, y, w, size=28, color=INK, bold=False, mono=False, max_lines=None):
            # Wrap once using actual font metrics; both formats use identical lines.
            pdf_font = "WorkshopMono" if mono else "WorkshopBold" if bold else "Workshop"
            lines = []
            for paragraph in value.split("\n"):
                current = ""
                for word in paragraph.split():
                    candidate = (current+" "+word).strip()
                    if pdfmetrics.stringWidth(candidate, pdf_font, size) > w*72 and current:
                        lines.append(current); current = word
                    else:
                        current = candidate
                lines.append(current)
            if max_lines is not None:
                assert len(lines) <= max_lines, (spec["number"], value, lines)
            height = len(lines)*size*1.24/72 + .06
            assert y+height <= H-.13, (spec["number"], "text overflow", value)
            shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w+.06), Inches(height+.08))
            tf = shape.text_frame
            tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
            tf.word_wrap = False
            for idx, line in enumerate(lines):
                p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                p.text = line
                p.font.name = "DejaVu Sans Mono" if mono else "DejaVu Sans"
                p.font.size = Pt(size); p.font.bold = bold; p.font.color.rgb = RGBColor.from_string(color)
                p.space_before = p.space_after = Pt(0); p.line_spacing = 1.24
            pdf.setFont(pdf_font, size); pdf.setFillColor("#"+color)
            for i, line in enumerate(lines):
                pdf.drawString(x*72, (H-y)*72-size-i*size*1.24, line)
            audit.append({"slide": spec["number"], "text": value, "font_pt": size, "lines": len(lines)})
            return height
        def picture(path, x, y, w, h):
            path = (out/path).resolve()
            with Image.open(path) as im: iw, ih = im.size
            scale = min(w/iw, h/ih)
            aw, ah = iw*scale, ih*scale
            xx, yy = x+(w-aw)/2, y+(h-ah)/2
            slide.shapes.add_picture(str(path), Inches(xx), Inches(yy), width=Inches(aw), height=Inches(ah))
            pdf.drawImage(str(path), xx*72, (H-yy-ah)*72, aw*72, ah*72)
        rect(0, 0, W, .075, GOLD)
        text(spec.get("badge", ""), .65, .25, 10.6, 13, TEAL, bold=True, max_lines=1)
        text(spec["time"], 11.2, .25, 1.55, 12, INK, max_lines=1)
        layout = spec["layout"]
        if layout == "title":
            title_height = text(spec["title"], .65, 1.15, 10.9, 52, bold=True, max_lines=2)
            y = max(3., 1.15+title_height+.3)
            for bullet in spec["bullets"]:
                y += text(bullet, .7, y, 8.6, 25, max_lines=2) + .22
            picture(spec["visual"], 10.0, 3., 2.35, 2.35)
        elif layout == "break":
            text(spec["title"], .65, 1.2, 12., 50, bold=True, max_lines=1)
            y = 3.
            for bullet in spec["bullets"]:
                y += text(bullet, .7, y, 11.7, 28, max_lines=2)+.3
        else:
            title_size = min(37, 12*72/pdfmetrics.stringWidth(spec["title"], "WorkshopBold", 37)*37)
            assert title_size >= 30, (spec["number"], "Shorten the title")
            text(spec["title"], .65, .78, 12., title_size, bold=True, max_lines=1)
            if layout == "cards":
                for i, bullet in enumerate(spec["bullets"]):
                    x, y = .65+(i%2)*6.15, 1.8+(i//2)*2.0
                    rect(x, y, 5.85, 1.72, WHITE)
                    rect(x, y, .065, 1.72, TEAL if i%2 == 0 else GOLD)
                    text(bullet, x+.25, y+.3, 5.3, 27, max_lines=3)
            elif layout == "image":
                y = 1.8
                for bullet in spec["bullets"]:
                    y += text(bullet, .7, y, 4.3, 27, max_lines=3)+.34
                picture(spec["visual"], 5.2, 1.55, 7.5, 4.4)
            elif layout == "wide":
                image_y = 1.6
                if spec["bullets"]:
                    image_y = 1.48 + text(spec["bullets"][0], .7, 1.48, 11.9, 23, max_lines=2) + .15
                picture(spec["visual"], .7, image_y, 11.9, (6.0 if "command" in spec else 6.4)-image_y)
            elif layout == "statement":
                y = 2.0
                for bullet in spec["bullets"]:
                    y += text(bullet, .75, y, 11.8, 30, max_lines=2)+.45
            else:
                raise ValueError(layout)
        if "command" in spec:
            rect(.65, 6.18, 12.05, .5, INK)
            text(spec["command"], .85, 6.27, 11.7, 20, WHITE, mono=True, max_lines=1)
        text(spec["checkpoint"], .7, 6.78, 12., 20, TEAL, bold=True, max_lines=1)
        text("PURDUE · AERONAUTICS & ASTRONAUTICS     /     GEORGIA TECH · AMC 2026", .7, 7.12, 11.9, 9, INK, max_lines=1)
        text(spec["number"], 12.3, 7.1, .5, 12, TEAL, max_lines=1)
        slide.notes_slide.notes_text_frame.text = spec["time"]+"\n"+spec["notes"]
        pdf.showPage()
    prs.save(str(out/"workshop.pptx"))
    pdf.save()
    inputs = {"slides/workshop.md", "models/Quadrotor.mo", "data/noisy_flight.csv",
              "results/reference/fit_drag.json", "results/reference/trajectory.npz",
              "scripts/build_slides.py", "scripts/slide_assets.py", "pyproject.toml", "uv.lock"}
    inputs.update(str((out/s["visual"]).resolve().relative_to(ROOT))
                  for s in slides if "visual" in s)
    digest = lambda path: hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
    write_json(out/"build-report.json", {"slides": len(slides), "main_slides": 22,
               "schedule_minutes": 180, "break_minutes": 20, "source": "slides/workshop.md",
               "input_sha256": {p: digest(p) for p in sorted(inputs)},
               "artifact_sha256": {p: digest(p) for p in ["slides/workshop.pptx", "slides/workshop.pdf"]},
               "rendered_text": audit, "notes_in_pptx": True})
    print(f"Built {len(slides)} slides, PPTX + PDF, 180-minute schedule, speaker notes")


if __name__ == "__main__":
    main()
