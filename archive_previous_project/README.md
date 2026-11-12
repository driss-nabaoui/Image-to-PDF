# 📄 Professional Image-to-PDF Publishing Suite

A senior-grade Python application that converts sequential image collections (JPG, JPEG, PNG, WEBP) into a beautifully designed, high-fidelity A4 PDF document with an editorial cover page, smart natural sorting, subtle page numbers, running headers, and automated validation.

---

## 🌟 Key Features

- **Automated Directory Ingestion**: Scans `./images` by default or any custom directory (including Windows and POSIX paths).
- **Universal Format Support**: Full support for JPG, JPEG, PNG, WEBP, BMP, and TIFF formats.
- **Smart Natural Sorting**: Naturally orders filenames like `01, 02... 16` and handles WhatsApp chronological timestamps (`WhatsApp Image YYYY-MM-DD at HH.MM.SS (copy)`).
- **Strict Aspect-Ratio Preservation**: Never stretches, squashes, or distorts images. Images are automatically scaled to fit the printable A4 content box and centered.
- **Premium Editorial Design**:
  - Crisp white background (`#FFFFFF`) with dark charcoal typography (`#0F172A`).
  - Subtle hairline grey rules (`#E2E8F0`) separating headers and footers.
  - Minimalist cover page with customizable title, subtitle, author, and category badges.
  - Subtle running headers (document title and plate counter) and footers (`Page X of Y`).
  - Gallery-style presentation framing (`card`, `subtle_border`, `shadow`, or `none`).
- **EXIF & Alpha Handling**:
  - Automatically respects smartphone camera EXIF orientation tags.
  - Composites transparent PNG and WEBP images cleanly over white backgrounds (no black box artifacts).
- **Automated PyMuPDF Verification**: Built-in visual and structural audit verifying page counts, A4 dimensions, and image stream integrity.

---

## 📁 Project Structure

```
Image-to-PDF/
├── images/                                # Source image plates (01.jpg .. 16.jpg)
│   ├── 01.jpg .. 16.jpg                   # 16 High-resolution sequential images
│   └── README.md                          # Sequential plate index & slide titles
├── output/                                # Generated PDF deliverables
│   ├── Professional_Image_Collection.pdf  # Master compiled 17-page PDF (1 Cover + 16 Plates)
│   └── preview_page_*.png                 # High-DPI page render previews
├── config.json                            # Optional JSON configuration file
├── main.py                                # Production image-to-PDF engine
├── requirements.txt                       # Project dependencies
└── README.md                              # Complete documentation & usage guide
```

---

## ⚡ Quick Start & Terminal Commands

### 1. Install Dependencies
Open PowerShell or your preferred terminal in the project directory:
```powershell
cd "C:\Users\AdMin\Image-to-PDF"
python -m pip install -r requirements.txt
```

### 2. Generate the PDF (Default 16 Images)
Run the application with default settings:
```powershell
python main.py
```
This automatically:
1. Reads all 16 images from `images/`
2. Sorts them naturally (`01.jpg` to `16.jpg`)
3. Typesets Page 1 (Cover) + 16 individual plate pages
4. Saves the compiled PDF to:
   `output/Professional_Image_Collection.pdf`
5. Runs automated validation verifying 17 pages and 16 image streams.

---

## 🛠️ CLI Customization Options

The application is fully customizable via command-line arguments:

```powershell
# Custom Title and Subtitle
python main.py --title "Annual Visual Portfolio" --subtitle "Curated Photography & Graphic Plates"

# Convert a custom external image directory (e.g., WhatsApp collection)
python main.py "c:\Users\AdMin\Downloads\globla_culture6641" --output "output/Global_Culture_Downloads.pdf"

# Generate an image-only document without a cover page
python main.py --no-cover --output "output/Plates_Only.pdf"

# Select an alternative design theme (minimalist, editorial, academic, dark_luxury)
python main.py --theme editorial --framing subtle_border

# Automatically open the PDF in your default system viewer when done
python main.py --open

# Load settings from a JSON configuration file
python main.py --config config.json
```

### CLI Options Reference

| Argument | Shorthand | Default | Description |
| :--- | :--- | :--- | :--- |
| `images_dir_pos` | *positional* | `images` | Optional positional folder path to source images |
| `--images-dir` | `-i` | `images` | Path to folder containing source images |
| `--output` | `-o` | `output/Professional_Image_Collection.pdf` | Destination PDF path |
| `--title` | `-t` | `Professional Image Collection` | Document title |
| `--subtitle` | `-s` | `Curated High-Resolution Visual Documentation...` | Document subtitle |
| `--author` | `-a` | `Editorial Studio Series` | Author or series name |
| `--category` | `-c` | `Visual Archive & Plate Collection` | Overline category badge on cover |
| `--theme` | | `minimalist` | Theme preset (`minimalist`, `editorial`, `academic`, `dark_luxury`) |
| `--framing` | | `card` | Plate framing style (`card`, `subtle_border`, `shadow`, `none`) |
| `--no-cover` | | `False` | Omit cover page and generate plates only |
| `--config` | | `None` | Path to optional JSON configuration file |
| `--no-validate`| | `False` | Skip automated PyMuPDF validation |
| `--open` | | `False` | Automatically launch default PDF viewer upon completion |

---

## 🎨 Configuration File (`config.json`)

You can persist document settings in `config.json`:
```json
{
  "title": "Professional Image Collection",
  "subtitle": "Curated High-Resolution Visual Documentation & Archival Plates",
  "author": "Antigravity Publishing Team",
  "category": "Visual Archive Series",
  "theme": "minimalist",
  "framing": "card",
  "images_dir": "images",
  "output": "output/Professional_Image_Collection.pdf",
  "highlights": [
    "Sequential 16-Plate Curated Visual Documentation",
    "Distortion-Free Aspect-Ratio Preservation",
    "A4 Standard Publication-Grade Vector Typesetting",
    "Adaptive Portrait & Landscape Geometry Engine",
    "Optimized Document Stream Compression with Calibrated Colors",
    "Automated Structural & Visual Integrity Verification"
  ]
}
```

---

## 🔍 Verification & Audit Report

Running the compilation executes an automated deep structural audit:

- **Source Images Discovered**: 16 images (`01.jpg` through `16.jpg`)
- **Total Document Pages**: 17 pages (1 Cover + 16 Image Plates)
- **Page Dimensions**: Exactly A4 standard ($595.28 \times 841.89\text{ pt}$) across all 17 pages
- **Image Streams**: 16 verified embedded image streams (1 plate per image page, 0 missing)
- **Output File Size**: ~2.38 MB (lossless direct embedding without generation quality loss)
