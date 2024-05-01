# test_app.py
import pytest
import threading
import time
from unittest.mock import patch, MagicMock 
from webApp.app import app, allowed_file, process_task, generate_fun_message, openai


class TestConfig:
    SECRET_KEY = "test_secret_key"


@pytest.fixture(name="testing_app")
def testing_app_fixture():
    """
    Test app for other function tests
    """
    test_app = app
    test_app.config.from_object(TestConfig)  # Use the test configuration
    test_app.config["TESTING"] = True
    return test_app



IMAGE_PATH = "test_png/tester_photo.png"


@pytest.fixture(name="client")
def client_fixture(testing_app):
    """
    Test client for other function tests
    """
    return testing_app.test_client()

@pytest.fixture(name="task_queue")
def task_queue_fixture():
    """
    Test queue for tasks
    """
    test_queue = []
    yield test_queue

# Test function for allowed_file
def test_allowed_file():
    """
    Test allowed_file function
    """
    assert allowed_file("test.png"), "Test case failed: allowed_file('test.png')"
    assert allowed_file("test.jpg"), "Test case failed: allowed_file('test.jpg')"
    assert allowed_file("test.jpeg"), "Test case failed: allowed_file('test.jpeg')"
    assert allowed_file("test.gif"), "Test case failed: allowed_file('test.gif')"
    assert not allowed_file("test.txt"), "Test case failed: allowed_file('test.txt')"

# Test function for home route
def test_home(client):
    """
    Test home function
    """
    response = client.get('/')
    assert response.status_code == 200

# Test function for upload image route
def test_upload_image(client):
    """
    Test upload image page and functionality
    """
    response = client.get('/upload')
    assert response.status_code == 200

    with open(IMAGE_PATH, "rb") as image_file:
        data = {
            "age": (None, "30"),
            "image": (image_file, "tester_photo.png")
        }
        response = client.post("/upload", data=data)
    assert response.status_code == 400

# Test function for start_task route
def test_start_task(client):
    """
    Test start_task function
    """
    data = {"task_id": "12345"}
    response = client.post("/start_task", json=data)
    assert response.status_code == 202

# Test function for process_task function
def test_process_task(task_queue):
    """
    Test process_task function
    """
    task_queue.append("12345")
    threading.Thread(target=process_task, daemon=True).start()
    time.sleep(1)
    assert task_queue == ["12345"]

# Test function for get_result route
def test_get_result(client):
    """
    Test get_result function
    """
    task_id = "12345"
    response = client.get(f"/get_result/{task_id}")
    assert response.status_code == 202

    data = response.json
    assert data["task_id"] == task_id
    assert data["status"] == "Processing"

# Test function for generate_fun_message function (OpenAI)
@patch.object(openai.chat.completions, 'create')
def test_generate_fun_message(mock_create):
    # Configure the mock response
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Have a great day!"))]
    mock_create.return_value = mock_response

    # Call the function being tested
    prompt = "Generate a fun message for someone who is 30 years old and seems Happy."
    fun_message = generate_fun_message(prompt)

    # Assert that the API call was made with the correct arguments
    mock_create.assert_called_with(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    # Assert that the returned message is as expected
    assert fun_message == "Have a great day!"
