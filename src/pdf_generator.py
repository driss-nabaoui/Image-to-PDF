"""
================================================================================
  PREMIUM PDF TYPESETTING ENGINE (src/pdf_generator.py)
================================================================================
  Generates a high-quality, publication-grade academic university study guide
  in A4 format using ReportLab Platypus, custom NumberedCanvas, and visual
  distinction styling (Blue Explanations, Green Answers, Gold Definitions).
================================================================================
"""

import os
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime

# ReportLab core imports
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
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
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY


# ==============================================================================
# 1. NUMBERED CANVAS WITH DYNAMIC TWO-PASS RUNNING HEADERS & FOOTERS
# ==============================================================================

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas that computes exact total page count,
    rendering professional running headers, dividers, and footers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_elements(num_pages)
            super().showPage()
        super().save()

    def draw_page_elements(self, total_pages: int):
        # Page 1 is the cover page; omit running header and footer
        if self._pageNumber == 1:
            return

        page_w, page_h = A4
        margin_x = 42.0
        header_y = page_h - 38.0
        footer_y = 38.0

        # Running Header
        self.saveState()
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(margin_x, header_y + 4, "READING IN GLOBAL CULTURE • UNIVERSITY STUDY GUIDE")
        self.drawRightString(page_w - margin_x, header_y + 4, "DR. PHILIP HERMANS (1999)")

        # Header Hairline Divider
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(margin_x, header_y, page_w - margin_x, header_y)

        # Footer Hairline Divider
        self.line(margin_x, footer_y + 12, page_w - margin_x, footer_y + 12)

        # Running Footer
        self.setFont("Helvetica", 8.0)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(
            margin_x,
            footer_y,
            "Academic Research & Intercultural Education Suite • Archival Study Guide",
        )
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(page_w - margin_x, footer_y, page_str)
        self.restoreState()


# ==============================================================================
# 2. DOCUMENT STYLESHEET INITIALIZATION
# ==============================================================================

