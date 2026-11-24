"""Export the editable interim Markdown to a one-page PDF and check page count."""
from html import escape
from pathlib import Path

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "interim_update.md").read_text(encoding="utf-8")
target = ROOT / "interim_update.pdf"
styles = {
    "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=15, leading=18,
                            textColor=colors.HexColor("#173548"), spaceAfter=6),
    "heading": ParagraphStyle("heading", fontName="Helvetica-Bold", fontSize=10.5, leading=13,
                              textColor=colors.HexColor("#173548"), spaceBefore=7, spaceAfter=3,
                              keepWithNext=True),
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=9.5, leading=12, spaceAfter=5),
}
story = []
for block in source.strip().split("\n\n"):
    style = "title" if block.startswith("# ") else "heading" if block.startswith("## ") else "body"
    text = block[2:] if style == "title" else block[3:] if style == "heading" else block
    story.append(Paragraph(escape(text).replace("\n", " "), styles[style]))
doc = SimpleDocTemplate(str(target), pagesize=letter, rightMargin=42, leftMargin=42,
                        topMargin=35, bottomMargin=35, title="EAS 510 Project 2 Interim Update",
                        author="Dai Trang Vo")
doc.build(story)
reader = PdfReader(target)
if len(reader.pages) != 1:
    raise RuntimeError(f"Expected one page; got {len(reader.pages)}. Edit the update or layout.")
text = reader.pages[0].extract_text()
for required in ("0.195812", "0.304555", "0.190134", "December 7", "daitrang"):
    if required not in text:
        raise RuntimeError(f"PDF text is missing {required}")
print(f"Wrote {target}: one page, {len(text.split())} extracted words")
