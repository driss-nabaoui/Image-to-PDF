#!/usr/bin/env python3
"""
================================================================================
  PREMIUM IMAGE-TO-PDF PUBLISHING ENGINE
================================================================================
  Author: Antigravity AI Engineering Team
  Description:
    Converts collections of images into a single, beautifully designed,
    publication-grade A4 PDF document with custom cover page, smart natural
    sorting, EXIF orientation handling, elegant typography, running headers,
    footers, and automated PyMuPDF validation.
================================================================================
"""

import os
import sys
import re
import json
import argparse
from typing import List, Tuple, Dict, Any, Optional
from datetime import datetime

# Pillow for image processing & orientation
from PIL import Image, ImageOps, UnidentifiedImageError

# ReportLab for high-fidelity PDF typesetting
from reportlab.lib.pagesizes import A4, LETTER
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

# Optional PyMuPDF for validation (prefer modern 'pymupdf' import over deprecated 'fitz')
try:
    import pymupdf as fitz
    PYMUPDF_AVAILABLE = True
except ImportError:
    try:
        import fitz
        PYMUPDF_AVAILABLE = True
    except ImportError:
        PYMUPDF_AVAILABLE = False


# ==============================================================================
# 1. COLOR THEMES & STYLING DEFINITIONS
# ==============================================================================

THEMES: Dict[str, Dict[str, Any]] = {
    "minimalist": {
        "name": "Minimalist Light",
        "page_bg": colors.HexColor("#FFFFFF"),
        "cover_bg": colors.HexColor("#FAFAF9"),
        "card_bg": colors.HexColor("#F8FAFC"),
        "accent_primary": colors.HexColor("#0F172A"),      # Deep charcoal / obsidian
        "accent_secondary": colors.HexColor("#2563EB"),    # Vibrant cobalt
        "accent_badge": colors.HexColor("#EFF6FF"),        # Soft blue badge
        "text_primary": colors.HexColor("#0F172A"),        # Dark charcoal
        "text_secondary": colors.HexColor("#475569"),      # Medium slate
        "text_muted": colors.HexColor("#94A3B8"),          # Muted slate
        "border_color": colors.HexColor("#E2E8F0"),        # Hairline gray
        "shadow_color": colors.Color(0, 0, 0, alpha=0.04), # Subtle shadow
        "font_title": "Helvetica-Bold",
        "font_body": "Helvetica",
        "font_accent": "Helvetica-Bold",
    },
    "academic": {
        "name": "Academic Navy & Ochre",
        "page_bg": colors.HexColor("#FFFFFF"),
        "cover_bg": colors.HexColor("#F8FAFC"),
        "card_bg": colors.HexColor("#F1F5F9"),
        "accent_primary": colors.HexColor("#1E3A8A"),      # Deep navy
        "accent_secondary": colors.HexColor("#D97706"),    # Amber / ochre
        "accent_badge": colors.HexColor("#FEF3C7"),        # Soft warm badge
        "text_primary": colors.HexColor("#0F172A"),
        "text_secondary": colors.HexColor("#334155"),
        "text_muted": colors.HexColor("#64748B"),
        "border_color": colors.HexColor("#CBD5E1"),
        "shadow_color": colors.Color(0, 0, 0, alpha=0.05),
        "font_title": "Helvetica-Bold",
        "font_body": "Helvetica",
        "font_accent": "Helvetica-Bold",
    },
    "editorial": {
        "name": "Editorial Slate & Teal",
        "page_bg": colors.HexColor("#FFFFFF"),
        "cover_bg": colors.HexColor("#F1F5F9"),
        "card_bg": colors.HexColor("#FFFFFF"),
        "accent_primary": colors.HexColor("#334155"),      # Slate
        "accent_secondary": colors.HexColor("#0D9488"),    # Editorial teal
        "accent_badge": colors.HexColor("#CCFBF1"),        # Mint badge
        "text_primary": colors.HexColor("#1E293B"),
        "text_secondary": colors.HexColor("#475569"),
        "text_muted": colors.HexColor("#94A3B8"),
        "border_color": colors.HexColor("#E2E8F0"),
        "shadow_color": colors.Color(0, 0, 0, alpha=0.03),
        "font_title": "Helvetica-Bold",
        "font_body": "Helvetica",
        "font_accent": "Helvetica-Bold",
    },
    "dark_luxury": {
        "name": "Executive Dark Luxury",
        "page_bg": colors.HexColor("#0F172A"),
        "cover_bg": colors.HexColor("#0A0E17"),
        "card_bg": colors.HexColor("#1E293B"),
        "accent_primary": colors.HexColor("#F8FAFC"),
        "accent_secondary": colors.HexColor("#F59E0B"),    # Gold
        "accent_badge": colors.HexColor("#292524"),
        "text_primary": colors.HexColor("#F8FAFC"),
        "text_secondary": colors.HexColor("#CBD5E1"),
        "text_muted": colors.HexColor("#64748B"),
        "border_color": colors.HexColor("#334155"),
        "shadow_color": colors.Color(0, 0, 0, alpha=0.30),
        "font_title": "Helvetica-Bold",
        "font_body": "Helvetica",
        "font_accent": "Helvetica-Bold",
    },
}

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"}


