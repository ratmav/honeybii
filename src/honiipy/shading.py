"""shaded ascii: render an image as shaded ascii text."""

from PIL import Image

from honiipy._gradients import GRADIENTS, ONE_TO_ONE_MAX, STYLES


def load_gray(path) -> Image.Image:
    """open an image as 8-bit grayscale (pillow 'L', 0-255)."""
    return Image.open(path).convert("L")


def pixelate(img: Image.Image, point_size: int) -> Image.Image:
    """resize to the char grid; rows use point_size*2 for aspect correction."""
    columns = img.width // point_size
    rows = img.height // (point_size * 2)
    return img.resize((columns, rows), Image.Resampling.LANCZOS)


def intensity_range(img: Image.Image) -> tuple[int, int]:
    """(min, max) pixel intensity of a grayscale image."""
    return img.getextrema()


def _round_half_up(value: float) -> int:
    """round half away from zero (index args are always >= 0)."""
    return int(value + 0.5)


def relative_index(value: int, low: int, high: int, gradient_size: int) -> int:
    """relative style: stretch intensity across the image's own [low, high]."""
    if high == low:
        raise ValueError("flat image has no intensity range for relative style")
    return _round_half_up(gradient_size * (value - low) / (high - low))


def one_to_one_index(value: int, gradient_size: int) -> int:
    """one_to_one style: map intensity across the full 0-255 range."""
    return _round_half_up(gradient_size * value / ONE_TO_ONE_MAX)


def _indexer(img: Image.Image, ramp: list[str], style: str):
    """pick the per-pixel index function for the chosen style."""
    size = len(ramp) - 1
    if style == "relative":
        low, high = intensity_range(img)
        return lambda v: relative_index(v, low, high, size)
    return lambda v: one_to_one_index(v, size)


def _join_rows(chars: list[str], width: int) -> str:
    """chunk a row-major char list into newline-joined lines."""
    lines = [chars[i : i + width] for i in range(0, len(chars), width)]
    return "\n".join("".join(line) for line in lines)


def to_ascii(img: Image.Image, gradient: int = 0, style: str = "relative") -> str:
    """render a grayscale image to shaded ascii."""
    if style not in STYLES:
        raise ValueError(f"style must be one of {STYLES}")
    if not 0 <= gradient < len(GRADIENTS):
        raise ValueError(f"gradient must be 0..{len(GRADIENTS) - 1}")
    ramp = GRADIENTS[gradient]
    indexer = _indexer(img, ramp, style)
    chars = [ramp[indexer(v)] for v in img.get_flattened_data()]
    return _join_rows(chars, img.width)


def shade(
    path, point_size: int = 12, gradient: int = 0, style: str = "relative"
) -> str:
    """turn an image path into shaded ascii."""
    img = pixelate(load_gray(path), point_size)
    return to_ascii(img, gradient, style)
