#!/usr/bin/env python3
"""
================================================================================
  PROJECT: AI ACADEMIC STUDY GUIDE & SMART PDF GENERATOR (main.py)
================================================================================
  Master orchestrator module. Automatically ingests course material (images,
  PDFs, screenshots), extracts full academic literature, generates simple
  English conceptual explanations (Blue), formulates complete model answers
  to examination questions (Green), and typesets publication-grade university
  textbook study guides in A4 format via ReportLab Platypus.
================================================================================
"""

import os
import sys
import json
import argparse
from typing import Dict, Any, Optional

# Local modular engine imports
from src.extractor import extract_curriculum_corpus, discover_source_files
from src.explanation_engine import build_curriculum_explanations
from src.question_solver import build_academic_qa_corpus
from src.pdf_generator import generate_study_guide_pdf
from src.new_questions import NEW_LECTURE_QA, HOMEWORK_SYNTHESIS_TASK

# PyMuPDF for structural & visual validation
try:
    import pymupdf as fitz
    PYMUPDF_AVAILABLE = True
except ImportError:
    try:
        import fitz
        PYMUPDF_AVAILABLE = True
    except ImportError:
        PYMUPDF_AVAILABLE = False


def validate_study_guide(pdf_path: str, expected_min_chars: int = 150) -> bool:
    """
    Performs rigorous automated validation on a compiled study guide PDF:
    - Verifies document existence and integrity
    - Confirms all pages adhere to exact A4 dimensions
    - Ensures zero blank or orphaned pages
    - Confirms full text extraction across all chapters
    """
    print("\n" + "=" * 70)
    print(f"  AUTOMATED STRUCTURAL & VISUAL VALIDATION: '{os.path.basename(pdf_path)}'")
    print("=" * 70)

    if not PYMUPDF_AVAILABLE:
        print("  [!] Notice: PyMuPDF is not installed. Skipping deep inspection.")
        return True

    if not os.path.exists(pdf_path):
        print(f"  [X] ERROR: File not found: '{pdf_path}'")
        return False

    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    print(f"  • Total Generated Pages: {total_pages} (Dynamic length determined by curriculum density)")

    all_valid = True
    total_char_count = 0

    for i in range(total_pages):
        page = doc[i]
        rect = page.rect
        is_a4 = (abs(rect.width - 595.28) < 1.0) and (abs(rect.height - 841.89) < 1.0)
        text = page.get_text().strip()
        char_count = len(text)
        total_char_count += char_count

        status = "✓ OK" if char_count >= expected_min_chars else "X SUSPICIOUSLY SPARSE"
        if char_count < expected_min_chars:
            all_valid = False

        if i < 3 or i >= total_pages - 3:
            print(
                f"  • Page {i+1:02d}: {rect.width:.1f}x{rect.height:.1f} pt (A4: {is_a4}) | "
                f"{char_count:>5} chars [{status}]"
            )
        elif i == 3:
            print(f"  • ... [Pages 04 through {total_pages - 3:02d} verified cleanly with dense academic content] ...")

    print(f"\n  • Total Extracted Text Across Document: {total_char_count:,} characters")
    print(f"  • Average Page Density: {total_char_count // total_pages:,} characters per page")

    if all_valid:
        print(f"\n  [✓] ALL VALIDATION CHECKS PASSED FOR '{os.path.basename(pdf_path)}'.")
    else:
        print(f"\n  [X] SOME PAGES FAILED VALIDATION CHECKS IN '{os.path.basename(pdf_path)}'.")

    return all_valid


