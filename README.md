# 🎓 AI Academic Study Guide & Smart PDF Generator

A complete, production-grade university publishing engine and automated educational content suite. Built in Python, this application dynamically discovers all available source images, documents, and lecture plates, extracts the full scholarly content, generates crystal-clear conceptual explanations in **Simple English** (marked in **Blue**), solves and explains all academic examination questions with **Model Answers** (marked in **Green**), and compiles a publication-grade, 22-page academic study guide in A4 format via ReportLab Platypus.

---

## 📚 Academic Subject Matter: Reading in Global Culture

This study guide is based on the seminal empirical research paper:
> **"Intersection of cultures, multiculturalism and Moroccan immigrants in Belgium: An analysis of the emotional repertoire of shame and guilt"**  
> **Author:** Dr. Philip Hermans  
> **Affiliation:** Department of Social and Cultural Anthropology, University of Leuven / University of Groningen  
> **Citation:** *International Journal of Educational Research*, Vol. 31 (1999), pp. 303–316 (Pergamon / Elsevier Science).  
> **Primary Source Ingestion:** `c:\Users\AdMin\Downloads\globla_culture6641` (Pages 303–316 Complete).

---

## 📁 Project Architecture & Deliverables

```
Image-to-PDF/
├── input/                                         # Dynamic input directory (supports JPG, PNG, WEBP, PDF)
│   ├── 01.jpeg .. 13.jpeg                         # Sequential archival journal plates (Pages 303–316)
│   ├── question_slide_1.jpg                       # Lecture slide: Questions 1 through 9
│   ├── question_slide_2.jpg                       # Lecture slide: Homework assignment prompt
│   └── README.md                                  # Plate mapping index
├── output/                                        # Generated publication deliverables
│   ├── Complete_University_Study_Guide_Updated.pdf# Master 28-page publication-grade PDF textbook (Includes Chapter 10 Q&A)
│   ├── Complete_University_Study_Guide.pdf        # Base 22-page publication-grade PDF textbook (Preserved)
│   ├── New_Questions_And_Answers.md               # Complete Markdown of Slide Questions 1–9 & Homework
│   ├── Extracted_Content.md                       # Complete, faithful academic text extraction
│   ├── Explained_Study_Notes.md                   # Pedagogical study notes with Blue explanations
│   ├── Questions_And_Answers.md                   # 12 Examination questions with Green model answers
│   └── preview_*.png                              # High-DPI page render previews
├── src/                                           # Modular system architecture
│   ├── __init__.py                                # Package initialization
│   ├── extractor.py                               # Dynamic file discovery & curriculum extraction
│   ├── explanation_engine.py                      # Simple English explanation engine (Blue Boxes)
│   ├── question_solver.py                         # Examination question detection & solver (Green Boxes)
│   ├── new_questions.py                           # Structured Q&A corpus for Slide Questions 1–9 & Homework
│   └── pdf_generator.py                           # ReportLab Platypus high-fidelity PDF typesetting
├── config.json                                    # Customizable document configuration
├── main.py                                        # Master CLI orchestrator & validation runner
├── requirements.txt                               # Project dependencies
└── README.md                                      # Project documentation & study guide
```

---

## 🎨 Three-Tier Visual System

The generated study guide enforces a strict, color-coded visual hierarchy throughout:

| Component | Visual Styling | Color Palette | Label / Identification |
| :--- | :--- | :--- | :--- |
| **Original Course Content** | Professional academic typography, justified alignment | Dark Charcoal (`#0F172A`) | Standard Chapter & Section Headings |
| **Simple Explanations** | Light-blue padded callout box with navy accent band | Background: `#F0F9FF`<br/>Border: `#0284C7`<br/>Text: `#0369A1` | `SIMPLE EXPLANATION: [CONCEPT]` with practical everyday examples |
| **Model Answers** | Light-green padded callout box with emerald accent band | Background: `#F0FDF4`<br/>Border: `#16A34A`<br/>Text: `#15803D` | `MODEL ANSWER` followed by `WHY IS THIS THE ANSWER?` rationale |
| **Important Definitions** | Warm amber/gold callout container | Background: `#FEF3C7`<br/>Border: `#D97706` | `IMPORTANT DEFINITION / KEY PRINCIPLE` |
| **Topic Summaries** | Slate grey review container at chapter ends | Background: `#F8FAFC`<br/>Border: `#64748B` | `WHAT YOU SHOULD REMEMBER FROM THIS CHAPTER` |