def create_document_stylesheet() -> Dict[str, ParagraphStyle]:
    """Builds a comprehensive, publication-grade academic typography system."""
    base_styles = getSampleStyleSheet()

    custom_styles = {
        # Document Cover Styles
        "CoverKicker": ParagraphStyle(
            "CoverKicker",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor("#D97706"), # Academic amber
            alignment=TA_LEFT,
            spaceAfter=14,
        ),
        "CoverTitle": ParagraphStyle(
            "CoverTitle",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=24.0,
            leading=29.0,
            textColor=colors.HexColor("#0F172A"),
            alignment=TA_LEFT,
            spaceAfter=12,
        ),
        "CoverSubtitle": ParagraphStyle(
            "CoverSubtitle",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=11.5,
            leading=16.0,
            textColor=colors.HexColor("#334155"),
            alignment=TA_LEFT,
            spaceAfter=20,
        ),
        "CoverAuthor": ParagraphStyle(
            "CoverAuthor",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10.0,
            leading=14.0,
            textColor=colors.HexColor("#1E3A8A"), # Academic Navy
            alignment=TA_LEFT,
        ),
        "CoverMeta": ParagraphStyle(
            "CoverMeta",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=12.0,
            textColor=colors.HexColor("#64748B"),
            alignment=TA_LEFT,
        ),

        # Headings
        "ChapterNumber": ParagraphStyle(
            "ChapterNumber",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.0,
            leading=12.0,
            textColor=colors.HexColor("#1E3A8A"),
            spaceBefore=12,
            spaceAfter=3,
        ),
        "ChapterHeading": ParagraphStyle(
            "ChapterHeading",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=15.0,
            leading=19.0,
            textColor=colors.HexColor("#0F172A"),
            spaceBefore=0,
            spaceAfter=8,
            keepWithNext=True,
        ),
        "SectionHeading": ParagraphStyle(
            "SectionHeading",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=11.5,
            leading=15.0,
            textColor=colors.HexColor("#1E3A8A"),
            spaceBefore=10,
            spaceAfter=4,
            keepWithNext=True,
        ),
        "SubsectionHeading": ParagraphStyle(
            "SubsectionHeading",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10.0,
            leading=13.0,
            textColor=colors.HexColor("#334155"),
            spaceBefore=8,
            spaceAfter=3,
            keepWithNext=True,
        ),

        # Body text
        "AcademicBody": ParagraphStyle(
            "AcademicBody",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=9.2,
            leading=13.5,
            textColor=colors.HexColor("#1E293B"),
            alignment=TA_JUSTIFY,
            spaceAfter=7,
        ),
        "AcademicCitation": ParagraphStyle(
            "AcademicCitation",
            parent=base_styles["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=8.5,
            leading=12.0,
            textColor=colors.HexColor("#475569"),
            leftIndent=14,
            rightIndent=14,
            spaceBefore=4,
            spaceAfter=8,
        ),

        # Table Styles
        "TableHead": ParagraphStyle(
            "TableHead",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.5,
            leading=11.0,
            textColor=colors.white,
            alignment=TA_LEFT,
        ),
        "TableCell": ParagraphStyle(
            "TableCell",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=8.2,
            leading=11.5,
            textColor=colors.HexColor("#1E293B"),
            alignment=TA_LEFT,
        ),
        "TableCellBold": ParagraphStyle(
            "TableCellBold",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.2,
            leading=11.5,
            textColor=colors.HexColor("#0F172A"),
            alignment=TA_LEFT,
        ),

        # Callout Titles & Bodies
        "BlueBoxTitle": ParagraphStyle(
            "BlueBoxTitle",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.5,
            leading=13.0,
            textColor=colors.HexColor("#0369A1"),
            spaceAfter=4,
        ),
        "BlueBoxBody": ParagraphStyle(
            "BlueBoxBody",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=8.8,
            leading=12.8,
            textColor=colors.HexColor("#0F172A"),
            alignment=TA_LEFT,
            spaceAfter=4,
        ),
        "BlueBoxExampleTitle": ParagraphStyle(
            "BlueBoxExampleTitle",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.2,
            leading=11.0,
            textColor=colors.HexColor("#0284C7"),
            spaceBefore=3,
            spaceAfter=2,
        ),
        "BlueBoxExampleBody": ParagraphStyle(
            "BlueBoxExampleBody",
            parent=base_styles["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=8.2,
            leading=11.8,
            textColor=colors.HexColor("#334155"),
            spaceAfter=2,
        ),

        # Green Answer Box Styles
        "GreenBoxTitle": ParagraphStyle(
            "GreenBoxTitle",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.5,
            leading=13.0,
            textColor=colors.HexColor("#15803D"),
            spaceAfter=4,
        ),
        "GreenQuestionText": ParagraphStyle(
            "GreenQuestionText",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.0,
            leading=12.5,
            textColor=colors.HexColor("#0F172A"),
            spaceAfter=4,
        ),
        "GreenBoxBody": ParagraphStyle(
            "GreenBoxBody",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=8.8,
            leading=12.8,
            textColor=colors.HexColor("#1E293B"),
            spaceAfter=4,
        ),
        "GreenWhyTitle": ParagraphStyle(
            "GreenWhyTitle",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.2,
            leading=11.0,
            textColor=colors.HexColor("#16A34A"),
            spaceBefore=3,
            spaceAfter=2,
        ),
        "GreenWhyBody": ParagraphStyle(
            "GreenWhyBody",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=8.2,
            leading=11.8,
            textColor=colors.HexColor("#334155"),
            spaceAfter=2,
        ),

        # Gold Alert Styles
        "GoldBoxTitle": ParagraphStyle(
            "GoldBoxTitle",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.5,
            leading=13.0,
            textColor=colors.HexColor("#B45309"),
            spaceAfter=4,
        ),
        "GoldBoxBody": ParagraphStyle(
            "GoldBoxBody",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=8.8,
            leading=12.8,
            textColor=colors.HexColor("#0F172A"),
            spaceAfter=3,
        ),

        # Summary Checklist Styles
        "SummaryTitle": ParagraphStyle(
            "SummaryTitle",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.5,
            leading=13.0,
            textColor=colors.HexColor("#1E3A8A"),
            spaceAfter=4,
        ),
        "SummaryBullet": ParagraphStyle(
            "SummaryBullet",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=12.0,
            textColor=colors.HexColor("#334155"),
            leftIndent=12,
            spaceAfter=2,
        ),
    }

    return custom_styles


# ==============================================================================
# 3. CALLOUT BOX GENERATOR (BLUE, GREEN, GOLD, SLATE)
# ==============================================================================

def create_callout_box(
    flowables_inside: List[Any],
    box_type: str = "blue",
    content_width: float = 511.0,
) -> Table:
    """
    Renders a beautifully padded callout card container with distinct color branding:
    - 'blue'  : Simple Explanation Box (#F0F9FF bg, #0284C7 border)
    - 'green' : Model Answer Box (#F0FDF4 bg, #16A34A border)
    - 'gold'  : Important Concept / Alert (#FEF3C7 bg, #D97706 border)
    - 'slate' : What You Should Remember (#F8FAFC bg, #64748B border)
    """
    palette_map = {
        "blue": {
            "bg": colors.HexColor("#F0F9FF"),
            "border": colors.HexColor("#0284C7"),
            "bar": colors.HexColor("#0369A1"),
        },
        "green": {
            "bg": colors.HexColor("#F0FDF4"),
            "border": colors.HexColor("#16A34A"),
            "bar": colors.HexColor("#15803D"),
        },
        "gold": {
            "bg": colors.HexColor("#FEF3C7"),
            "border": colors.HexColor("#D97706"),
            "bar": colors.HexColor("#B45309"),
        },
        "slate": {
            "bg": colors.HexColor("#F8FAFC"),
            "border": colors.HexColor("#64748B"),
            "bar": colors.HexColor("#1E3A8A"),
        },
    }

    cfg = palette_map.get(box_type, palette_map["blue"])

    # Table wrapping the internal flowables
    data = [[flowables_inside]]
    tbl = Table(data, colWidths=[content_width])
    tbl.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), cfg["bg"]),
            ("BOX", (0, 0), (-1, -1), 0.75, cfg["border"]),
            ("LINELEFT", (0, 0), (0, -1), 3.5, cfg["bar"]), # Left accent band
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LEFTPADDING", (0, 0), (-1, -1), 11),
            ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ])
    )
    return tbl


