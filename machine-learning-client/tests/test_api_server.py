import os
import pytest
from api_server import app
from unittest.mock import patch

# Define the path to a sample image for testing
IMAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "test_png", "photo2.png"))

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_analyze_image_endpoint(client):
    """
    Test the /analyze_image endpoint of the API server
    """
    # Send a POST request to the /analyze_image endpoint with a test image
    response = client.post("/analyze_image", data={"image": open(IMAGE_PATH, "rb")})

    assert response.status_code == 404

    # Print the response data for debugging
    print(response.data)


def test_invalid_method_analyze_image_endpoint(client):
    """
    Test sending a GET request to the /analyze_image endpoint
    """
    # Send a GET request to the /analyze_image endpoint
    response = client.get("/analyze_image")
    assert response.status_code == 404


def test_missing_image_analyze_image_endpoint(client):
    """
    Test sending a POST request to the /analyze_image endpoint without an image
    """
    # Send a POST request to the /analyze_image endpoint without an image
    response = client.post("/analyze_image")

    assert response.status_code == 404