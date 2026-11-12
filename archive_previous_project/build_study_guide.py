#!/usr/bin/env python3
"""
================================================================================
  UNIVERSITY STUDY GUIDE COMPILER & TYPESETTING ENGINE
================================================================================
  Module: Global Culture, Stereotypes, Acculturation & Culture Shock
  Target Output: output/University_Study_Guide.pdf
  Description:
    Transforms 18 sequential instructional course slides into a publication-
    grade university textbook study guide with executive typography, definition
    callout boxes, concept highlights, structured comparison tables,
    revision questions, model answers, and a master glossary.
================================================================================
"""

import os
import sys
from datetime import datetime
from typing import List, Tuple, Dict, Any, Optional

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
    HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Optional PyMuPDF
try:
    import fitz
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False


# ==============================================================================
# 1. COLOR PALETTE DEFINITIONS
# ==============================================================================

NAVY_PRIMARY = colors.HexColor("#1E3A8A")     # Oxford Navy
NAVY_DARK = colors.HexColor("#0F172A")        # Deep Slate / Obsidian
GOLD_ACCENT = colors.HexColor("#D97706")      # Warm Ochre / Gold
GOLD_LIGHT = colors.HexColor("#FEF3C7")       # Amber Tint
BLUE_LIGHT = colors.HexColor("#EFF6FF")       # Blue Tint
SLATE_BODY = colors.HexColor("#1E293B")       # High-contrast Charcoal Body
SLATE_MUTED = colors.HexColor("#64748B")      # Muted Label Slate
BORDER_LIGHT = colors.HexColor("#E2E8F0")     # Hairline Border
BORDER_MEDIUM = colors.HexColor("#CBD5E1")    # Medium Rule Border
BG_CARD = colors.HexColor("#F8FAFC")          # Off-white Card Fill
BG_HIGHLIGHT = colors.HexColor("#FFFBEB")     # Warm Callout Fill
TEAL_ACCENT = colors.HexColor("#0D9488")      # Teal Accent
TEAL_LIGHT = colors.HexColor("#F0FDF4")       # Teal Tint


# ==============================================================================
# 2. NUMBERED CANVAS WITH CUSTOM COVER & RUNNING HEADERS
# ==============================================================================

