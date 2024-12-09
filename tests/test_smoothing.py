from smoothing import apply_smoothing

def test_smoothing():
    result = apply_smoothing("data/input/test_image.jpg")
    assert result is not None