# ==============================================================================
# 4. MASTER DOCUMENT BUILDER PIPELINE
# ==============================================================================

def generate_study_guide_pdf(
    corpus: Dict[str, Any],
    explanations: List[Dict[str, Any]],
    qa_list: List[Dict[str, Any]],
    output_pdf_path: str = "output/Complete_University_Study_Guide.pdf",
    new_lecture_qa: Optional[List[Dict[str, Any]]] = None,
    homework_task: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Compiles the complete academic study guide into a publication-grade PDF.
    Supports optional Chapter 10 for lecture questions and homework synthesis.
    """
    print(f"\n[4/4] Typesetting study guide PDF via ReportLab Platypus -> '{output_pdf_path}'...")
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)

    page_w, page_h = A4
    margin_x = 42.0
    margin_y = 48.0
    content_w = page_w - (2 * margin_x)

    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=margin_x,
        rightMargin=margin_x,
        topMargin=margin_y,
        bottomMargin=margin_y,
    )

    styles = create_document_stylesheet()
    story: List[Any] = []

    # ==========================================================================
    # PAGE 1: EXECUTIVE UNIVERSITY TEXTBOOK COVER
    # ==========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("ACADEMIC CURRICULUM SERIES • ADVANCED READING IN GLOBAL CULTURE", styles["CoverKicker"]))
    story.append(Paragraph("INTERSECTION OF CULTURES & MOROCCAN IMMIGRANTS", styles["CoverTitle"]))
    story.append(
        Paragraph(
            "An Empirical & Anthropological Analysis of Acculturation, Schooling, "
            "and the Emotional Repertoires of Shame and Guilt",
            styles["CoverSubtitle"],
        )
    )

    # Accent decorative dual-tone band
    bar_tbl = Table([[""]], colWidths=[content_w], rowHeights=[4.0])
    bar_tbl.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#1E3A8A")),
            ("LINELEFT", (0, 0), (0, 0), content_w * 0.35, colors.HexColor("#D97706")),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ])
    )
    story.append(bar_tbl)
    story.append(Spacer(1, 20))

    # Executive Overview Card on Cover
    cover_card_content = [
        Paragraph("<b>COURSE ARCHIVE OVERVIEW & PEDAGOGICAL SPECIFICATIONS</b>", styles["BlueBoxTitle"]),
        Spacer(1, 3),
        Paragraph(
            "This comprehensive university textbook guide extracts, synthesizes, and explains the seminal empirical study by "
            "<b>Dr. Philip Hermans</b> (<i>International Journal of Educational Research</i>, 31, pp. 303–316). "
            "It is engineered specifically for university examination preparation, combining three parallel pedagogical tiers: "
            "(1) Faithful Original Academic Text, (2) Simple English Conceptual Breakdowns, and (3) Complete Model Examination Answers.",
            styles["AcademicBody"],
        ),
        Spacer(1, 4),
        Paragraph("<b>CORE CURRICULAR DOMAINS COVERED:</b>", styles["SubsectionHeading"]),
        Paragraph("• Historical, legal, and demographic roots of the Moroccan diaspora in Belgium (1964–Present).", styles["SummaryBullet"]),
        Paragraph("• Anthropological definitions separating public shame (Hshuma) from internalized guilt (Dhenb).", styles["SummaryBullet"]),
        Paragraph("• Critical refutation of Western deficit models and the ethnocentric distortion of Jean Piaget.", styles["SummaryBullet"]),
        Paragraph("• Thematic Apperception Test (TAT) empirical methodology across 70 Moroccan male adolescents.", styles["SummaryBullet"]),
        Paragraph("• Quantitative analysis of Tables 1 & 2: Proving the existence of deep moral conscience and remorse.", styles["SummaryBullet"]),
        Paragraph("• The Dialectic of the Gaze: How external shame acts as a catalyst activating internal conscience.", styles["SummaryBullet"]),
    ]
    story.append(create_callout_box(cover_card_content, box_type="blue", content_width=content_w))
    story.append(Spacer(1, 24))

    # 4-Column Metadata Grid
    meta_table_data = [
        [
            Paragraph("<b>PRIMARY RESEARCHER:</b><br/>Dr. Philip Hermans<br/>Univ. of Leuven / Groningen", styles["TableCell"]),
            Paragraph("<b>PUBLICATION OUTLET:</b><br/>Int. J. of Educational Res.<br/>Pergamon / Elsevier Science", styles["TableCell"]),
            Paragraph("<b>SOURCE MATERIALS:</b><br/>13 Archival Plates (Verified)<br/>Pages 303–316 Complete", styles["TableCell"]),
            Paragraph("<b>ACADEMIC STANDARD:</b><br/>A4 Print & HD Digital<br/>Two-Pass Dynamic Verified", styles["TableCell"]),
        ]
    ]
    meta_tbl = Table(meta_table_data, colWidths=[content_w / 4.0] * 4)
    meta_tbl.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ])
    )
    story.append(meta_tbl)
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 2: TABLE OF CONTENTS & VISUAL DISTINCTION SYSTEM
    # ==========================================================================
    story.append(Paragraph("TABLE OF CONTENTS & COURSE ROADMAP", styles["ChapterHeading"]))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=8))

    toc_data = [
        [Paragraph("<b>Curriculum Chapter</b>", styles["TableHead"]), Paragraph("<b>Core Subject Matter & Empirical Focus</b>", styles["TableHead"])],
        [Paragraph("<b>Chapter 1</b>", styles["TableCellBold"]), Paragraph("Historical & Demographic Background of Moroccan Labor Migration in Belgium", styles["TableCell"])],
        [Paragraph("<b>Chapter 2</b>", styles["TableCellBold"]), Paragraph("Psychological & Anthropological Foundations: The Taxonomy of Shame vs. Guilt", styles["TableCell"])],
        [Paragraph("<b>Chapter 3</b>", styles["TableCellBold"]), Paragraph("Western Professional Stereotypes & The Ethnocentric Distortion of Jean Piaget", styles["TableCell"])],
        [Paragraph("<b>Chapter 4</b>", styles["TableCellBold"]), Paragraph("Empirical Research Methodology: The Cross-Cultural Thematic Apperception Test (TAT)", styles["TableCell"])],
        [Paragraph("<b>Chapter 5</b>", styles["TableCellBold"]), Paragraph("Empirical Evidence & Quantitative Findings: Tables 1 & 2 (Disproving Deficit Myths)", styles["TableCell"])],
        [Paragraph("<b>Chapter 6</b>", styles["TableCellBold"]), Paragraph("Linguistic & Cultural Codification: The Moroccan Concepts of 'Hshuma' and 'Dhenb'", styles["TableCell"])],
        [Paragraph("<b>Chapter 7</b>", styles["TableCellBold"]), Paragraph("Sociostructural Realities & Intercultural Pedagogical Reforms for Schools", styles["TableCell"])],
        [Paragraph("<b>Chapter 8</b>", styles["TableCellBold"]), Paragraph("Comprehensive Academic Examination: 12 Questions & Green Model Answers", styles["TableCell"])],
        [Paragraph("<b>Chapter 9</b>", styles["TableCellBold"]), Paragraph("Master Revision Guide & High-Yield Conceptual Glossary (20 Core Terms)", styles["TableCell"])],
    ]
    if new_lecture_qa:
        toc_data.append(
            [Paragraph("<b>Chapter 10</b>", styles["TableCellBold"]), Paragraph("Professor's Lecture Questions (Q1–9) & Homework Curricular Synthesis", styles["TableCell"])]
        )

    toc_tbl = Table(toc_data, colWidths=[content_w * 0.22, content_w * 0.78])
    toc_tbl.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ])
    )
    story.append(toc_tbl)
    story.append(Spacer(1, 10))

    # Visual System Legend Card
    legend_content = [
        Paragraph("<b>HOW TO USE THIS STUDY BOOK: VISUAL SYSTEM LEGEND</b>", styles["GoldBoxTitle"]),
        Spacer(1, 2),
        Paragraph(
            "To guarantee effortless examination revision and eliminate confusion between original literature and study aids, "
            "this book strictly enforces a color-coded visual hierarchy throughout:",
            styles["AcademicBody"],
        ),
        Paragraph("• <b>ORIGINAL ACADEMIC TEXT (Dark Charcoal / Serif):</b> Direct quotes, research findings, and statistics from Dr. Hermans.", styles["SummaryBullet"]),
        Paragraph("• <b>BLUE CALLOUT BOXES (Simple Explanations):</b> Plain English breakdowns, real-life analogies, and concept simplifications.", styles["SummaryBullet"]),
        Paragraph("• <b>GREEN CALLOUT BOXES (Model Answers):</b> University-level examination answers with full pedagogical justifications.", styles["SummaryBullet"]),
        Paragraph("• <b>GOLD CALLOUT BOXES (Core Definitions):</b> High-yield theoretical concepts that frequently appear on midterm and final exams.", styles["SummaryBullet"]),
    ]
    story.append(create_callout_box(legend_content, box_type="gold", content_width=content_w))
    story.append(PageBreak())

    # ==========================================================================
    # CHAPTERS 1 THROUGH 7: CONTENT + BLUE EXPLANATIONS + SUMMARIES
    # ==========================================================================
    exp_by_chapter = {item["chapter_id"]: item for item in explanations}

    for ch in corpus["chapters"]:
        ch_id = ch["chapter_id"]
        story.append(Paragraph(f"CHAPTER {ch_id:02d}", styles["ChapterNumber"]))
        story.append(Paragraph(ch["title"].upper(), styles["ChapterHeading"]))
        story.append(Paragraph(f"<b>Source Document:</b> <i>{ch['source_plate']}</i>", styles["CoverMeta"]))
        story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor("#1E3A8A"), spaceBefore=3, spaceAfter=10))

        # Render original content sections
        for sec in ch["sections"]:
            story.append(Paragraph(sec["heading"], styles["SectionHeading"]))
            story.append(Paragraph(sec["content"], styles["AcademicBody"]))
            story.append(Spacer(1, 4))

        # Render Simple English Explanation Box for this Chapter
        ch_exp = exp_by_chapter.get(ch_id)
        if ch_exp:
            story.append(Spacer(1, 4))
            for item in ch_exp["explanations"]:
                box_items = [
                    Paragraph(f"<b>SIMPLE EXPLANATION: {item['concept'].upper()}</b>", styles["BlueBoxTitle"]),
                    Spacer(1, 2),
                    Paragraph(item["simple_text"], styles["BlueBoxBody"]),
                    Spacer(1, 2),
                    Paragraph("<b>💡 PRACTICAL REAL-WORLD EXAMPLE:</b>", styles["BlueBoxExampleTitle"]),
                    Paragraph(item["practical_example"], styles["BlueBoxExampleBody"]),
                    Spacer(1, 2),
                    Paragraph(f"<b>WHY THIS MATTERS:</b> {item['why_it_matters']}", styles["BlueBoxExampleBody"]),
                ]
                story.append(create_callout_box(box_items, box_type="blue", content_width=content_w))
                story.append(Spacer(1, 8))

            # End of Chapter Review Box
            summary_items = [
                Paragraph("<b>🧠 WHAT YOU SHOULD REMEMBER FROM THIS CHAPTER</b>", styles["SummaryTitle"]),
                Spacer(1, 2),
            ]
            for pt in ch_exp["what_to_remember"]:
                summary_items.append(Paragraph(f"• {pt}", styles["SummaryBullet"]))
            story.append(create_callout_box(summary_items, box_type="slate", content_width=content_w))

        story.append(PageBreak())

    # ==========================================================================
    # CHAPTER 8: COMPREHENSIVE EXAMINATION QUESTIONS & GREEN MODEL ANSWERS
    # ==========================================================================
    story.append(Paragraph("CHAPTER 08", styles["ChapterNumber"]))
    story.append(Paragraph("COMPREHENSIVE EXAMINATION QUESTIONS & MODEL ANSWERS", styles["ChapterHeading"]))
    story.append(Paragraph("<b>Assessment Format:</b> 12 Multi-Dimensional University Examination Prompts", styles["CoverMeta"]))
    story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor("#16A34A"), spaceBefore=3, spaceAfter=12))

    for item in qa_list:
        q_box = [
            Paragraph(f"<b>EXAMINATION QUESTION {item['question_id']:02d} (Chapter {item['chapter_id']})</b>", styles["GreenQuestionText"]),
            Spacer(1, 2),
            Paragraph(f"<i>\"{item['question']}\"</i>", styles["AcademicBody"]),
            Spacer(1, 4),
            Paragraph("<b>✅ MODEL ANSWER:</b>", styles["GreenBoxTitle"]),
            Paragraph(item["model_answer"], styles["GreenBoxBody"]),
            Spacer(1, 3),
            Paragraph("<b>🔍 WHY IS THIS THE ANSWER?</b>", styles["GreenWhyTitle"]),
            Paragraph(item["why_is_this_the_answer"], styles["GreenWhyBody"]),
            Spacer(1, 2),
            Paragraph("<b>💡 APPLIED EXAMPLE:</b>", styles["GreenWhyTitle"]),
            Paragraph(item["practical_example"], styles["GreenWhyBody"]),
        ]
        story.append(create_callout_box(q_box, box_type="green", content_width=content_w))
        story.append(Spacer(1, 10))

    story.append(PageBreak())

    # ==========================================================================
    # CHAPTER 9: MASTER REVISION GUIDE & GLOSSARY
    # ==========================================================================
    story.append(Paragraph("CHAPTER 09", styles["ChapterNumber"]))
    story.append(Paragraph("MASTER EXAMINATION REVISION GUIDE & CONCEPTUAL GLOSSARY", styles["ChapterHeading"]))
    story.append(Paragraph("<b>Review Module:</b> High-Yield Principles and Definitions for Final Examination", styles["CoverMeta"]))
    story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor("#1E3A8A"), spaceBefore=3, spaceAfter=12))

    # Core Principles Table
    principles_data = [
        [Paragraph("<b>High-Yield Principle</b>", styles["TableHead"]), Paragraph("<b>Core Examination Takeaway & Scientific Justification</b>", styles["TableHead"])],
        [Paragraph("<b>1. Economic Nature of Migration</b>", styles["TableCellBold"]), Paragraph("Moroccan migration was actively initiated by bilateral treaties to solve Western industrial labor shortages, disproving xenophobic narratives of sudden illegal arrival.", styles["TableCell"])],
        [Paragraph("<b>2. Shame vs. Guilt Taxonomy</b>", styles["TableCellBold"]), Paragraph("Shame involves external surveillance, audience spectators, and whole-self defect; guilt involves internalized conscience, injured victims, and reparative restitution.", styles["TableCell"])],
        [Paragraph("<b>3. Fallacy of the Deficit Model</b>", styles["TableCellBold"]), Paragraph("Early Western theorists committed ethnocentric bias by assuming Mediterranean honor cultures lack guilt. Direct empirical testing completely refutes this claim.", styles["TableCell"])],
        [Paragraph("<b>4. Weaponized Developmental Psychology</b>", styles["TableCellBold"]), Paragraph("Belgian counselors ethnocentrically abused Jean Piaget's childhood heteronomous vs. autonomous stages to claim immigrant adults have child-like morality.", styles["TableCell"])],
        [Paragraph("<b>5. The TAT Empirical Triumph</b>", styles["TableCellBold"]), Paragraph("Table 1 and Table 2 provide quantitative and verbatim proof that over 68% of Moroccan youth express internal moral agony, tears, and guilt.", styles["TableCell"])],
        [Paragraph("<b>6. Filial Relational Morality</b>", styles["TableCellBold"]), Paragraph("Moral conscience in collectivist contexts is mediated through deep love and responsibility toward parents, particularly maternal tears and fatherly dignity.", styles["TableCell"])],
        [Paragraph("<b>7. Semantic Depth of Hshuma</b>", styles["TableCellBold"]), Paragraph("Hshuma is not humiliation; it is a vital social code of decency, modesty, and discretion. Dhenb and Ndam provide religious vocabulary for guilt and remorse.", styles["TableCell"])],
        [Paragraph("<b>8. The Dialectic of the Gaze</b>", styles["TableCellBold"]), Paragraph("External shame acts as the psychological mirror that turns the offender's attention inward to activate conscience and stimulate moral restitution.", styles["TableCell"])],
    ]
    principle_tbl = Table(principles_data, colWidths=[content_w * 0.30, content_w * 0.70])
    principle_tbl.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ])
    )
    story.append(principle_tbl)
    story.append(Spacer(1, 14))

    # Comprehensive Glossary of 20 Core Terms
    story.append(Paragraph("20 HIGH-YIELD ACADEMIC GLOSSARY TERMS", styles["SectionHeading"]))
    glossary_data = [
        ("Acculturation", "The dual-process of cultural and psychological change that results following continuous contact between distinct cultural groups."),
        ("Autonomous Morality", "Piaget's advanced stage where morality is based on internal conscience, mutual respect, and reciprocal human empathy."),
        ("Bilateral Labor Treaty", "A formal diplomatic pact signed between two sovereign states governing the recruitment and migration of manual workers (e.g., Belgium-Morocco 1964)."),
        ("Deficit Model", "A flawed pedagogical framework that attributes educational disparities to presumed cultural or moral shortcomings within minority families."),
        ("Dhenb (ذنب)", "The Moroccan Arabic and Islamic theological concept for sin, moral transgression against divine balance, and internal spiritual guilt."),
        ("Dialectic of the Gaze", "Dr. Hermans' formulation explaining how external social surveillance forces the individual to turn inward and confront conscience."),
        ("Educational Tracking", "The institutional sorting of students into separate academic vs. vocational streams based on early test scores or teacher perceptions."),
        ("Fdiha (فضيحة)", "Public exposure and collective disgrace that causes an individual and their entire family lineage to lose social face."),
        ("Filial Obligation", "The moral, emotional, and social duty of children to respect, honor, and emotionally support their parents throughout life."),
        ("Guest Worker (Gastarbeiter)", "The post-WWII policy concept falsely assuming foreign laborers would work temporarily without establishing permanent families."),
        ("Heteronomous Morality", "Piaget's early childhood stage where rules are obeyed strictly due to fear of external punishment from powerful adults."),
        ("Hshuma (حشومة)", "A comprehensive Moroccan cultural code signifying propriety, modesty, discretion, decency, and respect for social boundaries."),
        ("Hshumiya", "The character trait of being well-bred, polite, modest, and socially considerate of other people's dignity."),
        ("Loss of Face", "The acute psychological and social trauma of having one's private moral failing publicly exposed before the community."),
        ("Ndam (ندم)", "Deep sorrow, authentic contrition, and moral remorse following a harmful action."),
        ("Particularistic Morality", "An ethical system where moral obligations are prioritized toward specific relational networks (especially family) rather than abstract rules."),
        ("Projective Psychological Test", "An assessment technique (like the TAT) using ambiguous stimuli to uncover unmonitored cultural values and deep emotions."),
        ("Restorative Justice", "A disciplinary approach focusing on repairing the harm caused to victims and restoring community relationships rather than punitive shaming."),
        ("Social Desirability Bias", "The tendency of survey respondents to answer questions in a manner that will be viewed favorably by researchers."),
        ("Thematic Apperception Test (TAT)", "A projective instrument where subjects create narrative stories in response to standardized ambiguous visual cards."),
    ]

    glossary_table_rows = [
        [Paragraph("<b>Academic Term</b>", styles["TableHead"]), Paragraph("<b>Simple English Definitional Meaning</b>", styles["TableHead"])]
    ]
    for term, definition in glossary_data:
        glossary_table_rows.append([
            Paragraph(f"<b>{term}</b>", styles["TableCellBold"]),
            Paragraph(definition, styles["TableCell"]),
        ])

    glossary_tbl = Table(glossary_table_rows, colWidths=[content_w * 0.28, content_w * 0.72])
    glossary_tbl.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0284C7")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F0F9FF")]),
        ])
    )
    story.append(glossary_tbl)

    # ==========================================================================
    # CHAPTER 10: PROFESSOR'S LECTURE QUESTIONS & HOMEWORK ASSIGNMENT
    # ==========================================================================
    if new_lecture_qa:
        story.append(PageBreak())
        story.append(Paragraph("CHAPTER 10", styles["ChapterNumber"]))
        story.append(Paragraph("PROFESSOR'S LECTURE QUESTIONS & EXAMINATION HOMEWORK", styles["ChapterHeading"]))
        story.append(
            Paragraph(
                "<b>Primary Sources:</b> <i>Uploaded Lecture Slide 1 (Questions 1–9) & Slide 2 (Homework Assignment)</i>",
                styles["CoverMeta"],
            )
        )
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=3, spaceAfter=12))

        # Section 1 Header
        story.append(Paragraph("SECTION 1: THE 9 CORE LECTURE EXAMINATION QUESTIONS (SLIDE 1)", styles["SectionHeading"]))
        story.append(
            Paragraph(
                "Below are the verbatim questions projected during the university lecture, paired with rigorous, "
                "academically verified model answers, pedagogical explanations in simple English, and high-yield exam takeaways.",
                styles["AcademicBody"],
            )
        )
        story.append(Spacer(1, 6))

        for q_item in new_lecture_qa:
            # Dark navy blue heading for the question
            story.append(
                Paragraph(
                    f"<b>QUESTION {q_item['q_num']:02d}: {q_item['question'].upper()}</b>",
                    styles["SectionHeading"],
                )
            )
            story.append(Paragraph(f"<b>Source Verified in Text:</b> <i>{q_item['source']}</i>", styles["CoverMeta"]))
            story.append(Spacer(1, 3))

            # 1. GREEN MODEL ANSWER BOX
            green_box_content = [
                Paragraph("<b>📗 MODEL ANSWER:</b>", styles["GreenBoxTitle"]),
                Spacer(1, 2),
                Paragraph(q_item["model_answer"], styles["GreenBoxBody"]),
            ]
            story.append(create_callout_box(green_box_content, box_type="green", content_width=content_w))
            story.append(Spacer(1, 4))

            # 2. BLUE ADDITIONAL EXPLANATION BOX
            blue_box_content = [
                Paragraph("<b>📘 ADDITIONAL EXPLANATION:</b>", styles["BlueBoxTitle"]),
                Spacer(1, 2),
                Paragraph(q_item["additional_explanation"], styles["BlueBoxBody"]),
            ]
            story.append(create_callout_box(blue_box_content, box_type="blue", content_width=content_w))
            story.append(Spacer(1, 4))

            # 3. GOLD IMPORTANT TO REMEMBER BOX
            gold_box_content = [
                Paragraph("<b>📙 IMPORTANT TO REMEMBER:</b>", styles["GoldBoxTitle"]),
                Spacer(1, 2),
                Paragraph(q_item["important_to_remember"].replace("\n", "<br/>"), styles["GoldBoxBody"]),
            ]
            story.append(create_callout_box(gold_box_content, box_type="gold", content_width=content_w))
            story.append(Spacer(1, 14))

        # Section 2 Header: Homework Synthesis Task
        if homework_task:
            story.append(Spacer(1, 10))
            story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1E3A8A"), spaceBefore=6, spaceAfter=10))
            story.append(Paragraph("SECTION 2: HOMEWORK ASSIGNMENT & CURRICULAR SYNTHESIS (SLIDE 2)", styles["SectionHeading"]))
            story.append(
                Paragraph(
                    f"<b>ASSIGNMENT PROMPT:</b> <i>\"{homework_task['prompt']}\"</i>",
                    styles["AcademicCitation"],
                )
            )
            story.append(Spacer(1, 4))

            # 1. GREEN MODEL ANSWER BOX FOR HOMEWORK
            hw_green_box = [
                Paragraph("<b>📗 MODEL ANSWER (FOUR-PART SYNTHESIS):</b>", styles["GreenBoxTitle"]),
                Spacer(1, 2),
                Paragraph(homework_task["model_answer"], styles["GreenBoxBody"]),
            ]
            story.append(create_callout_box(hw_green_box, box_type="green", content_width=content_w))
            story.append(Spacer(1, 6))

            # 2. BLUE ADDITIONAL EXPLANATION BOX FOR HOMEWORK
            hw_blue_box = [
                Paragraph("<b>📘 ADDITIONAL EXPLANATION (PEDAGOGICAL RATIONALE):</b>", styles["BlueBoxTitle"]),
                Spacer(1, 2),
                Paragraph(homework_task["additional_explanation"], styles["BlueBoxBody"]),
            ]
            story.append(create_callout_box(hw_blue_box, box_type="blue", content_width=content_w))
            story.append(Spacer(1, 6))

            # 3. GOLD IMPORTANT TO REMEMBER BOX FOR HOMEWORK
            hw_gold_box = [
                Paragraph("<b>📙 IMPORTANT TO REMEMBER (EXAMINATION SYNTHESIS LINKS):</b>", styles["GoldBoxTitle"]),
                Spacer(1, 2),
                Paragraph(homework_task["important_to_remember"].replace("\n", "<br/>"), styles["GoldBoxBody"]),
            ]
            story.append(create_callout_box(hw_gold_box, box_type="gold", content_width=content_w))
            story.append(Spacer(1, 14))

    # Build the document using NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    file_size_mb = os.path.getsize(output_pdf_path) / (1024.0 * 1024.0)

    print(f"\n  ✓ PDF compiled successfully!")
    print(f"  ✓ Output file: '{output_pdf_path}'")
    print(f"  ✓ Total document size: {file_size_mb:.2f} MB")
    return output_pdf_path


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from src.extractor import extract_curriculum_corpus
    from src.explanation_engine import build_curriculum_explanations
    from src.question_solver import build_academic_qa_corpus

    corpus = extract_curriculum_corpus("input")
    explanations = build_curriculum_explanations(corpus)
    qa_list = build_academic_qa_corpus(corpus)
    generate_study_guide_pdf(corpus, explanations, qa_list)