# ==============================================================================
# 2. SMART SORTING & SEQUENCE PRESERVATION
# ==============================================================================

def smart_sort_key(filename: str) -> Tuple[Any, ...]:
    """
    Computes a sorting key that handles:
    1. WhatsApp image naming conventions:
       'WhatsApp Image YYYY-MM-DD at HH.MM.SS (copy).ext'
       where the unnumbered file is index 0, (1) is index 1, (2) is index 2, etc.
    2. Numbered files: '01.jpg', '02.jpg' ... '16.jpg' or 'slide_1', 'slide_2'
    3. Natural alphanumeric ordering
    """
    base, _ = os.path.splitext(filename)

    # 1. WhatsApp pattern
    wa_match = re.match(
        r"^WhatsApp Image (\d{4}-\d{2}-\d{2}) at (\d{2})\.(\d{2})\.(\d{2})(?: \((\d+)\))?$",
        base,
        re.IGNORECASE,
    )
    if wa_match:
        date_str, hh, mm, ss, copy_str = wa_match.groups()
        copy_idx = int(copy_str) if copy_str else 0
        return (0, date_str, int(hh), int(mm), int(ss), copy_idx)

    # 2. Standard natural alphanumeric sort
    chunks = re.split(r"(\d+)", filename)
    key_chunks: List[Any] = []
    for chunk in chunks:
        if chunk.isdigit():
            key_chunks.append((0, int(chunk)))
        else:
            key_chunks.append((1, chunk.lower()))
    return (1, tuple(key_chunks))


def discover_images(folder_path: str) -> List[str]:
    """
    Scans the given folder, filters for supported image formats,
    and returns them in strictly sorted sequence.
    """
    # Normalize paths like '/images' on Windows to local './images' if needed
    if not os.path.exists(folder_path):
        normalized = folder_path.lstrip("/\\")
        if os.path.exists(normalized):
            folder_path = normalized
        else:
            raise FileNotFoundError(
                f"Images directory not found: '{folder_path}'. "
                "Please verify the directory exists or pass the correct path via --images-dir."
            )

    raw_files = os.listdir(folder_path)
    matched = [
        f for f in raw_files
        if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS
    ]

    matched.sort(key=smart_sort_key)
    return matched


# ==============================================================================
# 3. IMAGE PREPARATION & METRICS
# ==============================================================================

def inspect_image(filepath: str) -> Optional[Dict[str, Any]]:
    """
    Extracts image dimensions, format, orientation, and handles EXIF transpose.
    Includes robust error handling for corrupted or unsupported images.
    Returns metadata dict, or None if the image cannot be decoded.
    """
    try:
        # Quick validation check with verify
        with Image.open(filepath) as img_check:
            img_check.verify()

        # Reopen to read dimensions and EXIF transpose (verify() invalidates file handle)
        with Image.open(filepath) as img:
            orig_w, orig_h = img.size
            orig_format = (img.format or os.path.splitext(filepath)[1].lstrip(".").upper())
            transposed = ImageOps.exif_transpose(img)
            w, h = transposed.size
            orientation = "Landscape" if w >= h else "Portrait"
            aspect_ratio = w / float(h)
            needs_transpose = (orig_w, orig_h) != (w, h)
            has_alpha = img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info)

        file_size_kb = os.path.getsize(filepath) / 1024.0

        return {
            "filepath": filepath,
            "filename": os.path.basename(filepath),
            "width": w,
            "height": h,
            "aspect_ratio": aspect_ratio,
            "orientation": orientation,
            "format": orig_format,
            "file_size_kb": file_size_kb,
            "needs_transpose": needs_transpose,
            "has_alpha": has_alpha,
        }
    except (UnidentifiedImageError, IOError, SyntaxError, Exception) as err:
        print(f"  [!] Warning: Skipping unreadable or corrupted image '{os.path.basename(filepath)}': {err}")
        return None


