# Shan Tesseract OCR

A Gradio web application for optical character recognition (OCR) with first-class support for the **Shan language**, powered by [Tesseract OCR](https://tesseract-ocr.github.io/).

## Features

- **Multi-language OCR** — recognizes Shan (`shn`) and English (`eng`) out of the box; additional languages can be added by dropping `.traineddata` files into `tessdata/`
- **Image preprocessing pipeline** — optional per-image tuning before sending to Tesseract:
  - Auto-scale to a target DPI (up to 4×)
  - Grayscale conversion
  - Denoise with a median filter
  - Contrast and sharpness enhancement
  - Binarization via Otsu's threshold
- **OCR engine controls** — choose the OCR Engine Mode (OEM) and Page Segmentation Mode (PSM) directly from the UI
- **Two UI variants**:
  - `app.py` — full-featured Gradio Blocks interface with all preprocessing and engine controls
  - `app_interface.py` — lightweight Gradio Interface with sensible defaults

## Project Structure

```
.
├── app.py               # Full-featured Gradio Blocks UI
├── app_interface.py     # Minimal Gradio Interface UI
├── preprocessing.py     # Image preprocessing pipeline
├── tessdata/
│   ├── eng.traineddata  # English language data
│   └── shn.traineddata  # Shan language data
├── examples/            # Sample images for testing
├── requirements.txt     # Python dependencies
└── packages.txt         # System packages (for Hugging Face Spaces)
```

## Setup

### Prerequisites

- Python 3.8+
- Tesseract OCR installed on your system

**macOS**
```bash
brew install tesseract
```

**Ubuntu / Debian**
```bash
sudo apt-get install tesseract-ocr-all
```

### Installation

```bash
pip install -r requirements.txt
```

### Run

```bash
# Full UI with preprocessing controls
python app.py

# Minimal UI
python app_interface.py
```

Then open the URL printed in the terminal (default: `http://127.0.0.1:7860`).

## OCR Settings

### OCR Engine Mode (OEM)

| Value | Description |
|-------|-------------|
| 0 | Legacy engine only |
| 1 | LSTM neural net only |
| 2 | Legacy + LSTM |
| 3 | Default (Legacy + LSTM) |

### Page Segmentation Mode (PSM)

| Value | Description |
|-------|-------------|
| 0 | Orientation and script detection (OSD) only |
| 1 | Auto OSD |
| 3 | Fully automatic (no OSD) |
| 4 | Single column of text |
| 5 | Single vertical block |
| 6 | Single uniform block of text |
| 7 | Single text line |
| 8 | Single word |
| 9 | Single word in a circle |
| 10 | Single character |
| 11 | Sparse text |
| 12 | Sparse text + OSD |
| 13 | Raw line |

## Adding Languages

Place any Tesseract `.traineddata` file into the `tessdata/` directory and restart the app — the new language will appear automatically in the language selector.

Download additional language models from the [tesseract-ocr/tessdata](https://github.com/tesseract-ocr/tessdata) repository.

## Deployment on Hugging Face Spaces

This project is ready to deploy on [Hugging Face Spaces](https://huggingface.co/spaces/NorHsangPha/Shan-Tesseract-OCR):

- `packages.txt` installs `tesseract-ocr-all` as a system dependency
- `requirements.txt` installs Python dependencies

Select **Gradio** as the SDK and set the entry point to `app.py`.

## Dependencies

| Package | Version |
|---------|---------|
| gradio | 5.22.0 |
| pytesseract | 0.3.13 |
| Pillow | >=10.4.0 |

## References

- [Tesseract OCR documentation](https://tesseract-ocr.github.io/)
- [Tesseract GitHub repository](https://github.com/tesseract-ocr/tesseract)
