"""
Need these modules for the tests to work
"""
import sys
import os
import pytest
from api_server import app
from unittest.mock import patch


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

IMAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",
                                           "test_png", "tester_photo2.png"))

@pytest.fixture(name="testing_app")
def testing_app_fixture():
    """
    Fixture to provide Flask application for testing
    """
    test_app = app
    test_app.config.update({
        "TESTING": True,
    })
    yield test_app

@pytest.fixture(name="client")
def client_fixture(testing_app):
    """
    Fixture to create a test client for the Flask app
    """
    # Set up the Flask app for testing
    return testing_app.test_client()

def test_analyze_success(client):
    """
    Test the analyze endpoint with a successful analysis
    """
    # Correctly patch the analyze_image function used within the Flask app
    with patch("api.analyze_image", return_value=[25, "Male", "Happy", "Asian"]) as mock_analyze:
        # Ensure you're sending the file under the correct form name expected by the Flask route
        with open(IMAGE_PATH, "rb") as image_file:
            data = {
                "file": (image_file, "tester_photo.png")  # Change "image" to "file" if that's what your Flask route expects
            }
            response = client.post("/analyze", data=data, content_type='multipart/form-data')

        # Check that the response status code is 200 and the result matches the expected value
        assert response.status_code == 200
        assert response.json == {
            "predicted_age": 25,
            "predicted_gender": "Male",
            "dominant_emotion": "Happy",
            "predicted_race": "Asian"
        }, "Test failed: The response did not match the expected JSON"

        # Ensure the function was called once
        mock_analyze.assert_called_once()