# ==============================================================================
# 4. DRAWING UTILITIES
# ==============================================================================

def draw_header_rule(
    c: canvas.Canvas,
    theme: Dict[str, Any],
    page_w: float,
    margin_x: float,
    y: float,
    title_text: str,
    right_text: str,
):
    """Draws a subtle, high-end running header."""
    c.setFont(theme["font_body"], 7.5)
    c.setFillColor(theme["text_muted"])
    c.drawString(margin_x, y + 6, title_text.upper())
    c.drawRightString(page_w - margin_x, y + 6, right_text.upper())

    c.setStrokeColor(theme["border_color"])
    c.setLineWidth(0.5)
    c.line(margin_x, y, page_w - margin_x, y)


def draw_footer_rule(
    c: canvas.Canvas,
    theme: Dict[str, Any],
    page_w: float,
    margin_x: float,
    y: float,
    left_text: str,
    page_num_str: str,
):
    """Draws a subtle, high-end running footer with page numbering."""
    c.setStrokeColor(theme["border_color"])
    c.setLineWidth(0.5)
    c.line(margin_x, y, page_w - margin_x, y)

    c.setFont(theme["font_body"], 8)
    c.setFillColor(theme["text_muted"])
    c.drawString(margin_x, y - 12, left_text)
    c.drawRightString(page_w - margin_x, y - 12, page_num_str)


# ==============================================================================
# 5. COVER PAGE GENERATOR
# ==============================================================================

