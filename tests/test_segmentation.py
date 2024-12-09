from segmentation import segment_image

def test_segmentation():
    result = segment_image("data/input/test_image.jpg")
    assert result is not None
