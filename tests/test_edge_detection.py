from edge_detection import detect_edges

def test_edge_detection():
    result = detect_edges("data/input/test_image.jpg")
    assert result is not None