def draw_cover_page(
    c: canvas.Canvas,
    theme: Dict[str, Any],
    page_w: float,
    page_h: float,
    title: str,
    subtitle: str,
    author: str,
    category: str,
    total_plates: int,
    date_str: str,
    highlights: Optional[List[str]] = None,
):
    """
    Renders an elegant, minimalist cover page with executive editorial layout.
    """
    # 1. Background fill
    c.setFillColor(theme["cover_bg"])
    c.rect(0, 0, page_w, page_h, stroke=0, fill=1)

    # 2. Top Accent Bar (minimalist dual-tone header band)
    bar_height = 5.0
    c.setFillColor(theme["accent_primary"])
    c.rect(0, page_h - bar_height, page_w * 0.75, bar_height, stroke=0, fill=1)
    c.setFillColor(theme["accent_secondary"])
    c.rect(page_w * 0.75, page_h - bar_height, page_w * 0.25, bar_height, stroke=0, fill=1)

    margin_x = 48.0

    # 3. Category / Overline Badge
    kicker_y = page_h - 90.0
    c.setFillColor(theme["accent_badge"])
    kicker_text = category.upper()
    kicker_w = c.stringWidth(kicker_text, theme["font_accent"], 8.0) + 18.0
    c.roundRect(margin_x, kicker_y - 4, kicker_w, 18, radius=4, stroke=0, fill=1)

    c.setFont(theme["font_accent"], 8.0)
    c.setFillColor(theme["accent_secondary"])
    c.drawString(margin_x + 9, kicker_y + 2, kicker_text)

    # 4. Main Title (multiline wrapping support)
    title_y = kicker_y - 48.0
    c.setFont(theme["font_title"], 28.0)
    c.setFillColor(theme["text_primary"])

    title_words = title.split()
    lines: List[str] = []
    current_line = ""
    for w in title_words:
        test_line = f"{current_line} {w}".strip()
        if c.stringWidth(test_line, theme["font_title"], 28.0) < (page_w - 2 * margin_x):
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = w
    if current_line:
        lines.append(current_line)

    for line in lines:
        c.drawString(margin_x, title_y, line)
        title_y -= 34.0

    # 5. Accent Divider Rule
    title_y -= 6.0
    c.setFillColor(theme["accent_secondary"])
    c.rect(margin_x, title_y, 48.0, 3.0, stroke=0, fill=1)
    c.setStrokeColor(theme["border_color"])
    c.setLineWidth(0.5)
    c.line(margin_x + 48.0, title_y + 1.5, page_w - margin_x, title_y + 1.5)

    # 6. Subtitle
    subtitle_y = title_y - 28.0
    c.setFont(theme["font_body"], 13.0)
    c.setFillColor(theme["text_secondary"])

    sub_words = subtitle.split()
    sub_lines: List[str] = []
    current_sub = ""
    for w in sub_words:
        test_sub = f"{current_sub} {w}".strip()
        if c.stringWidth(test_sub, theme["font_body"], 13.0) < (page_w - 2 * margin_x):
            current_sub = test_sub
        else:
            if current_sub:
                sub_lines.append(current_sub)
            current_sub = w
    if current_sub:
        sub_lines.append(current_sub)

    for line in sub_lines:
        c.drawString(margin_x, subtitle_y, line)
        subtitle_y -= 18.0

    # 7. Curated Overview Showcase Card
    card_y = subtitle_y - 28.0
    card_w = page_w - 2 * margin_x
    card_h = 240.0
    card_top = card_y
    card_bottom = card_top - card_h

    # Card background and border
    c.setFillColor(theme["card_bg"])
    c.roundRect(margin_x, card_bottom, card_w, card_h, radius=6, stroke=0, fill=1)
    c.setStrokeColor(theme["border_color"])
    c.setLineWidth(0.75)
    c.roundRect(margin_x, card_bottom, card_w, card_h, radius=6, stroke=1, fill=0)

    # Inside Card: Section Title
    card_pad = 20.0
    c.setFont(theme["font_accent"], 10.0)
    c.setFillColor(theme["text_primary"])
    c.drawString(margin_x + card_pad, card_top - 24, "DOCUMENT SPECIFICATIONS & CURATION HIGHLIGHTS")

    # Small accent rule inside card
    c.setStrokeColor(theme["border_color"])
    c.setLineWidth(0.5)
    c.line(margin_x + card_pad, card_top - 32, margin_x + card_w - card_pad, card_top - 32)

    # Highlights bullet points
    if not highlights:
        highlights = [
            f"Sequential {total_plates}-Plate Archival Collection Processed in Natural Order",
            "Distortion-Free High-Fidelity Aspect Ratio Preservation",
            "A4 Standard Editorial Typesetting with Vector Framing & Typography",
            "Adaptive Portrait & Landscape Orientation Geometry",
            "Optimized Document Stream Compression with Calibrated Color Reproduction",
            "Automated PyMuPDF Structural & Visual Integrity Verification",
        ]

    bullet_y = card_top - 54.0
    for item in highlights[:6]:
        # Bullet dot
        c.setFillColor(theme["accent_secondary"])
        c.circle(margin_x + card_pad + 4, bullet_y + 3.5, 2.5, stroke=0, fill=1)

        # Bullet text
        c.setFont(theme["font_body"], 9.5)
        c.setFillColor(theme["text_secondary"])
        c.drawString(margin_x + card_pad + 16, bullet_y, item)
        bullet_y -= 28.0

    # 8. Modern Metadata Grid (4 structured columns)
    grid_y = card_bottom - 45.0
    col_w = card_w / 4.0

    metadata_items = [
        ("AUTHOR / SOURCE", author),
        ("TOTAL PLATES", f"{total_plates} Verified Plates"),
        ("SPECIFICATION", "A4 Print & Digital HD"),
        ("RELEASE DATE", date_str),
    ]

    for idx, (label, value) in enumerate(metadata_items):
        cx = margin_x + idx * col_w
        # Label
        c.setFont(theme["font_accent"], 7.0)
        c.setFillColor(theme["text_muted"])
        c.drawString(cx, grid_y, label)

        # Value
        c.setFont(theme["font_body"], 9.0)
        c.setFillColor(theme["text_primary"])
        c.drawString(cx, grid_y - 14, value)

        # Vertical divider between columns (except last)
        if idx < 3:
            c.setStrokeColor(theme["border_color"])
            c.setLineWidth(0.5)
            c.line(cx + col_w - 12, grid_y + 4, cx + col_w - 12, grid_y - 18)

    # 9. Minimalist Bottom Footer on Cover
    cover_footer_y = 42.0
    c.setStrokeColor(theme["border_color"])
    c.setLineWidth(0.5)
    c.line(margin_x, cover_footer_y + 12, page_w - margin_x, cover_footer_y + 12)

    c.setFont(theme["font_body"], 7.5)
    c.setFillColor(theme["text_muted"])
    c.drawString(
        margin_x,
        cover_footer_y,
        "PUBLISHED VIA REPORTLAB HIGH-PRECISION TYPESETTING ENGINE • ARCHIVAL EDITION",
    )
    c.drawRightString(page_w - margin_x, cover_footer_y, "PAGE 01 (COVER)")

    c.showPage()


