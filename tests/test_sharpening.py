from sharpening import apply_sharpening

def test_sharpening():
    result = apply_sharpening("data/input/test_image.jpg")
    assert result is not None
