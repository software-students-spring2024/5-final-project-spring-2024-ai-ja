import os
import pytest
from unittest.mock import patch, MagicMock
import sys

# Ensure the app module is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import app, allowed_file

# Path to a test image
IMAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../test_png", "tester_photo.png"))

@pytest.fixture
def client():
    app.config.update({
        "TESTING": True,
        "DEBUG": True,
    })
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Ensure the home page can be accessed."""
    response = client.get('/')
    assert response.status_code == 200
    assert 'Please upload your image to estimate your age' in response.get_data(as_text=True)

def test_allowed_file():
    """Validate that allowed_file function works for supported file types."""
    assert allowed_file("test.png")
    assert allowed_file("test.jpg")
    assert not allowed_file("test.txt")

@patch('gridfs.GridFS.put')
@patch('pymongo.collection.Collection.insert_one')
def test_upload_image(mock_insert_one, mock_put, client):
    """Simulate image uploading."""
    mock_put.return_value = 'mock_image_id'
    mock_insert_one.return_value = None

    with open(IMAGE_PATH, 'rb') as img:
        data = {'age': '30', 'image': (img, 'tester_photo.png')}
        response = client.post('/upload', data=data, content_type='multipart/form-data')
        assert response.status_code == 200

@patch('pymongo.collection.Collection.find_one')
def test_show_results_no_data(mock_find_one, client):
    """Check the behavior when no data is found for a given image ID."""
    mock_find_one.return_value = None
    response = client.get('/results/nonexistent_id')
    assert response.status_code == 302
    assert '/' in response.headers['Location']