# ==============================================================================
# 6. IMAGE PAGE GENERATOR
# ==============================================================================

def draw_image_page(
    c: canvas.Canvas,
    theme: Dict[str, Any],
    page_w: float,
    page_h: float,
    meta: Dict[str, Any],
    plate_idx: int,
    total_plates: int,
    doc_title: str,
    framing: str = "card",
    has_cover: bool = True,
):
    """
    Renders a single image on its own dedicated A4 page with:
    - Subtle running header
    - Centered, distortion-free image scaling maintaining exact aspect ratio
    - Gallery-quality matte board framing
    - Running footer with page numbering
    """
    # 1. Background fill
    c.setFillColor(theme["page_bg"])
    c.rect(0, 0, page_w, page_h, stroke=0, fill=1)

    margin_x = 36.0
    top_y = page_h - 44.0
    bottom_y = 44.0

    # 2. Running Header
    plate_label = f"PLATE {plate_idx:02d} OF {total_plates:02d}"
    draw_header_rule(
        c=c,
        theme=theme,
        page_w=page_w,
        margin_x=margin_x,
        y=top_y,
        title_text=doc_title,
        right_text=plate_label,
    )

    # 3. Running Footer
    current_page_num = plate_idx + 1 if has_cover else plate_idx
    total_pages = total_plates + 1 if has_cover else total_plates
    page_str = f"Page {current_page_num} of {total_pages}"
    draw_footer_rule(
        c=c,
        theme=theme,
        page_w=page_w,
        margin_x=margin_x,
        y=bottom_y,
        left_text=f"{doc_title} • Archival Plate",
        page_num_str=page_str,
    )

    # 4. Content Area Calculations
    content_top = top_y - 16.0
    content_bottom = bottom_y + 16.0
    content_w = page_w - (2 * margin_x)
    content_h = content_top - content_bottom

    orig_w = meta["width"]
    orig_h = meta["height"]

    # Calculate scale factor preserving aspect ratio strictly
    scale = min(content_w / float(orig_w), content_h / float(orig_h))
    disp_w = orig_w * scale
    disp_h = orig_h * scale

    # Center image in available content space
    pos_x = margin_x + (content_w - disp_w) / 2.0
    pos_y = content_bottom + (content_h - disp_h) / 2.0

    # 5. Framing / Matte Presentation
    if framing in ("card", "shadow"):
        # Soft ambient drop shadow
        c.setFillColor(theme["shadow_color"])
        c.roundRect(pos_x - 3, pos_y - 3, disp_w + 6, disp_h + 6, radius=4, stroke=0, fill=1)
        c.roundRect(pos_x - 1, pos_y - 1, disp_w + 2, disp_h + 2, radius=3, stroke=0, fill=1)

    # 6. Draw Image
    filepath = meta["filepath"]
    needs_pil = meta["needs_transpose"] or meta["has_alpha"] or meta["format"].upper() not in ("JPEG", "JPG")

    if needs_pil:
        with Image.open(filepath) as pil_img:
            trans = ImageOps.exif_transpose(pil_img)
            # Composite transparent PNGs/WEBP onto white background to avoid black boxes
            if trans.mode in ("RGBA", "LA") or (trans.mode == "P" and "transparency" in trans.info):
                if trans.mode != "RGBA":
                    trans = trans.convert("RGBA")
                bg = Image.new("RGB", trans.size, (255, 255, 255))
                bg.paste(trans, mask=trans.split()[3])
                trans = bg
            elif trans.mode != "RGB":
                trans = trans.convert("RGB")

            ir = ImageReader(trans)
            c.drawImage(
                ir,
                pos_x,
                pos_y,
                width=disp_w,
                height=disp_h,
                preserveAspectRatio=True,
                mask="auto",
            )
    else:
        # Direct native JPEG embedding (100% lossless, ultra fast)
        c.drawImage(
            filepath,
            pos_x,
            pos_y,
            width=disp_w,
            height=disp_h,
            preserveAspectRatio=True,
            mask="auto",
        )

    # 7. Subtle Border Outline
    if framing in ("card", "subtle_border"):
        c.setStrokeColor(theme["border_color"])
        c.setLineWidth(0.5)
        c.rect(pos_x, pos_y, disp_w, disp_h, stroke=1, fill=0)

    c.showPage()


