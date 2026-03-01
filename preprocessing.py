from PIL import Image, ImageEnhance, ImageFilter


def _compute_otsu_threshold(gray: Image.Image) -> int:
    histogram = gray.histogram()
    total = sum(histogram)
    if total == 0:
        return 128

    sum_all = sum(i * histogram[i] for i in range(256))
    sum_bg = 0
    count_bg = 0
    max_variance = 0.0
    threshold = 128

    for i in range(256):
        count_bg += histogram[i]
        if count_bg == 0:
            continue
        count_fg = total - count_bg
        if count_fg == 0:
            break
        sum_bg += i * histogram[i]
        mean_bg = sum_bg / count_bg
        mean_fg = (sum_all - sum_bg) / count_fg
        variance = count_bg * count_fg * (mean_bg - mean_fg) ** 2
        if variance > max_variance:
            max_variance = variance
            threshold = i

    return threshold


def preprocess_image(
    image: Image.Image,
    do_scale: bool,
    target_dpi: int,
    do_grayscale: bool,
    do_denoise: bool,
    contrast: float,
    sharpness: float,
    do_binarize: bool,
) -> Image.Image:
    # 1. Scale
    if do_scale:
        src_dpi = image.info.get("dpi", (72, 72))
        if isinstance(src_dpi, (tuple, list)):
            src_dpi = src_dpi[0]
        src_dpi = src_dpi or 72
        scale = min(target_dpi / src_dpi, 4.0)
        if scale != 1.0:
            new_w = int(image.width * scale)
            new_h = int(image.height * scale)
            image = image.resize((new_w, new_h), Image.LANCZOS)

    # 2. Grayscale (also required for binarize)
    if do_grayscale or do_binarize:
        image = image.convert("L")

    # 3. Denoise
    if do_denoise:
        image = image.filter(ImageFilter.MedianFilter(size=3))

    # 4. Contrast
    if contrast != 1.0:
        image = ImageEnhance.Contrast(image).enhance(contrast)

    # 5. Sharpness
    if sharpness != 1.0:
        image = ImageEnhance.Sharpness(image).enhance(sharpness)

    # 6. Binarize
    if do_binarize:
        if image.mode != "L":
            image = image.convert("L")
        thresh = _compute_otsu_threshold(image)
        image = image.point(lambda x: 255 if x >= thresh else 0, "L")

    return image.convert("RGB")
