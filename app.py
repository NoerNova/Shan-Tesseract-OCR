from pathlib import Path
from typing import List

import gradio as gr
import pytesseract
from PIL import Image

from preprocessing import preprocess_image

_TESSDATA_DIR = Path(__file__).parent / "tessdata"
_LANG_CONFIG = f"--tessdata-dir {_TESSDATA_DIR}"


def tesseract_ocr(
    filepath: str,
    languages: List[str],
    enable_preprocess: bool,
    do_scale: bool,
    target_dpi: int,
    do_grayscale: bool,
    do_denoise: bool,
    contrast: float,
    sharpness: float,
    do_binarize: bool,
    oem: int,
    psm: int,
) -> str:
    if filepath is None:
        return "Please upload an image."
    if not languages:
        return "Please select at least one language."
    try:
        config = f"--oem {oem} --psm {psm} --tessdata-dir {_TESSDATA_DIR}"
        with Image.open(filepath) as img:
            if enable_preprocess:
                image = preprocess_image(
                    img,
                    do_scale=do_scale,
                    target_dpi=target_dpi,
                    do_grayscale=do_grayscale,
                    do_denoise=do_denoise,
                    contrast=contrast,
                    sharpness=sharpness,
                    do_binarize=do_binarize,
                )
            else:
                image = img.convert("RGB")

            return pytesseract.image_to_string(
                image=image,
                lang="+".join(languages),
                config=config,
            )
    except Exception as e:
        return f"OCR failed: {e}"


title = "Shan Tesseract OCR"
description = "Gradio demo for Tesseract-OCR Shan. Tesseract is an open source text recognition (OCR) Engine."
article = "<p style='text-align: center'><a href='https://tesseract-ocr.github.io/' target='_blank'>Tesseract documentation</a> | <a href='https://github.com/tesseract-ocr/tesseract' target='_blank'>Github Repo</a></p>"

# examples: [image_path, languages, enable_preprocess, do_scale, target_dpi, do_grayscale, do_denoise, contrast, sharpness, do_binarize, oem, psm]
examples = [
    ["examples/example1.png", ["eng", "shn"], False, True, 252, False, False, 1.0, 1.2, False, 3, 11],
    ["examples/example2.png", ["eng", "shn"], True, True, 252, False, False, 1.0, 1.2, False, 3, 6],
    ["examples/example3.png", ["eng", "shn"], False, True, 252, False, False, 1.0, 1.2, False, 3, 6],
    ["examples/example4.png", ["eng", "shn"], False, True, 252, False, False, 1.0, 1.2, False, 3, 6],
    ["examples/example5.jpg", ["eng", "shn"], True, True, 300, False, True, 1.8, 2.7, False, 3, 6],
]

with gr.Blocks(title=title) as demo:
    gr.Markdown(f'<h1 style="text-align: center; margin-bottom: 1rem;">{title}</h1>')
    gr.Markdown(description)
    with gr.Row():
        with gr.Column():
            image = gr.Image(type="filepath", label="Input")
            language_choices = pytesseract.get_languages(config=_LANG_CONFIG)
            with gr.Accordion("Languages", open=False):
                languages = gr.CheckboxGroup(language_choices, type="value", value=["eng", "shn"], label='language')
            with gr.Accordion("Preprocessing", open=False):
                enable_preprocess = gr.Checkbox(label="Enable Preprocessing", value=False)
                do_scale = gr.Checkbox(label="Auto-scale to target DPI", value=True)
                target_dpi = gr.Slider(minimum=72, maximum=600, value=252, step=1, label="Target DPI")
                do_grayscale = gr.Checkbox(label="Grayscale", value=False)
                do_denoise = gr.Checkbox(label="Denoise (Median filter)", value=False)
                contrast = gr.Slider(minimum=0.5, maximum=3.0, value=1.0, step=0.1, label="Contrast")
                sharpness = gr.Slider(minimum=0.5, maximum=3.0, value=1.2, step=0.1, label="Sharpness")
                do_binarize = gr.Checkbox(label="Binarize (Otsu's threshold)", value=False)
            with gr.Accordion("OCR Engine", open=False):
                oem = gr.Radio(
                    choices=[
                        ("0 — Legacy only", 0),
                        ("1 — LSTM only", 1),
                        ("2 — Legacy + LSTM", 2),
                        ("3 — Default (Legacy + LSTM)", 3),
                    ],
                    value=3,
                    label="OEM — OCR Engine Mode",
                )
                psm = gr.Dropdown(
                    choices=[
                        ("0 — OSD only", 0),
                        ("1 — Auto OSD", 1),
                        ("3 — Fully auto (no OSD)", 3),
                        ("4 — Single column", 4),
                        ("5 — Single vert. block", 5),
                        ("6 — Single uniform block", 6),
                        ("7 — Single text line", 7),
                        ("8 — Single word", 8),
                        ("9 — Single word (circle)", 9),
                        ("10 — Single char", 10),
                        ("11 — Sparse text", 11),
                        ("12 — Sparse + OSD", 12),
                        ("13 — Raw line", 13),
                    ],
                    value=6,
                    label="PSM — Page Segmentation Mode",
                )
            with gr.Row():
                btn_clear = gr.ClearButton([image, languages])
                btn_submit = gr.Button(value="Submit", variant="primary")
        with gr.Column():
            text = gr.Textbox(label="Output", lines=10)

    btn_submit.click(
        tesseract_ocr,
        inputs=[image, languages, enable_preprocess, do_scale, target_dpi, do_grayscale, do_denoise, contrast, sharpness, do_binarize, oem, psm],
        outputs=text,
        api_name="tesseract-ocr",
        show_progress="minimal",
    )
    btn_clear.add(text)

    gr.Examples(
        examples=examples,
        inputs=[image, languages, enable_preprocess, do_scale, target_dpi, do_grayscale, do_denoise, contrast, sharpness, do_binarize, oem, psm],
    )

    gr.Markdown(article)

if __name__ == '__main__':
    demo.launch()