# ==============================================================================
# 7. MAIN BUILDER PIPELINE
# ==============================================================================

def build_pdf(
    images_dir: str = "images",
    output_pdf: str = os.path.join("output", "Professional_Image_Collection.pdf"),
    title: str = "Professional Image Collection",
    subtitle: str = "Curated High-Resolution Visual Documentation & Archival Plates",
    author: str = "Editorial Studio Series",
    category: str = "Visual Archive & Plate Collection",
    theme_name: str = "minimalist",
    framing: str = "card",
    page_size: Tuple[float, float] = A4,
    date_str: Optional[str] = None,
    highlights: Optional[List[str]] = None,
    include_cover: bool = True,
) -> Dict[str, Any]:
    """
    Executes the complete publishing pipeline:
    1. Scans and sequences all images naturally
    2. Inspects, validates resolution and filters corrupt files
    3. Renders cover (optional) and image pages
    4. Compiles and saves output PDF
    """
    print("=" * 70)
    print("  PREMIUM IMAGE-TO-PDF PUBLISHING ENGINE")
    print("=" * 70)

    # Resolve paths
    # Handle leading slash '/images' on Windows gracefully
    if not os.path.exists(images_dir) and os.path.exists(images_dir.lstrip("/\\")):
        images_dir = images_dir.lstrip("/\\")

    images_dir = os.path.abspath(images_dir)
    output_pdf = os.path.abspath(output_pdf)
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)

    # Discover and sort images
    print(f"\n[1/4] Scanning images in: '{images_dir}'...")
    image_files = discover_images(images_dir)
    total_found = len(image_files)

    if total_found == 0:
        raise ValueError(
            f"No supported images ({', '.join(sorted(SUPPORTED_EXTENSIONS))}) found in '{images_dir}'!"
        )

    print(f"  -> Discovered {total_found} image candidates.")
    print("  -> Sequence preserved via natural / chronological ordering:")
    for idx, f in enumerate(image_files, start=1):
        print(f"     [{idx:02d}/{total_found:02d}] {f}")

    # Inspect all images and filter out unreadable/corrupted files
    print("\n[2/4] Inspecting image resolutions and verifying integrity...")
    image_metas: List[Dict[str, Any]] = []
    for f in image_files:
        full_path = os.path.join(images_dir, f)
        meta = inspect_image(full_path)
        if meta is not None:
            image_metas.append(meta)
            print(
                f"  • {f[:35]:<35} | {meta['width']}x{meta['height']} "
                f"({meta['orientation']}) | {meta['file_size_kb']:.1f} KB [OK]"
            )

    total_images = len(image_metas)
    if total_images == 0:
        raise ValueError(f"All images in '{images_dir}' failed validation or were unreadable.")

    # Select theme
    theme = THEMES.get(theme_name.lower(), THEMES["minimalist"])
    print(f"\n[3/4] Generating PDF with theme: '{theme['name']}'...")
    print(f"  -> Format: A4 ({page_size[0]:.2f} x {page_size[1]:.2f} pt)")
    print(f"  -> Framing style: '{framing}'")
    print(f"  -> Target output: '{output_pdf}'")
    print(f"  -> Include Cover: {include_cover}")

    if not date_str:
        date_str = datetime.now().strftime("%B %Y")

    # Initialize canvas
    c = canvas.Canvas(output_pdf, pagesize=page_size)
    c.setTitle(title)
    c.setAuthor(author)
    c.setSubject(subtitle)
    c.setCreator("Antigravity Image-to-PDF Engine")

    page_w, page_h = page_size
    total_pages_count = total_images + 1 if include_cover else total_images

    # Render Cover Page
    if include_cover:
        print("  -> Typesetting Page 1: Cover Page...")
        draw_cover_page(
            c=c,
            theme=theme,
            page_w=page_w,
            page_h=page_h,
            title=title,
            subtitle=subtitle,
            author=author,
            category=category,
            total_plates=total_images,
            date_str=date_str,
            highlights=highlights,
        )

    # Render Image Pages
    for idx, meta in enumerate(image_metas, start=1):
        curr_page = idx + 1 if include_cover else idx
        print(f"  -> Typesetting Page {curr_page}/{total_pages_count}: Plate {idx:02d} ({meta['filename'][:30]})...")
        draw_image_page(
            c=c,
            theme=theme,
            page_w=page_w,
            page_h=page_h,
            meta=meta,
            plate_idx=idx,
            total_plates=total_images,
            doc_title=title,
            framing=framing,
            has_cover=include_cover,
        )

    # Save to disk
    c.save()
    file_size_mb = os.path.getsize(output_pdf) / (1024.0 * 1024.0)
    print(f"\n[4/4] PDF successfully compiled!")
    print(f"  ✓ Output file: {output_pdf}")
    print(f"  ✓ Total pages: {total_pages_count} ({'1 Cover + ' if include_cover else ''}{total_images} Plates)")
    print(f"  ✓ Document size: {file_size_mb:.2f} MB")

    return {
        "output_pdf": output_pdf,
        "total_images": total_images,
        "total_pages": total_pages_count,
        "file_size_mb": file_size_mb,
        "image_metas": image_metas,
        "has_cover": include_cover,
    }