---

## 📖 Curricular Structure (28-Page Study Book)

```
Complete_University_Study_Guide_Updated.pdf (28 Pages)
├── Page 01: Executive University Textbook Cover Page (Navy, Gold, & Charcoal Metadata Grid)
├── Page 02: Table of Contents & Color-Coded Visual System Legend (Chapters 1–10)
├── Page 03–04: Chapter 1 — Historical & Demographic Background of Moroccan Migration in Belgium
├── Page 05–06: Chapter 2 — Psychological Foundations: The Classical Taxonomy of Shame vs. Guilt
├── Page 07–08: Chapter 3 — Western Stereotypes & The Ethnocentric Abuse of Jean Piaget's Moral Stages
├── Page 09: Chapter 4 — Empirical Research Methodology: The Cross-Cultural TAT (70 Adolescents)
├── Page 10–11: Chapter 5 — Quantitative Evidence: Tables 1 & 2 Disproving the Deficit Myth
├── Page 12–13: Chapter 6 — Linguistic & Cultural Analysis: 'Hshuma' (حشومة) vs. 'Dhenb' (ذنب)
├── Page 14: Chapter 7 — Sociostructural Realities & Intercultural Pedagogical Guidelines for Schools
├── Page 15–20: Chapter 8 — Comprehensive Academic Examination: 12 Questions & Green Model Answers
├── Page 21–22: Chapter 9 — Master Revision Guide (8 Core Principles Table) & 20-Term Glossary
└── Page 23–28: Chapter 10 — Professor's Lecture Questions (Q1–9) & Homework Curricular Synthesis
    ├── Page 23–24: Questions 1 to 4 (Author, Focus, Main Ideas, Author's Perspective)
    ├── Page 25–26: Questions 5 to 7 (Themes, Racism & Stereotypes, Definition of Guilt)
    ├── Page 27: Questions 8 to 9 (Definition of Shame, Empirical Exemplification)
    └── Page 28: Section 2 — Homework Assignment & 4-Part Curricular Synthesis
```

---

## ⚡ Quick Start & Execution Commands

### 1. Setup Environment
```powershell
cd "C:\Users\AdMin\Image-to-PDF"
python -m pip install -r requirements.txt
```

### 2. Execute the Complete Pipeline
```powershell
python main.py
```
This automatically:
1. Dynamically detects all source files in `input/` (no fixed count assumed).
2. Extracts full academic content into `output/Extracted_Content.md`.
3. Synthesizes simple English explanations into `output/Explained_Study_Notes.md`.
4. Formulates 12 examination questions and answers into `output/Questions_And_Answers.md`.
5. Compiles the 22-page master textbook into [`output/Complete_University_Study_Guide.pdf`](file:///C:/Users/AdMin/Image-to-PDF/output/Complete_University_Study_Guide.pdf).
6. Runs automated PyMuPDF validation confirming 22 pages, 64,835 characters, and zero blank pages.

### 3. Open Directly in Default System Viewer
```powershell
python main.py --open
```

### 4. Process Any Custom Input Folder
```powershell
python main.py --input "c:\path\to\another_course_folder" --output "output/Custom_Study_Guide.pdf"
```

---

## 🔍 Quality Control & Verification Audit

The built-in PyMuPDF structural audit verifies:
- **Total Pages:** Exactly 22 pages (A4 standard: $595.28 \times 841.89\text{ pt}$).
- **Text Density:** 64,835 total characters extracted across all 22 pages (average 2,947 chars/page).
- **Zero Orphaned or Blank Pages:** Verified dense academic content across every individual page.
- **Visual Separation:** Explanations strictly formatted in blue containers; Model Answers in green containers.
- **Dynamic Two-Pass Header/Footer:** Running headers with paper title and author; running footers with dynamic `Page X of 22` numbering (omitted on Cover).
