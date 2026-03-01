from pathlib import Path
from typing import List

import pytesseract
from PIL import Image

import gradio as gr

_TESSDATA_DIR = Path(__file__).parent / "tessdata"
_OCR_CONFIG = f"--oem 3 --psm 11 --tessdata-dir {_TESSDATA_DIR}"
_LANG_CONFIG = f"--tessdata-dir {_TESSDATA_DIR}"


def tesseract_ocr(filepath: str, languages: List[str]):
    if filepath is None:
        return "Please upload an image."
    if not languages:
        return "Please select at least one language."
    try:
        with Image.open(filepath) as image:
            image = image.convert("RGB")
            return pytesseract.image_to_string(
                image=image,
                lang="+".join(languages),
                config=_OCR_CONFIG,
            )
    except Exception as e:
        return f"OCR failed: {e}"


title = "Shan Tesseract OCR"
description = "Gradio demo for Tesseract-OCR Shan. Tesseract is an open source text recognition (OCR) Engine."
article = "<p style='text-align: center'><a href='https://tesseract-ocr.github.io/' target='_blank'>Tesseract documentation</a> | <a href='https://github.com/tesseract-ocr/tesseract' target='_blank'>Github Repo</a></p>"

examples = [
    ["examples/example2.png", ["eng", "shn"]],
    ["examples/example3.png", ["eng", "shn"]],
    ["examples/example4.png", ["eng", "shn"]],
    ["examples/example1.png", ["eng", "shn"]],
]

language_choices = pytesseract.get_languages(config=_LANG_CONFIG)

demo = gr.Interface(
    fn=tesseract_ocr,
    inputs=[
        gr.Image(type="filepath", label="Input"),
        gr.CheckboxGroup(language_choices, type="value", value=['eng'], label='language')
        ],
    outputs='text',
    title=title,
    description=description,
    article=article,
    examples=examples,
)

if __name__ == '__main__':
    demo.launch()
    print("Finished running")
