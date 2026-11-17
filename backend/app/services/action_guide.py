from io import BytesIO
from pathlib import Path

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

GUIDE_PATH = Path(__file__).resolve().parents[1] / "assets" / "action_guide.txt"
FONT_PATHS = (
	Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
	Path("C:/Windows/Fonts/arial.ttf"),
)


def _register_unicode_font() -> str:
	for font_path in FONT_PATHS:
		if font_path.exists():
			pdfmetrics.registerFont(TTFont("GuideSans", str(font_path)))
			return "GuideSans"
	return "Helvetica"


def build_action_guide_pdf() -> bytes:
	font_name = _register_unicode_font()
	styles = getSampleStyleSheet()
	styles.add(ParagraphStyle(
		name="GuideTitle", parent=styles["Title"], fontName=font_name,
		fontSize=18, leading=24, alignment=TA_CENTER, textColor="#292b25",
		spaceAfter=5 * mm,
	))
	styles.add(ParagraphStyle(
		name="GuideHeading", parent=styles["Heading2"], fontName=font_name,
		fontSize=11, leading=15, textColor="#596044", spaceBefore=4 * mm,
		spaceAfter=1.5 * mm,
	))
	styles.add(ParagraphStyle(
		name="GuideBody", parent=styles["BodyText"], fontName=font_name,
		fontSize=9, leading=14, textColor="#45463f", spaceAfter=2 * mm,
	))

	story = []
	for line in GUIDE_PATH.read_text(encoding="utf-8").splitlines():
		text = line.strip()
		if not text:
			story.append(Spacer(1, 2 * mm))
		elif text.startswith("KENETLEN") or text.startswith("BASLANGIC EYLEM REHBERI"):
			story.append(Paragraph(text, styles["GuideTitle"]))
		elif text[:1].isdigit() and ". " in text[:4]:
			story.append(Paragraph(text, styles["GuideHeading"]))
		elif text in {"BU BELGE HAKKINDA", "SON NOT"}:
			story.append(Paragraph(text, styles["GuideHeading"]))
		else:
			story.append(Paragraph(text.replace("&", "&amp;"), styles["GuideBody"]))

	buffer = BytesIO()
	document = SimpleDocTemplate(
		buffer,
		pagesize=A4,
		leftMargin=22 * mm,
		rightMargin=22 * mm,
		topMargin=20 * mm,
		bottomMargin=20 * mm,
		title="KENETLEN - Baslangic Eylem Rehberi",
		author="KENETLEN",
	)
	document.build(story)
	return buffer.getvalue()