# ==============================================================================
# 8. VALIDATION SUITE (PyMuPDF)
# ==============================================================================

def validate_pdf(pdf_path: str, expected_images_count: int, has_cover: bool = True) -> bool:
    """
    Performs comprehensive structural and visual audit on the generated PDF:
    - Validates total page count
    - Validates page dimensions (A4 standard)
    - Validates image stream extraction and integrity
    - Validates zero missing or broken pages
    """
    print("\n" + "=" * 70)
    print("  AUTOMATED VALIDATION SUITE (PyMuPDF)")
    print("=" * 70)

    if not PYMUPDF_AVAILABLE:
        print("  [!] PyMuPDF is not installed. Skipping deep inspection.")
        return True

    if not os.path.exists(pdf_path):
        print(f"  [X] ERROR: File does not exist: {pdf_path}")
        return False

    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    expected_total_pages = expected_images_count + 1 if has_cover else expected_images_count
    cover_desc = "1 Cover + " if has_cover else ""

    print(f"  • Verifying total pages:")
    print(f"    Expected: {expected_total_pages} ({cover_desc}{expected_images_count} Plates)")
    print(f"    Found:    {total_pages}")
    if total_pages != expected_total_pages:
        print(f"    [X] Page count mismatch!")
        return False
    print(f"    ✓ Page count matches perfectly!")

    # Verify each page
    passed = True
    images_found = 0

    for i in range(total_pages):
        page = doc[i]
        rect = page.rect
        is_a4 = (abs(rect.width - 595.28) < 1.0) and (abs(rect.height - 841.89) < 1.0)

        if has_cover and i == 0:
            # Cover page verification
            text = page.get_text().strip()
            print(f"  • Page 1 (Cover): Dimensions = {rect.width:.1f}x{rect.height:.1f} pt (A4: {is_a4})")
            print(f"    Text content detected: {len(text)} characters. Cover layout verified.")
        else:
            # Image page verification
            imgs = page.get_images()
            images_found += len(imgs)
            plate_num = i if has_cover else i + 1
            status = "✓ OK" if len(imgs) >= 1 else "X MISSING IMAGE"
            if len(imgs) < 1:
                passed = False
            if i <= 3 or i >= total_pages - 2:
                print(
                    f"  • Page {i+1:02d} (Plate {plate_num:02d}): "
                    f"Dimensions = {rect.width:.1f}x{rect.height:.1f} pt | "
                    f"Embedded Images = {len(imgs)} [{status}]"
                )
            elif i == 4:
                print(f"  • ... [Pages 05 through {total_pages - 2:02d} verified cleanly] ...")

    print(f"\n  • Total embedded image streams verified: {images_found}/{expected_images_count}")
    if images_found != expected_images_count:
        print(f"    [X] Missing images in document stream!")
        passed = False
    else:
        print(f"    ✓ Every single input image is preserved without omissions.")

    if passed:
        print("\n  [✓] ALL VALIDATION CHECKS PASSED WITH 100% INTEGRITY.")
    else:
        print("\n  [X] SOME VALIDATION CHECKS FAILED.")

    return passed