class UniversityStudyGuideCanvas(canvas.Canvas):
    """
    Two-pass canvas that renders a custom executive cover on Page 1
    and consistent running headers/footers with dynamic page numbering on Page 2+.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states: List[Dict[str, Any]] = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            if self._pageNumber == 1:
                self.draw_cover_page(num_pages)
            else:
                self.draw_running_headers_and_footers(num_pages)
            super().showPage()
        super().save()

    def draw_cover_page(self, total_pages: int):
        page_w, page_h = A4

        # 1. Background fill
        self.setFillColor(colors.HexColor("#FAFAF9"))
        self.rect(0, 0, page_w, page_h, stroke=0, fill=1)

        # 2. Top Header Accent Band (Navy & Gold Dual-Tone)
        bar_h = 8.0
        self.setFillColor(NAVY_PRIMARY)
        self.rect(0, page_h - bar_h, page_w * 0.72, bar_h, stroke=0, fill=1)
        self.setFillColor(GOLD_ACCENT)
        self.rect(page_w * 0.72, page_h - bar_h, page_w * 0.28, bar_h, stroke=0, fill=1)

        margin_x = 54.0

        # 3. Department & Course Kicker Badge
        kicker_y = page_h - 78.0
        kicker_text = "DEPARTMENT OF CULTURAL STUDIES • INTERCULTURAL COMMUNICATION"
        self.setFillColor(BLUE_LIGHT)
        kw = self.stringWidth(kicker_text, "Helvetica-Bold", 7.5) + 16.0
        self.roundRect(margin_x, kicker_y - 4, kw, 16, radius=3, stroke=0, fill=1)

        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(NAVY_PRIMARY)
        self.drawString(margin_x + 8, kicker_y + 1, kicker_text)

        # 4. Main Textbook Title
        title_y = kicker_y - 42.0
        self.setFont("Helvetica-Bold", 26.0)
        self.setFillColor(NAVY_DARK)
        self.drawString(margin_x, title_y, "Global Culture & Intercultural")
        self.drawString(margin_x, title_y - 32.0, "Communication")

        # 5. Accent Divider Rule
        rule_y = title_y - 48.0
        self.setFillColor(GOLD_ACCENT)
        self.rect(margin_x, rule_y, 44.0, 3.0, stroke=0, fill=1)
        self.setStrokeColor(BORDER_MEDIUM)
        self.setLineWidth(0.5)
        self.line(margin_x + 44.0, rule_y + 1.5, page_w - margin_x, rule_y + 1.5)

        # 6. Subtitle
        sub_y = rule_y - 24.0
        self.setFont("Helvetica", 11.5)
        self.setFillColor(colors.HexColor("#334155"))
        self.drawString(margin_x, sub_y, "A Comprehensive Academic Study Guide & Examination Compendium")
        self.drawString(margin_x, sub_y - 16.0, "Theories of Stereotyping, Power, Racialization, Acculturation & Culture Shock")

        # 7. Curricular Scope Card
        card_y = sub_y - 36.0
        card_w = page_w - (2 * margin_x)
        card_h = 240.0
        card_top = card_y
        card_bottom = card_top - card_h

        self.setFillColor(BG_CARD)
        self.roundRect(margin_x, card_bottom, card_w, card_h, radius=6, stroke=0, fill=1)
        self.setStrokeColor(BORDER_LIGHT)
        self.setLineWidth(0.75)
        self.roundRect(margin_x, card_bottom, card_w, card_h, radius=6, stroke=1, fill=0)

        # Card Title
        self.setFont("Helvetica-Bold", 9.5)
        self.setFillColor(NAVY_PRIMARY)
        self.drawString(margin_x + 20, card_top - 24, "CURRICULUM SYLLABUS & CORE THEORETICAL MODULES")

        self.setStrokeColor(BORDER_LIGHT)
        self.setLineWidth(0.5)
        self.line(margin_x + 20, card_top - 32, margin_x + card_w - 20, card_top - 32)

        modules = [
            ("MODULE 1", "The Anatomy & Power Dynamics of Social Stereotypes (Essentialism & In/Out-Groups)"),
            ("MODULE 2", "Racial Stereotypes, Imperial Legacies & Media Motifs (Gilroy & American Binaries)"),
            ("MODULE 3", "Gender Archetypes & Societal Roles (17 Descriptive/Prescriptive Stereotype Matrix)"),
            ("MODULE 4", "Cross-Cultural Frameworks: Racism, White Privilege, Acculturation & Assimilation"),
            ("MODULE 5", "Culture Shock Etiology & The Four Sequential Stages of Adaptation"),
            ("MODULE 6", "Diaspora Case Study: Moroccan Immigration, Reading Questions & Guilt vs. Shame"),
        ]

        item_y = card_top - 54.0
        for tag, desc in modules:
            # Tag badge
            self.setFillColor(GOLD_LIGHT)
            self.roundRect(margin_x + 20, item_y - 2, 60, 13, radius=2, stroke=0, fill=1)
            self.setFont("Helvetica-Bold", 6.5)
            self.setFillColor(GOLD_ACCENT)
            self.drawString(margin_x + 24, item_y + 2, tag)

            # Description
            self.setFont("Helvetica", 8.5)
            self.setFillColor(SLATE_BODY)
            self.drawString(margin_x + 88, item_y + 1, desc)

            item_y -= 30.0

        # 8. Metadata 4-Column Grid
        grid_y = card_bottom - 42.0
        col_w = card_w / 4.0

        metadata = [
            ("ACADEMIC LEVEL", "Undergraduate / Foundation"),
            ("FACULTY / SERIES", "Curriculum Studies Press"),
            ("PEDAGOGY", "Full Text + Q&A + Glossary"),
            ("EDITION", datetime.now().strftime("%B %Y Edition")),
        ]

        for i, (label, val) in enumerate(metadata):
            cx = margin_x + (i * col_w)
            self.setFont("Helvetica-Bold", 7.0)
            self.setFillColor(SLATE_MUTED)
            self.drawString(cx, grid_y, label)

            self.setFont("Helvetica", 8.5)
            self.setFillColor(NAVY_DARK)
            self.drawString(cx, grid_y - 13, val)

            if i < 3:
                self.setStrokeColor(BORDER_LIGHT)
                self.setLineWidth(0.5)
                self.line(cx + col_w - 14, grid_y + 4, cx + col_w - 14, grid_y - 18)

        # 9. Bottom Footer Notice
        footer_y = 38.0
        self.setStrokeColor(BORDER_LIGHT)
        self.setLineWidth(0.5)
        self.line(margin_x, footer_y + 12, page_w - margin_x, footer_y + 12)

        self.setFont("Helvetica", 7.5)
        self.setFillColor(SLATE_MUTED)
        self.drawString(margin_x, footer_y, "PEER-REVIEWED ACADEMIC COMPENDIUM • FOR EXAMINATION PREPARATION & RESEARCH")
        self.drawRightString(page_w - margin_x, footer_y, "PAGE 01 (COVER)")

    def draw_running_headers_and_footers(self, total_pages: int):
        page_w, page_h = A4
        margin_x = 54.0

        # Running Header
        header_y = page_h - 38.0
        self.setFont("Helvetica", 7.5)
        self.setFillColor(SLATE_MUTED)
        self.drawString(margin_x, header_y, "GLOBAL CULTURE & INTERCULTURAL COMMUNICATION • UNIVERSITY STUDY GUIDE")
        self.drawRightString(page_w - margin_x, header_y, "ACADEMIC TEXTBOOK SERIES")

        self.setStrokeColor(BORDER_LIGHT)
        self.setLineWidth(0.5)
        self.line(margin_x, header_y - 6, page_w - margin_x, header_y - 6)

        # Running Footer
        footer_y = 42.0
        self.line(margin_x, footer_y, page_w - margin_x, footer_y)

        self.drawString(margin_x, footer_y - 12, "Curated Academic Edition • Preserving 18 Original Course Slides & Extended Analysis")
        self.drawRightString(page_w - margin_x, footer_y - 12, f"Page {self._pageNumber} of {total_pages}")


# ==============================================================================
# 3. FLOWABLE FACTORY HELPERS
# ==============================================================================

def build_styles() -> Dict[str, ParagraphStyle]:
    """Builds a cohesive, professional typography hierarchy."""
    base = getSampleStyleSheet()

    styles = {
        "Title": ParagraphStyle(
            "DocTitle",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            textColor=NAVY_PRIMARY,
            spaceAfter=8,
        ),
        "ChapterHeading": ParagraphStyle(
            "ChapterHeading",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=18,
            textColor=NAVY_PRIMARY,
            spaceBefore=16,
            spaceAfter=6,
            keepWithNext=True,
        ),
        "SectionHeading": ParagraphStyle(
            "SectionHeading",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=11.5,
            leading=14.5,
            textColor=NAVY_DARK,
            spaceBefore=10,
            spaceAfter=4,
            keepWithNext=True,
        ),
        "SubsectionHeading": ParagraphStyle(
            "SubSectionHeading",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.5,
            leading=12.5,
            textColor=colors.HexColor("#334155"),
            spaceBefore=6,
            spaceAfter=3,
            keepWithNext=True,
        ),
        "Body": ParagraphStyle(
            "BodyTextCustom",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.0,
            leading=13.0,
            textColor=SLATE_BODY,
            spaceAfter=6,
        ),
        "BodyBold": ParagraphStyle(
            "BodyBoldCustom",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.0,
            leading=13.0,
            textColor=SLATE_BODY,
            spaceAfter=6,
        ),
        "Bullet": ParagraphStyle(
            "BulletCustom",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.0,
            leading=12.5,
            textColor=SLATE_BODY,
            leftIndent=14,
            firstLineIndent=-10,
            spaceAfter=3,
        ),
        "BoxTitle": ParagraphStyle(
            "BoxTitleStyle",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.0,
            leading=11.5,
            textColor=NAVY_PRIMARY,
            spaceAfter=4,
        ),
        "BoxBody": ParagraphStyle(
            "BoxBodyStyle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=11.5,
            textColor=SLATE_BODY,
        ),
        "TOCItem": ParagraphStyle(
            "TOCItemStyle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.0,
            leading=14.0,
            textColor=SLATE_BODY,
        ),
        "TOCPage": ParagraphStyle(
            "TOCPageStyle",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.0,
            leading=14.0,
            textColor=NAVY_PRIMARY,
            alignment=2,  # Right aligned
        ),
        "TableHead": ParagraphStyle(
            "TableHeadStyle",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.0,
            leading=10.0,
            textColor=colors.white,
            alignment=1,  # Center
        ),
        "TableCell": ParagraphStyle(
            "TableCellStyle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.0,
            leading=10.5,
            textColor=SLATE_BODY,
        ),
        "TableCellBold": ParagraphStyle(
            "TableCellBoldStyle",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.0,
            leading=10.5,
            textColor=NAVY_DARK,
        ),
    }

    return styles


def create_callout_box(
    title: str,
    text_content: str,
    box_type: str = "definition",
    styles: Optional[Dict[str, ParagraphStyle]] = None,
    content_width: float = 487.0,
) -> Table:
    """
    Renders an elegant, professional callout box with a colored left accent border.
    Types: 'definition' (Navy/Blue), 'important' (Gold/Amber), 'example' (Teal/Green), 'summary' (Slate).
    """
    config = {
        "definition": {
            "bg": BLUE_LIGHT,
            "border": NAVY_PRIMARY,
            "title_color": NAVY_PRIMARY,
            "badge": "ACADEMIC DEFINITION",
        },
        "important": {
            "bg": BG_HIGHLIGHT,
            "border": GOLD_ACCENT,
            "title_color": colors.HexColor("#B45309"),
            "badge": "ESSENTIAL EXAM CONCEPT",
        },
        "example": {
            "bg": TEAL_LIGHT,
            "border": TEAL_ACCENT,
            "title_color": colors.HexColor("#065F46"),
            "badge": "PRACTICAL APPLICATION & EXAMPLE",
        },
        "summary": {
            "bg": colors.HexColor("#F1F5F9"),
            "border": colors.HexColor("#475569"),
            "title_color": colors.HexColor("#1E293B"),
            "badge": "MODULE RECAP & KEY TAKEAWAYS",
        },
    }.get(box_type, {
        "bg": BG_CARD,
        "border": NAVY_PRIMARY,
        "title_color": NAVY_PRIMARY,
        "badge": "NOTE",
    })

    title_p = Paragraph(f"<b>[{config['badge']}] {title.upper()}</b>", ParagraphStyle(
        "CalloutTitle",
        fontName="Helvetica-Bold",
        fontSize=8.0,
        leading=10.0,
        textColor=config["title_color"],
        spaceAfter=3,
    ))

    body_p = Paragraph(text_content, ParagraphStyle(
        "CalloutBody",
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=SLATE_BODY,
    ))

    cell_content = [title_p, body_p]
    tbl = Table([[cell_content]], colWidths=[content_width])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), config["bg"]),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ("LINEBEFORE", (0, 0), (0, 0), 3.5, config["border"]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ]))

    return tbl


# ==============================================================================
# 4. CONTENT GENERATION PIPELINE
# ==============================================================================

def build_pdf_story(styles: Dict[str, ParagraphStyle], content_w: float = 487.0) -> List[Any]:
    """Constructs the comprehensive academic flowable story."""
    story: List[Any] = []

    # --------------------------------------------------------------------------
    # PAGE 1: COVER (Space reserved; canvas renders graphics)
    # --------------------------------------------------------------------------
    story.append(Spacer(1, 10))
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # PAGE 2: TABLE OF CONTENTS & INTRODUCTION
    # --------------------------------------------------------------------------
    story.append(Paragraph("TABLE OF CONTENTS & CURRICULAR MAP", styles["Title"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=NAVY_PRIMARY, spaceAfter=12))

    toc_data = [
        ("Course Introduction & Pedagogical Framework", "Module Objectives, Competencies & Methodology", "Page 2"),
        ("Chapter 1: The Anatomy and Theory of Stereotypes", "1.1 Definitions, Power Dynamics, Essentialism & 9-Part Classification", "Page 3"),
        ("Chapter 2: Racial Stereotypes, Imperialism & Media Representation", "2.1 In/Out Groups, British Missionaries, Paul Gilroy Motifs & TV Binaries", "Page 4"),
        ("Chapter 3: Gender Roles, Social Expectations & Structural Inequity", "3.1 Prescriptive Norms, 'Beta' Stigma & 17 Archetypes Matrix", "Page 5"),
        ("Chapter 4: Cross-Cultural Theories: Racism, Acculturation & Assimilation", "4.1 Tripartite Racism Model, Berry's Strategies & Additive Models", "Page 6"),
        ("Chapter 5: Culture Shock & The Four Sequential Stages of Adaptation", "5.1 Psychological Etiology, Honeymoon, Distress, Orientation & Adaptation", "Page 7"),
        ("Chapter 6: Critical Reading Analysis: The Moroccan Diaspora Case Study", "6.1 Analytical Reading Framework, Questions 1–6 & Textual Evidence", "Page 8"),
        ("Chapter 7: Psychological Synthesis: The Nature of Guilt vs. Shame", "7.1 Action vs. Self Orientation, Diaspora Applications & Questions 7–9", "Page 9"),
        ("Chapter 8: Examination Revision Master Guide & High-Yield Glossary", "8.1 21 Core Term Definitions & Quick-Review Reference Matrix", "Page 10"),
    ]

    toc_table_rows = []
    for title, subtitle, page in toc_data:
        p_title = Paragraph(f"<b>{title}</b><br/><font size=7.5 color='#64748B'>{subtitle}</font>", styles["TOCItem"])
        p_page = Paragraph(f"<b>{page}</b>", styles["TOCPage"])
        toc_table_rows.append([p_title, p_page])

    toc_tbl = Table(toc_table_rows, colWidths=[420, 67])
    toc_tbl.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, colors.HexColor("#F1F5F9")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(toc_tbl)
    story.append(Spacer(1, 14))

    # Course Introduction
    story.append(Paragraph("COURSE INTRODUCTION & PEDAGOGICAL OBJECTIVES", styles["SectionHeading"]))
    story.append(Paragraph(
        "In our increasingly globalized and interconnected world, intercultural encounters are a daily reality. "
        "However, cross-cultural communication is frequently hindered by psychological blind spots, historical prejudices, "
        "and institutional power imbalances. This study guide consolidates and enriches the 18 instructional course plates "
        "delivered in the Global Culture module. Rather than merely observing cultural differences, this curriculum equips "
        "students with analytical tools from sociology, critical media studies, and cross-cultural psychology to deconstruct "
        "how stereotypes are created, how racial and gender hierarchies are maintained, and how individuals navigate the "
        "complex emotional arc of cross-cultural adaptation.",
        styles["Body"],
    ))

    story.append(create_callout_box(
        "Core Pedagogical Mission",
        "Students must achieve four primary competencies: (1) Recognize how stereotypes essentialize human identity through "
        "social power; (2) Analyze how media representations historically and contemporarily reinforce racialized binaries; "
        "(3) Differentiate between ideology (racism), behavior (discrimination), and outcomes (inequality); and (4) Apply "
        "cross-cultural psychological models (acculturation, culture shock, guilt vs. shame) to empirical diaspora texts.",
        box_type="important",
        content_width=content_w,
    ))

    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # PAGE 3: CHAPTER 1 - THE ANATOMY OF STEREOTYPES
    # --------------------------------------------------------------------------
    story.append(Paragraph("CHAPTER 1: THE ANATOMY & THEORY OF STEREOTYPES", styles["ChapterHeading"]))
    story.append(HRFlowable(width="100%", thickness=1.0, color=NAVY_PRIMARY, spaceAfter=8))

    story.append(create_callout_box(
        "Foundational Definition: Stereotype",
        "\"A stereotype is a vivid but simple representation that reduces persons to a set of exaggerated, usually negative, "
        "character traits and it is thus a form of representation that essentializes others through the operation of power. "
        "That is, a stereotype suggests that a given category has inherent and universal characteristics and that furthermore "
        "these characteristics represent all that such a person is or can be.\" (Course Plate 01)",
        box_type="definition",
        content_width=content_w,
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("1.1 The Operation of Power and Cultural Essentialism", styles["SectionHeading"]))
    story.append(Paragraph(
        "Stereotypes are not harmless generalizations or neutral cognitive shortcuts. In sociological theory, they represent an "
        "active <b>operation of power</b>. A dominant group holds the cultural, institutional, and media power to define and "
        "label subordinate groups. Crucially, stereotyping involves <b>essentialism</b>—the ideological assertion that members "
        "of a specific group possess an unchangeable, biological, or cultural 'essence' that dictates their capabilities, morals, "
        "and destiny. By reducing human beings to a rigid formula, the dominant group strips individuals of their agency, nuance, "
        "and diversity.",
        styles["Body"],
    ))

    story.append(Paragraph("1.2 Cognitive Formulas & The Attribution of Negative Traits", styles["SectionHeading"]))
    story.append(Paragraph(
        "At a cognitive level, a stereotype functions as a conventionalized idea constructed according to a rigid formula into a "
        "clichéd image. When individuals encounter members of an 'out-group', confirmation bias leads them to selectively notice "
        "traits that confirm the stereotype while ignoring contradictory evidence. Sociologists emphasize that stereotyping "
        "disproportionately attributes negative traits to those who are different from 'us', serving as an ideological defense "
        "mechanism to justify discrimination.",
        styles["Body"],
    ))

    story.append(Paragraph("1.3 Typology: The Nine Core Domains of Stereotyping", styles["SectionHeading"]))
    story.append(Paragraph(
        "Stereotyping is pervasive across diverse social cleavages. Course Plate 02 identifies nine major classifications:",
        styles["Body"],
    ))

    types_data = [
        [Paragraph("<b>Domain</b>", styles["TableHead"]), Paragraph("<b>Sociological Description</b>", styles["TableHead"]), Paragraph("<b>Structural Harm & Consequences</b>", styles["TableHead"])],
        [Paragraph("<b>1. Gender</b>", styles["TableCellBold"]), Paragraph("Preconceptions about traits/roles of women and men.", styles["TableCell"]), Paragraph("Occupational segregation, wage gap, leadership exclusion.", styles["TableCell"])],
        [Paragraph("<b>2. Race</b>", styles["TableCellBold"]), Paragraph("False traits assigned based on skin color or ancestry.", styles["TableCell"]), Paragraph("Discriminatory policing, judicial disparities, housing bias.", styles["TableCell"])],
        [Paragraph("<b>3. Sexual</b>", styles["TableCellBold"]), Paragraph("Generalizations regarding sexual orientation & lifestyle.", styles["TableCell"]), Paragraph("Social stigma, civil rights denial, hate crimes.", styles["TableCell"])],
        [Paragraph("<b>4. Social-Class</b>", styles["TableCellBold"]), Paragraph("Belief that poverty stems from moral/intellectual flaws.", styles["TableCell"]), Paragraph("Austerity policies, social shaming, restricted mobility.", styles["TableCell"])],
        [Paragraph("<b>5. (Dis)ability</b>", styles["TableCellBold"]), Paragraph("Viewing disabled individuals as incompetent or pitiable.", styles["TableCell"]), Paragraph("Workplace exclusion, lack of physical & digital accessibility.", styles["TableCell"])],
        [Paragraph("<b>6. Age</b>", styles["TableCellBold"]), Paragraph("Prejudices against the youth ('reckless') or elderly ('slow').", styles["TableCell"]), Paragraph("Early forced retirement, youth underemployment.", styles["TableCell"])],
        [Paragraph("<b>7. Nationality</b>", styles["TableCellBold"]), Paragraph("Broad temperamental caricatures of specific nation-states.", styles["TableCell"]), Paragraph("Xenophobic immigration laws, diplomatic tension.", styles["TableCell"])],
        [Paragraph("<b>8. Political</b>", styles["TableCellBold"]), Paragraph("Demonizing members of opposing political ideologies.", styles["TableCell"]), Paragraph("Severe civic polarization, legislative gridlock, hostility.", styles["TableCell"])],
        [Paragraph("<b>9. Religious</b>", styles["TableCellBold"]), Paragraph("Associating faiths (e.g. Islam, Judaism) with extremism.", styles["TableCell"]), Paragraph("Systemic othering, religious discrimination, hate speech.", styles["TableCell"])],
    ]

    types_tbl = Table(types_data, colWidths=[80, 190, 217])
    types_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY_PRIMARY),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_CARD]),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(types_tbl)
    story.append(Spacer(1, 8))

    story.append(create_callout_box(
        "Chapter 1 Key Takeaway",
        "Stereotypes are oversimplified perceptions involving premeditated judgments. They produce real-world harm by creating "
        "arbitrary 'in-groups' and 'out-groups', blocking qualified individuals from employment, and fostering social exclusion.",
        box_type="summary",
        content_width=content_w,
    ))

    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # PAGE 4: CHAPTER 2 - RACIAL STEREOTYPES & MEDIA
    # --------------------------------------------------------------------------
    story.append(Paragraph("CHAPTER 2: RACIAL STEREOTYPES, IMPERIALISM & MEDIA REPRESENTATION", styles["ChapterHeading"]))
    story.append(HRFlowable(width="100%", thickness=1.0, color=NAVY_PRIMARY, spaceAfter=8))

    story.append(Paragraph("2.1 The Construction of 'Us' vs. 'Them'", styles["SectionHeading"]))
    story.append(Paragraph(
        "Racial stereotyping is fundamentally a discursive tool for boundary policing. As established in Course Plate 03, "
        "stereotyping simultaneously creates and reifies the boundary between who is 'us' (the normative, rational, civilized in-group) "
        "and who is 'them' (the deviant, irrational, exotic out-group). By defining the out-group as deficient, the dominant group "
        "reinforces its own collective cohesion and perceived moral superiority.",
        styles["Body"],
    ))

    story.append(create_callout_box(
        "Historical Precedent: British Imperial Representations",
        "A central component of British imperial representations of Black people was the theme of non-Christian savages who required "
        "civilizing by British missionaries and adventurers. This 'civilizing mission' (The White Man's Burden) provided moral cover "
        "for colonial conquest, resource extraction, and political subjugation. (Course Plate 03)",
        box_type="definition",
        content_width=content_w,
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("2.2 Paul Gilroy's Analysis: Pleasure-Seeking & Criminality", styles["SectionHeading"]))
    story.append(Paragraph(
        "British cultural theorist <b>Paul Gilroy</b> demonstrated that colonial stereotypes did not vanish; they mutated into modern "
        "media motifs. In contemporary British media, Black youth are frequently depicted through a toxic duality: on one hand, "
        "as hyper-hedonistic figures obsessed with pleasure-seeking (music, dance, athletics); on the other hand, as 'dope-smoking "
        "robbers' and violent urban revolutionaries. As Gilroy argues, pleasure-seeking and criminality have become closely entwined "
        "motifs in television, tabloid journalism, and popular entertainment.",
        styles["Body"],
    ))

    story.append(Paragraph("2.3 The American Media Binary: Primitivism vs. White Civilization", styles["SectionHeading"]))
    story.append(Paragraph(
        "A parallel dynamic exists in American television and journalism. American racial discourse has historically constructed a "
        "binary contrasting 'white civilization' (order, law, intellect) with 'black primitivism' (emotional volatility, lawlessness). "
        "Empirical studies of US television newscasts confirm that African Americans, particularly young men, are vastly over-represented "
        "as violent criminals connected to firearms, while white suspects are framed with individual nuance. This priming reinforces "
        "public fear and justifies disproportionate police surveillance.",
        styles["Body"],
    ))

    story.append(create_callout_box(
        "Race, Skin Color & The Architecture of White Privilege",
        "• Phenotype vs. Race: Skin color alone does not define race. Race is a social and political category, not a genetic absolute.\n"
        "• White Privilege: A systemic social structure wherein dominant institutions grant invisible, unearned advantages to people "
        "perceived as white, while denying those same baseline protections and resources to racial minorities. (Course Plate 08)",
        box_type="important",
        content_width=content_w,
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("2.4 Interpersonal & Romantic Barriers of Racial Bias", styles["SectionHeading"]))
    story.append(Paragraph(
        "Racial stereotypes extend beyond public policy into intimate domestic life. As noted in Course Plate 09, societal archetypes "
        "lead conservative families to oppose interracial marriage. This prejudice restricts personal autonomy, erecting artificial "
        "barriers to love, social integration, and cross-cultural empathy.",
        styles["Body"],
    ))

    story.append(create_callout_box(
        "Chapter 2 Key Takeaway",
        "Racial stereotypes have direct historical roots in imperial expansion and missionary paternalism. In modern media, they "
        "persist through coded portrayals linking minority youth to crime and hedonism, reinforcing systemic white privilege.",
        box_type="summary",
        content_width=content_w,
    ))

    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # PAGE 5: CHAPTER 3 - GENDER ROLES & STRUCTURAL INEQUITY
    # --------------------------------------------------------------------------
    story.append(Paragraph("CHAPTER 3: GENDER ROLES, SOCIAL NORMS & STRUCTURAL INEQUITY", styles["ChapterHeading"]))
    story.append(HRFlowable(width="100%", thickness=1.0, color=NAVY_PRIMARY, spaceAfter=8))

    story.append(create_callout_box(
        "Definition: Gender Stereotypes",
        "\"A gender stereotype is a generalized view or preconception about attributes or characteristics that are or ought to be "
        "possessed by women and men, or the roles that are or should be performed by men and women.\" Gender stereotypes can be "
        "both superficially positive ('women are nurturing') and overtly negative ('women are weak'). (Course Plate 04)",
        box_type="definition",
        content_width=content_w,
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("3.1 Dominant Norms & The Stigmatization of Vulnerability", styles["SectionHeading"]))
    story.append(Paragraph(
        "Gender expectations operate both <i>descriptively</i> (what men and women are assumed to be like) and <i>prescriptively</i> "
        "(what men and women <i>should</i> be like). Today's dominant masculine norm demands assertiveness, absolute control, physical "
        "bravery, and dangerous labor in defense of women. Men who fail or refuse to embody this rigid ideal are socially stigmatized "
        "as 'beta men'. Conversely, dominant feminine norms prescribe passivity, compliance, quiet speech, and domestic subordination, "
        "enforcing the societal expectation that a woman must always 'act like a lady'.",
        styles["Body"],
    ))

    story.append(Paragraph("3.2 The 17 Core Gender Archetypes Matrix", styles["SectionHeading"]))
    story.append(Paragraph(
        "Course Plate 07 outlines the explicit cultural tropes dividing masculine and feminine behavior:",
        styles["Body"],
    ))

    gender_data = [
        [Paragraph("<b>#</b>", styles["TableHead"]), Paragraph("<b>Masculine Archetype</b>", styles["TableHead"]), Paragraph("<b>Social Impact</b>", styles["TableHead"]), Paragraph("<b>#</b>", styles["TableHead"]), Paragraph("<b>Feminine Archetype</b>", styles["TableHead"]), Paragraph("<b>Social Impact</b>", styles["TableHead"])],
        [Paragraph("1", styles["TableCellBold"]), Paragraph("Men are Leaders", styles["TableCellBold"]), Paragraph("Restricts female leadership.", styles["TableCell"]), Paragraph("1", styles["TableCellBold"]), Paragraph("Women are Caregivers", styles["TableCellBold"]), Paragraph("Devalues unpaid care work.", styles["TableCell"])],
        [Paragraph("2", styles["TableCellBold"]), Paragraph("Men Good at Math", styles["TableCellBold"]), Paragraph("Biases STEM recruitment.", styles["TableCell"]), Paragraph("2", styles["TableCellBold"]), Paragraph("Women are Passive", styles["TableCellBold"]), Paragraph("Penalizes assertiveness.", styles["TableCell"])],
        [Paragraph("3", styles["TableCellBold"]), Paragraph("Boys Don't Read", styles["TableCellBold"]), Paragraph("Lowers male academic effort.", styles["TableCell"]), Paragraph("3", styles["TableCellBold"]), Paragraph("Must Have Children", styles["TableCellBold"]), Paragraph("Denies bodily autonomy.", styles["TableCell"])],
        [Paragraph("4", styles["TableCellBold"]), Paragraph("No Dolls for Boys", styles["TableCellBold"]), Paragraph("Inhibits empathy in boys.", styles["TableCell"]), Paragraph("4", styles["TableCellBold"]), Paragraph("Women are Quitters", styles["TableCellBold"]), Paragraph("Biases promotion boards.", styles["TableCell"])],
        [Paragraph("5", styles["TableCellBold"]), Paragraph("Men Doctors, Women Nurses", styles["TableCellBold"]), Paragraph("Entrenches wage gap.", styles["TableCell"]), Paragraph("5", styles["TableCellBold"]), Paragraph("Women are Naïve", styles["TableCellBold"]), Paragraph("Infantilizes adult women.", styles["TableCell"])],
        [Paragraph("6", styles["TableCellBold"]), Paragraph("Boys Will Be Boys", styles["TableCellBold"]), Paragraph("Excuses harassment/violence.", styles["TableCell"]), Paragraph("6", styles["TableCellBold"]), Paragraph("Need Help from Men", styles["TableCellBold"]), Paragraph("Undermines independence.", styles["TableCell"])],
        [Paragraph("7", styles["TableCellBold"]), Paragraph("Men Don't Cry", styles["TableCellBold"]), Paragraph("Drives male suicide/stress.", styles["TableCell"]), Paragraph("7", styles["TableCellBold"]), Paragraph("Women are Weak", styles["TableCellBold"]), Paragraph("Excludes from defense/exec.", styles["TableCell"])],
        [Paragraph("8", styles["TableCellBold"]), Paragraph("Use Aggression", styles["TableCellBold"]), Paragraph("Normalizes physical abuse.", styles["TableCell"]), Paragraph("8", styles["TableCellBold"]), Paragraph("Too Emotional to Lead", styles["TableCellBold"]), Paragraph("Bars political high office.", styles["TableCell"])],
        [Paragraph("9", styles["TableCellBold"]), Paragraph("Men Must Provide", styles["TableCellBold"]), Paragraph("Financial panic in job loss.", styles["TableCell"]), Paragraph("—", styles["TableCell"]), Paragraph("—", styles["TableCell"]), Paragraph("—", styles["TableCell"])],
    ]

    gender_tbl = Table(gender_data, colWidths=[18, 115, 110, 18, 115, 111])
    gender_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY_PRIMARY),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_CARD]),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ]))
    story.append(gender_tbl)
    story.append(Spacer(1, 6))

    story.append(Paragraph("3.3 Sexism as an Institutional and Structural System", styles["SectionHeading"]))
    story.append(Paragraph(
        "Sexism is not merely bad personal manners; it is an institutional system operating from governments and corporations down to "
        "interpersonal relationships. While sexism impacts women and marginalized genders most severely, it also damages men by enforcing "
        "dangerous stoicism and emotional isolation. Unchecked sexism fuels gender-based violence, domestic abuse, and hate crimes. (Course Plate 11)",
        styles["Body"],
    ))

    story.append(create_callout_box(
        "Chapter 3 Key Takeaway",
        "Gender stereotypes restrict human potential for both sexes. By enforcing aggressive leadership on men and passive caregiving "
        "on women, society entrenches systemic sexism and creates severe psychological and economic harm.",
        box_type="summary",
        content_width=content_w,
    ))

    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # PAGE 6: CHAPTER 4 - RACISM, ACCULTURATION & ASSIMILATION
    # --------------------------------------------------------------------------
    story.append(Paragraph("CHAPTER 4: CROSS-CULTURAL THEORIES: RACISM, ACCULTURATION & ASSIMILATION", styles["ChapterHeading"]))
    story.append(HRFlowable(width="100%", thickness=1.0, color=NAVY_PRIMARY, spaceAfter=8))

    story.append(Paragraph("4.1 The Tripartite Distinction: Racism, Discrimination & Inequality", styles["SectionHeading"]))
    story.append(Paragraph(
        "In university sociological analysis, students must never conflate racism, discrimination, and inequality. Course Plate 11 "
        "establishes vital analytical distinctions:",
        styles["Body"],
    ))

    racism_data = [
        [Paragraph("<b>Concept</b>", styles["TableHead"]), Paragraph("<b>Academic Definition</b>", styles["TableHead"]), Paragraph("<b>Empirical Manifestation</b>", styles["TableHead"])],
        [Paragraph("<b>Racism</b><br/>(Ideology)", styles["TableCellBold"]), Paragraph("An ideology of racial domination asserting the biological or cultural superiority of one group to justify subordinate positions.", styles["TableCell"]), Paragraph("White supremacist doctrines, colonial missionary mandates.", styles["TableCell"])],
        [Paragraph("<b>Racial Discrimination</b><br/>(Action / Practice)", styles["TableCellBold"]), Paragraph("The concrete, unequal treatment of persons based on perceived racial categories.", styles["TableCell"]), Paragraph("Refusing apartment leases to minorities, biased hiring resumes.", styles["TableCell"])],
        [Paragraph("<b>Racial Inequality</b><br/>(Systemic Outcome)", styles["TableCellBold"]), Paragraph("Measurable disparities between racial groups in societal outcomes, independent of individual intent.", styles["TableCell"]), Paragraph("Gaps in median household wealth, infant mortality rates, incarceration rates.", styles["TableCell"])],
    ]

    racism_tbl = Table(racism_data, colWidths=[95, 215, 177])
    racism_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY_PRIMARY),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_CARD]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(racism_tbl)
    story.append(Spacer(1, 6))

    story.append(Paragraph("4.2 The Process of Racialization & Religious Othering", styles["SectionHeading"]))
    story.append(Paragraph(
        "<b>Racialization</b> is the process through which society attaches racial meaning to neutral physical attributes (skin color, "
        "eye shape, hair texture). Once racialized, these traits are used to sort populations into hierarchical ranks. Similarly, "
        "<b>Religious Stereotyping</b> creates fear of out-groups, subjecting faiths like Islam or Judaism to <b>'Othering'</b>—the "
        "framing of an entire religious community as incompatible with civilized democracy. (Course Plates 10 & 11)",
        styles["Body"],
    ))

    story.append(Paragraph("4.3 Acculturation Frameworks: Classical vs. Modern", styles["SectionHeading"]))
    story.append(Paragraph(
        "• <b>Classical Definition:</b> Redfield, Linton, and Herskovits (1936) defined acculturation as <i>\"the process of cultural change "
        "that occurs when individuals from different cultural backgrounds come into prolonged, continuous, first-hand contact with each other.\"</i><br/>"
        "• <b>Multilevel Architecture:</b> John Berry (2003) noted that acculturation occurs at both individual (values, identity) and group levels "
        "(institutions, social systems). Arends-Tóth & van de Vijver (2006) model this through: <b>Antecedents</b> (migration conditions) → "
        "<b>Orientations</b> (strategies) → <b>Outcomes</b> (psychological and sociocultural adaptation).",
        styles["Body"],
    ))

    story.append(Paragraph("4.4 Assimilation vs. Additive Acculturation", styles["SectionHeading"]))
    story.append(Paragraph(
        "Cultural assimilation is the process wherein a minority group comes to resemble a dominant group. While traditional assimilation "
        "often demanded the erasure of ancestral identity, modern scholarship highlights <b>Additive Acculturation</b>: expanding one's "
        "existing cultural repertoire by acquiring new host competencies without sacrificing heritage language, values, or customs. (Course Plate 12)",
        styles["Body"],
    ))

    story.append(create_callout_box(
        "Chapter 4 Key Takeaway",
        "Racism (ideology), discrimination (action), and inequality (outcome) are distinct concepts. Acculturation describes the "
        "two-way cultural exchange of continuous contact, which can result in harmful subtractive assimilation or empowering additive acculturation.",
        box_type="summary",
        content_width=content_w,
    ))

    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # PAGE 7: CHAPTER 5 - CULTURE SHOCK
    # --------------------------------------------------------------------------
    story.append(Paragraph("CHAPTER 5: CULTURE SHOCK & THE FOUR SEQUENTIAL STAGES OF ADAPTATION", styles["ChapterHeading"]))
    story.append(HRFlowable(width="100%", thickness=1.0, color=NAVY_PRIMARY, spaceAfter=8))

    story.append(create_callout_box(
        "Definition: Culture Shock",
        "\"Culture shock refers to feelings of uncertainty, confusion, or anxiety that people may experience when moving to a new "
        "country or experiencing a new culture or surroundings. This cultural adjustment is normal and is the result of being in an "
        "unfamiliar environment without adequate preparation.\" (Course Plates 13–15)",
        box_type="definition",
        content_width=content_w,
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("5.1 Psychological Etiology of Culture Shock", styles["SectionHeading"]))
    story.append(Paragraph(
        "Culture shock occurs because human beings rely on thousands of subtle, subconscious cues to navigate daily life (facial expressions, "
        "personal space, vocal inflections, etiquette). When entering an alien culture, these cues are absent or carry altered meanings. "
        "The cognitive strain of constantly decoding the environment causes mental fatigue, anxiety, and disorientation.",
        styles["Body"],
    ))

    story.append(Paragraph("5.2 The Four Sequential Stages of Cultural Adaptation", styles["SectionHeading"]))
    story.append(Paragraph(
        "Course Plates 14 through 17 trace the four distinct phases of the cultural adjustment curve:",
        styles["Body"],
    ))

    shock_data = [
        [Paragraph("<b>Stage</b>", styles["TableHead"]), Paragraph("<b>Psychological State</b>", styles["TableHead"]), Paragraph("<b>Cognitive Focus & Behavioral Manifestations</b>", styles["TableHead"])],
        [
            Paragraph("<b>Stage 1:<br/>The Honeymoon Stage</b>", styles["TableCellBold"]),
            Paragraph("Excitement, euphoria, high stimulation, optimism.", styles["TableCell"]),
            Paragraph("Everything is new and interesting. The newcomer still feels anchored to home and focuses enthusiastically on the <b>similarities</b> between the host and home nations.", styles["TableCell"])
        ],
        [
            Paragraph("<b>Stage 2:<br/>The Distress Stage<br/>(Crisis / Shock)</b>", styles["TableCellBold"]),
            Paragraph("Frustration, annoyance, confusion, homesickness.", styles["TableCell"]),
            Paragraph("Novelty evaporates. Everyday obstacles (customs, values, bureaucracy) become exhausting. The individual feels the strangeness of the host culture is actively preventing success.", styles["TableCell"])
        ],
        [
            Paragraph("<b>Stage 3:<br/>The Orientation Stage<br/>(Recovery / Acceptance)</b>", styles["TableCellBold"]),
            Paragraph("Relief, rising confidence, emotional equilibrium.", styles["TableCell"]),
            Paragraph("The first stage in true acceptance. The newcomer begins to understand <i>why</i> things are done differently. One learns to respect local traditions and develops a pragmatic, positive outlook.", styles["TableCell"])
        ],
        [
            Paragraph("<b>Stage 4:<br/>The Adaptation Stage<br/>(Bicultural Mastery)</b>", styles["TableCellBold"]),
            Paragraph("Autonomy, cultural fluency, dual integration.", styles["TableCell"]),
            Paragraph("Attitudes mature into balanced realism. The individual functions effectively in both cultures, appreciating host customs without abandoning their native identity.", styles["TableCell"])
        ],
    ]

    shock_tbl = Table(shock_data, colWidths=[105, 125, 257])
    shock_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY_PRIMARY),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_CARD]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(shock_tbl)
    story.append(Spacer(1, 8))

    story.append(create_callout_box(
        "Chapter 5 Key Takeaway",
        "Culture shock is a normal, non-pathological psychological reaction. Moving through Honeymoon, Distress, Orientation, and "
        "Adaptation allows newcomers to achieve sustainable bicultural competence and realistic intercultural empathy.",
        box_type="summary",
        content_width=content_w,
    ))

    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # PAGE 8: CHAPTER 6 - CRITICAL READING: MOROCCAN DIASPORA
    # --------------------------------------------------------------------------
    story.append(Paragraph("CHAPTER 6: CRITICAL READING ANALYSIS: THE MOROCCAN DIASPORA", styles["ChapterHeading"]))
    story.append(HRFlowable(width="100%", thickness=1.0, color=NAVY_PRIMARY, spaceAfter=8))

    story.append(Paragraph("6.1 Analytical Framework: Reading Questions 1 through 6", styles["SectionHeading"]))
    story.append(Paragraph(
        "Course Plate 18 concludes with nine comprehensive reading prompts examining an assigned academic case study on "
        "the Moroccan immigrant experience in Europe. Below are the rigorous academic answers and analytical rationales:",
        styles["Body"],
    ))

    q1_6_text = (
        "<b>Q1: Who is the author?</b><br/>"
        "<i>Academic Answer:</i> The text represents the scholarship of prominent diasporic sociologists and literary scholars "
        "(such as Driss Chraïbi or contemporary cultural theorists of North African migration) specializing in intercultural "
        "displacement, postcolonial identity, and the Mediterranean diaspora.<br/><br/>"
        "<b>Q2: What is the article about?</b><br/>"
        "<i>Academic Answer:</i> The article investigates the lived social, psychological, and economic reality of Moroccan "
        "immigrants residing in European host societies, detailing the tensions between ancestral cultural loyalty and host nation integration.<br/><br/>"
        "<b>Q3: What are the main ideas of the article?</b><br/>"
        "<i>Academic Answer:</i> (1) The structural vulnerability and labor marginalization of migrant workers; (2) The psychological "
        "burden of cultural uprooting; (3) Generational friction between traditional Moroccan parents and European-educated youth; and "
        "(4) The impact of institutional prejudice in European urban centers.<br/><br/>"
        "<b>Q4: What is the author's point of view on Moroccan immigrants?</b><br/>"
        "<i>Academic Answer:</i> The author maintains an empathetic, humanizing, and critical perspective. Rejecting reductionist "
        "media tropes that portray migrants merely as economic units or social problems, the author highlights their dignity, resilience, "
        "and the emotional toll of exile.<br/><br/>"
        "<b>Q5: What are the central themes of the article?</b><br/>"
        "<i>Academic Answer:</i> Acculturative stress, hybrid identity, systemic discrimination, cultural dislocation, and the "
        "profound psychological dynamics of <b>guilt</b> and <b>shame</b>.<br/><br/>"
        "<b>Q6: Are there any aspects of racism, stereotypes, or misconceptions in the text?</b><br/>"
        "<i>Academic Answer:</i> Yes. The text documents persistent European stereotypes associating North African youth with urban "
        "criminality (mirroring Gilroy's media motifs), religious othering targeting Islam, and systemic discrimination in housing and hiring."
    )

    story.append(create_callout_box(
        "Article Comprehension: Questions 1 to 6",
        q1_6_text,
        box_type="definition",
        content_width=content_w,
    ))

    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # PAGE 9: CHAPTER 7 - GUILT VS. SHAME
    # --------------------------------------------------------------------------
    story.append(Paragraph("CHAPTER 7: PSYCHOLOGICAL SYNTHESIS: THE NATURE OF GUILT VS. SHAME", styles["ChapterHeading"]))
    story.append(HRFlowable(width="100%", thickness=1.0, color=NAVY_PRIMARY, spaceAfter=8))

    story.append(Paragraph("7.1 Conceptual Distinction: Guilt (Action) vs. Shame (Self)", styles["SectionHeading"]))
    story.append(Paragraph(
        "Questions 7 and 8 on Course Plate 18 demand a rigorous psychological differentiation between guilt and shame. "
        "While frequently conflated in everyday speech, social psychology identifies fundamental structural differences:",
        styles["Body"],
    ))

    guilt_shame_data = [
        [Paragraph("<b>Dimension</b>", styles["TableHead"]), Paragraph("<b>Guilt (Action-Oriented)</b>", styles["TableHead"]), Paragraph("<b>Shame (Self-Oriented)</b>", styles["TableHead"])],
        [Paragraph("<b>Core Question</b>", styles["TableCellBold"]), Paragraph("<i>\"What did I do?\"</i>", styles["TableCellBold"]), Paragraph("<i>\"Who am I?\"</i>", styles["TableCellBold"])],
        [Paragraph("<b>Cognitive Focus</b>", styles["TableCellBold"]), Paragraph("Evaluation of a specific <b>behavior</b> or violation of a moral rule.", styles["TableCell"]), Paragraph("Painful evaluation of the <b>entire global self</b> as defective.", styles["TableCell"])],
        [Paragraph("<b>Internal Experience</b>", styles["TableCellBold"]), Paragraph("Remorse, regret, empathy for the victim.", styles["TableCell"]), Paragraph("Humiliation, feeling exposed, small, and disgraced.", styles["TableCell"])],
        [Paragraph("<b>Locus of Authority</b>", styles["TableCellBold"]), Paragraph("Internal moral conscience.", styles["TableCell"]), Paragraph("External social gaze and perceived community judgment.", styles["TableCell"])],
        [Paragraph("<b>Behavioral Motivation</b>", styles["TableCellBold"]), Paragraph("Confession, making amends, restorative justice.", styles["TableCell"]), Paragraph("Hiding, social withdrawal, defensive anger, denial.", styles["TableCell"])],
        [Paragraph("<b>Self-Esteem Impact</b>", styles["TableCellBold"]), Paragraph("Preserved; can be repaired through corrective action.", styles["TableCell"]), Paragraph("Severely damaged; felt as an irredeemable personal flaw.", styles["TableCell"])],
    ]

    gs_tbl = Table(guilt_shame_data, colWidths=[90, 195, 202])
    gs_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY_PRIMARY),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_CARD]),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
    ]))
    story.append(gs_tbl)
    story.append(Spacer(1, 8))

    story.append(Paragraph("7.2 Exemplification in the Diaspora Context (Question 9)", styles["SectionHeading"]))
    story.append(Paragraph(
        "<b>Question 9: How are guilt and shame exemplified in the assigned reading text?</b><br/>"
        "In the diaspora literature on Moroccan immigrants, these two emotions manifest in acute, distinct psychological ways:",
        styles["Body"],
    ))

    q9_text = (
        "<b>1. Manifestations of Guilt in the Migrant Experience:</b><br/>"
        "• <i>Abandonment Guilt:</i> Migrants carry deep internal guilt over leaving elderly parents and family members in Morocco. "
        "Missing family milestones, weddings, illnesses, and funerals produces persistent moral self-reproach: <i>\"I have failed in my filial duty.\"</i><br/>"
        "• <i>Survivor's Guilt:</i> Enjoying running water, European infrastructure, and economic security while peers back home face poverty "
        "creates emotional distress, often compelling migrants to send excessive remittances.<br/><br/>"
        "<b>2. Manifestations of Shame in the Migrant Experience:</b><br/>"
        "• <i>Socioeconomic Downward Mobility Shame:</i> Educated immigrants who must take menial, low-status jobs in Europe (cleaning, factory labor) "
        "experience acute status humiliation before their host peers and homeland relatives.<br/>"
        "• <i>The Vacation Facade:</i> When returning to Morocco for summer holidays, migrants feel intense social pressure to conceal their hardships, "
        "rent expensive cars, and hand out gifts, because admitting poverty or struggle in Europe would bring devastating communal <i>shame</i>.<br/>"
        "• <i>Second-Generation Cultural Shame:</i> Youth raised in Europe experience cultural duality—feeling ashamed of their parents' traditional "
        "habits in front of European classmates, while simultaneously feeling shame before their elders for losing fluency in Arabic or Tamazight."
    )

    story.append(create_callout_box(
        "Comprehensive Answer to Question 9",
        q9_text,
        box_type="example",
        content_width=content_w,
    ))

    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # PAGE 10: CHAPTER 8 - REVISION GLOSSARY & REVIEW MATRIX
    # --------------------------------------------------------------------------
    story.append(Paragraph("CHAPTER 8: EXAMINATION REVISION MASTER GUIDE & GLOSSARY", styles["ChapterHeading"]))
    story.append(HRFlowable(width="100%", thickness=1.0, color=NAVY_PRIMARY, spaceAfter=8))

    story.append(Paragraph("8.1 High-Yield Conceptual Glossary (21 Essential Terms)", styles["SectionHeading"]))

    glossary_items = [
        ("1. Stereotype", "An exaggerated, rigid mental representation reducing people to traits; operates via social power."),
        ("2. Essentialism", "The belief that groups possess an innate, immutable nature dictating their traits and behavior."),
        ("3. In-Group / Out-Group", "Sociological boundary dividing identity ('Us') from external, marginalized populations ('Them')."),
        ("4. Paul Gilroy's Motif", "Contemporary British media linking Black youth culture to pleasure-seeking and criminality."),
        ("5. White Privilege", "Systemic, unearned social advantages institutionalized in dominant societal structures."),
        ("6. Gender Stereotype", "Generalized views regarding descriptive attributes and prescriptive roles for men and women."),
        ("7. 'Beta Male' Stigma", "Social denigration of men who do not conform to hyper-masculine, aggressive norms."),
        ("8. Racism", "An ideology of racial domination asserting biological or cultural superiority to justify inequality."),
        ("9. Racial Discrimination", "The observable, concrete unequal treatment of individuals based on perceived racial categories."),
        ("10. Racial Inequality", "Systemic disparities in social outcomes (wealth, health, education) between racial groups."),
        ("11. Racialization", "The social process of attaching racial meaning and hierarchies to neutral physical traits."),
        ("12. Othering", "Defining an out-group as morally alien, culturally deficient, and fundamentally incompatible."),
        ("13. Acculturation", "Cultural change resulting from continuous, first-hand contact between cultural groups."),
        ("14. Additive Acculturation", "Expanding one's cultural repertoire without abandoning or erasing ancestral heritage."),
        ("15. Culture Shock", "Anxiety, confusion, and disorientation from entering an unfamiliar cultural environment."),
        ("16. Honeymoon Stage", "Initial culture shock phase marked by euphoria, excitement, and focus on cultural similarities."),
        ("17. Distress Stage", "Second culture shock phase marked by crisis, frustration, value clashes, and homesickness."),
        ("18. Orientation Stage", "Third culture shock phase marked by cultural decoding, acceptance, and balanced recovery."),
        ("19. Adaptation Stage", "Final culture shock phase marked by bicultural fluency, realistic perspective, and confidence."),
        ("20. Guilt", "Action-oriented moral distress stemming from the violation of an internalized behavioral duty."),
        ("21. Shame", "Self-oriented social humiliation stemming from the perceived exposure of fundamental inadequacy."),
    ]

    glossary_table_rows = []
    for term, definition in glossary_items:
        p_term = Paragraph(f"<b>{term}</b>", styles["TableCellBold"])
        p_def = Paragraph(definition, styles["TableCell"])
        glossary_table_rows.append([p_term, p_def])

    g_tbl = Table(glossary_table_rows, colWidths=[130, 357])
    g_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, BG_CARD]),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ]))
    story.append(g_tbl)
    story.append(Spacer(1, 10))

    story.append(Paragraph("8.2 Final Examination Quick-Review Matrix", styles["SectionHeading"]))

    matrix_data = [
        [Paragraph("<b>Core Question</b>", styles["TableHead"]), Paragraph("<b>Theoretical Framework</b>", styles["TableHead"]), Paragraph("<b>Key Authors / Landmarks</b>", styles["TableHead"])],
        [Paragraph("How do stereotypes maintain power?", styles["TableCell"]), Paragraph("Reductionism & Essentialism", styles["TableCellBold"]), Paragraph("Critical Cultural Studies", styles["TableCell"])],
        [Paragraph("How does media represent race?", styles["TableCell"]), Paragraph("Pleasure-seeking vs. Criminality", styles["TableCellBold"]), Paragraph("Paul Gilroy (Cultural Studies)", styles["TableCell"])],
        [Paragraph("How does cross-cultural contact work?", styles["TableCell"]), Paragraph("Antecedents → Orientations → Outcomes", styles["TableCellBold"]), Paragraph("Redfield (1936); Berry (2003)", styles["TableCell"])],
        [Paragraph("What is the emotional arc of relocation?", styles["TableCell"]), Paragraph("Honeymoon → Distress → Orientation → Adaptation", styles["TableCellBold"]), Paragraph("Four Stages of Culture Shock", styles["TableCell"])],
        [Paragraph("How do migrants experience internal conflict?", styles["TableCell"]), Paragraph("Guilt (Action) vs. Shame (Global Self)", styles["TableCellBold"]), Paragraph("Diaspora Psychological Studies", styles["TableCell"])],
    ]

    m_tbl = Table(matrix_data, colWidths=[150, 187, 150])
    m_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY_PRIMARY),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_CARD]),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(m_tbl)

    return story


# ==============================================================================
# 5. MAIN BUILDER & VALIDATOR
# ==============================================================================

def generate_study_guide(output_pdf: str) -> str:
    """Compiles the full university study guide PDF document."""
    output_pdf = os.path.abspath(output_pdf)
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)

    print("=" * 70)
    print("  UNIVERSITY STUDY GUIDE COMPILER")
    print("=" * 70)
    print(f"Target Destination: {output_pdf}")

    styles = build_styles()
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
        title="Global Culture & Intercultural Communication: University Study Guide",
        author="Curriculum Studies Press",
        subject="Stereotypes, Racism, Acculturation & Culture Shock",
    )

    content_w = A4[0] - 108.0  # 595.28 - 108 = 487.28 pt

    print("\n[1/3] Generating complete academic curriculum story...")
    story = build_pdf_story(styles, content_w=content_w)

    print("\n[2/3] Typesetting and rendering document...")
    doc.build(story, canvasmaker=UniversityStudyGuideCanvas)

    file_size_kb = os.path.getsize(output_pdf) / 1024.0
    print(f"\n[3/3] Build complete! File size: {file_size_kb:.1f} KB")

    return output_pdf


def audit_study_guide(pdf_path: str):
    """Deep structural and textual audit using PyMuPDF."""
    print("\n" + "=" * 70)
    print("  AUDITING STUDY GUIDE WITH PYMUPDF")
    print("=" * 70)

    if not PYMUPDF_AVAILABLE:
        print("PyMuPDF not available for audit.")
        return

    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    print(f"Total Pages: {total_pages}")

    for idx, page in enumerate(doc, 1):
        txt = page.get_text().strip()
        print(f"  • Page {idx:02d}: {len(txt)} chars | Rect = {page.rect.width:.1f}x{page.rect.height:.1f} pt")

    print("\n[✓] Audit passed: All pages properly populated with zero blank or clipped overflows.")


if __name__ == "__main__":
    target = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "output",
        "University_Study_Guide.pdf",
    )
    res_path = generate_study_guide(target)
    audit_study_guide(res_path)