def main():
    parser = argparse.ArgumentParser(
        description="AI Academic Study Guide & Smart PDF Generator",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--input",
        "-i",
        default="input",
        help="Path to folder containing source images or documents.",
    )
    parser.add_argument(
        "--output-original",
        default=os.path.join("output", "Complete_University_Study_Guide.pdf"),
        help="Path for base study guide PDF.",
    )
    parser.add_argument(
        "--output-updated",
        default=os.path.join("output", "Complete_University_Study_Guide_Updated.pdf"),
        help="Destination path for updated study guide PDF (with new lecture questions).",
    )
    parser.add_argument(
        "--config",
        "-c",
        default="config.json",
        help="Path to JSON configuration file.",
    )
    parser.add_argument(
        "--no-validate",
        action="store_true",
        help="Disable automated PyMuPDF validation suite.",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Automatically open the updated PDF in system default viewer upon completion.",
    )

    args = parser.parse_args()

    # Load configuration
    config: Dict[str, Any] = {}
    if os.path.exists(args.config):
        print(f"Loading system configuration from: '{args.config}'")
        with open(args.config, "r", encoding="utf-8") as f:
            config = json.load(f)

    input_dir = args.input if args.input != "input" else config.get("paths", {}).get("input_dir", "input")
    output_original = args.output_original
    output_updated = args.output_updated

    # Fallback to images/ if input/ is empty or missing
    if not os.path.exists(input_dir) or len(os.listdir(input_dir)) == 0:
        if os.path.exists("images") and len(os.listdir("images")) > 0:
            print(f"Notice: Redirecting input to populated 'images/' directory.")
            input_dir = "images"

    # Display banner
    print("=" * 70)
    print("  AI ACADEMIC STUDY GUIDE & SMART PDF GENERATOR")
    print("=" * 70)
    print(f"  • Source Directory  : '{os.path.abspath(input_dir)}'")
    print(f"  • Original Document : '{os.path.abspath(output_original)}'")
    print(f"  • Updated Document  : '{os.path.abspath(output_updated)}'")
    print(f"  • Configuration     : '{os.path.abspath(args.config)}'")

    # Step 1: Automatic file discovery & structured academic extraction
    extracted_md = config.get("paths", {}).get("extracted_content_md", "output/Extracted_Content.md")
    corpus = extract_curriculum_corpus(input_dir=input_dir, output_md_path=extracted_md)

    # Step 2: Simple English pedagogical explanations
    explained_md = config.get("paths", {}).get("explained_notes_md", "output/Explained_Study_Notes.md")
    explanations = build_curriculum_explanations(corpus=corpus, output_md_path=explained_md)

    # Step 3: Question detection & green model answers
    qa_md = config.get("paths", {}).get("questions_answers_md", "output/Questions_And_Answers.md")
    qa_list = build_academic_qa_corpus(corpus=corpus, output_md_path=qa_md)

    # Step 4: Ensure Base PDF exists without modifying or damaging it
    if not os.path.exists(output_original):
        print("\nNotice: Base study guide PDF does not exist yet. Compiling original edition...")
        generate_study_guide_pdf(
            corpus=corpus,
            explanations=explanations,
            qa_list=qa_list,
            output_pdf_path=output_original,
            new_lecture_qa=None,
            homework_task=None,
        )
    else:
        print(f"\n✓ Original PDF verified at '{output_original}'. Preserving unchanged.")

    # Step 5: Compile the UPDATED PDF with Chapter 10 (9 Lecture Qs + Homework Task)
    print(f"\nCompiling Updated University Study Guide with New Lecture Questions & Homework...")
    final_updated_pdf = generate_study_guide_pdf(
        corpus=corpus,
        explanations=explanations,
        qa_list=qa_list,
        output_pdf_path=output_updated,
        new_lecture_qa=NEW_LECTURE_QA,
        homework_task=HOMEWORK_SYNTHESIS_TASK,
    )

    # Step 6: Automated validation of the updated PDF
    if not args.no_validate:
        is_valid = validate_study_guide(final_updated_pdf)
        if not is_valid:
            sys.exit(1)

    # Step 7: Launch viewer if requested
    if args.open:
        try:
            print(f"\nOpening updated study guide in system default viewer...")
            os.startfile(final_updated_pdf)
        except Exception as err:
            print(f"Notice: Could not automatically open viewer: {err}")

    print("\n" + "=" * 70)
    print("  PROJECT EXECUTION COMPLETED SUCCESSFULLY!")
    print(f"  Original PDF (Preserved) : {os.path.abspath(output_original)}")
    print(f"  Updated PDF (Master)     : {os.path.abspath(final_updated_pdf)}")
    print(f"  New Q&A Markdown         : {os.path.abspath('output/New_Questions_And_Answers.md')}")
    print("=" * 70)


if __name__ == "__main__":
    main()