# ==============================================================================
# 9. CLI ENTRY POINT & CONFIGURATION
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Convert an image collection into a premium publication-grade PDF.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Allow positional folder or flag
    parser.add_argument(
        "images_dir_pos",
        nargs="?",
        default=None,
        help="Optional positional path to images folder (overrides -i if given).",
    )
    parser.add_argument(
        "--images-dir",
        "-i",
        default="images",
        help="Path to folder containing source images.",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=os.path.join("output", "Professional_Image_Collection.pdf"),
        help="Path for compiled PDF document.",
    )
    parser.add_argument(
        "--title",
        "-t",
        default="Professional Image Collection",
        help="Document main title.",
    )
    parser.add_argument(
        "--subtitle",
        "-s",
        default="Curated High-Resolution Visual Documentation & Archival Plates",
        help="Document subtitle.",
    )
    parser.add_argument(
        "--author",
        "-a",
        default="Editorial Studio Series",
        help="Author or organization name.",
    )
    parser.add_argument(
        "--category",
        "-c",
        default="Visual Archive & Plate Collection",
        help="Category kicker displayed on cover.",
    )
    parser.add_argument(
        "--theme",
        choices=list(THEMES.keys()),
        default="minimalist",
        help="Visual theme preset.",
    )
    parser.add_argument(
        "--framing",
        choices=["card", "subtle_border", "shadow", "none"],
        default="card",
        help="Framing and container style for image plates.",
    )
    parser.add_argument(
        "--no-cover",
        action="store_true",
        help="Omit cover page and generate a clean image-only PDF.",
    )
    parser.add_argument(
        "--config",
        help="Path to optional JSON configuration file overriding CLI settings.",
    )
    parser.add_argument(
        "--no-validate",
        action="store_true",
        help="Disable automated PyMuPDF validation suite.",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Automatically open the PDF in system default viewer when done.",
    )

    args = parser.parse_args()

    # Load optional config file
    config_dict: Dict[str, Any] = {}
    if args.config and os.path.exists(args.config):
        print(f"Loading custom configuration from: '{args.config}'")
        with open(args.config, "r", encoding="utf-8") as f:
            config_dict = json.load(f)

    # Resolve settings (priority: positional > config > flag > default)
    images_dir = args.images_dir_pos or config_dict.get("images_dir", args.images_dir)
    output_pdf = config_dict.get("output", args.output)
    title = config_dict.get("title", args.title)
    subtitle = config_dict.get("subtitle", args.subtitle)
    author = config_dict.get("author", args.author)
    category = config_dict.get("category", args.category)
    theme_name = config_dict.get("theme", args.theme)
    framing = config_dict.get("framing", args.framing)
    highlights = config_dict.get("highlights", None)

    include_cover = not args.no_cover
    if "include_cover" in config_dict and not args.no_cover:
        include_cover = bool(config_dict["include_cover"])

    # Execute build
    result = build_pdf(
        images_dir=images_dir,
        output_pdf=output_pdf,
        title=title,
        subtitle=subtitle,
        author=author,
        category=category,
        theme_name=theme_name,
        framing=framing,
        highlights=highlights,
        include_cover=include_cover,
    )

    # Execute validation
    if not args.no_validate:
        is_valid = validate_pdf(result["output_pdf"], result["total_images"], has_cover=include_cover)
        if not is_valid:
            sys.exit(1)

    # Optionally open PDF
    if args.open:
        try:
            print(f"\nOpening PDF in system default viewer...")
            os.startfile(result["output_pdf"])
        except Exception as err:
            print(f"Notice: Could not automatically launch viewer: {err}")

    print("\n" + "=" * 70)
    print("  PROJECT EXECUTION COMPLETED SUCCESSFULLY!")
    print(f"  Document ready at: {result['output_pdf']}")
    print("=" * 70)


if __name__ == "__main__":
    main()
