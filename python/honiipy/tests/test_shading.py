import pytest
from PIL import Image

from honiipy import shading
from honiipy._gradients import GRADIENTS


def _gray(values, size):
    """build an 'L' image from a row-major list of 0-255 values."""
    img = Image.new("L", size)
    img.putdata(values)
    return img


def test_load_gray_converts_to_l(tmp_path):
    path = tmp_path / "rgb.png"
    Image.new("RGB", (4, 4), (200, 30, 90)).save(path)
    img = shading.load_gray(path)
    assert img.mode == "L"
    low, high = img.getextrema()
    assert low == high  # solid color -> uniform gray


def test_pixelate_dims():
    out = shading.pixelate(Image.new("L", (120, 120)), 12)
    assert out.size == (120 // 12, 120 // (12 * 2))  # (10, 5)


def test_intensity_range():
    assert shading.intensity_range(_gray([0, 50, 200, 255], (4, 1))) == (0, 255)


def test_round_half_up_rounds_away_from_zero():
    # python's round() is banker's: round(0.5) == 0, round(2.5) == 2.
    assert [shading._round_half_up(v) for v in (0.5, 1.5, 2.5)] == [1, 2, 3]


def test_index_functions():
    assert shading.one_to_one_index(0, 3) == 0
    assert shading.one_to_one_index(255, 3) == 3
    assert shading.relative_index(50, 50, 200, 3) == 0
    assert shading.relative_index(200, 50, 200, 3) == 3
    assert shading.relative_index(125, 50, 200, 3) == 2  # 3 * 0.5 -> half-up 2
    with pytest.raises(ValueError):
        shading.relative_index(128, 128, 128, 3)


def test_to_ascii_one_to_one_exact():
    # gradient 3 = list("01  "); index = half_up(3 * v / 255)
    img = _gray([0, 85, 170, 255], (4, 1))
    assert shading.to_ascii(img, gradient=3, style="one_to_one") == "01  "


def test_to_ascii_rejects_bad_args():
    img = _gray([0, 255], (2, 1))
    with pytest.raises(ValueError):
        shading.to_ascii(img, style="bogus")
    with pytest.raises(ValueError):
        shading.to_ascii(img, gradient=99)


@pytest.mark.parametrize("style", ["relative", "one_to_one"])
@pytest.mark.parametrize("gradient", range(4))
def test_to_ascii_shape_and_alphabet(gradient, style):
    img = _gray([0, 64, 128, 192, 255, 32, 96, 160], (4, 2))
    lines = shading.to_ascii(img, gradient=gradient, style=style).split("\n")
    assert len(lines) == 2
    assert all(len(line) == 4 for line in lines)
    assert set("".join(lines)) <= set(GRADIENTS[gradient])


def test_shade_dims(tmp_path):
    path = tmp_path / "grad.png"
    img = Image.new("L", (60, 120))
    img.putdata([(x * 255) // 59 for _ in range(120) for x in range(60)])
    img.save(path)
    lines = shading.shade(path, point_size=6, style="relative").split("\n")
    assert len(lines) == 120 // (6 * 2)  # 10 rows
    assert all(len(line) == 60 // 6 for line in lines)  # 10 cols


def test_shade_flat_image(tmp_path):
    path = tmp_path / "flat.png"
    Image.new("L", (48, 48), 128).save(path)
    with pytest.raises(ValueError):
        shading.shade(path, point_size=4, style="relative")  # no relative range
    art = shading.shade(path, point_size=4, style="one_to_one")
    assert len(set(art.replace("\n", ""))) == 1  # uniform solid block
