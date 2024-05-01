import os
from unittest.mock import patch
import api

# Define the path to a sample image for testing
IMAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "machine-learning-client", "test_png", "photo2.png"))

def test_analyze_image():
    """
    Test to see if analyze image returns an age, not necessarily the correct one
    """
    # Mock the DeepFace library's analyze method
    with patch("api.DeepFace.analyze") as mock_analyze:
        mock_analyze.return_value = [{
            "age": 30,
            "dominant_gender": "Male",
            "dominant_emotion": "Happy",
            "dominant_race": "Asian"
        }]

        # Call the analyze_image function with the sample image path
        result = api.analyze_image(IMAGE_PATH)

        # Assert that the result is as expected
        assert result == [30, "Male", "Happy", "Asian"], "Test failed: The analyze_image function did not return expected results"
