import importlib
import sys
import threading
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Dynamically import the dash app instance from app.py
app_module = importlib.import_module("app")
app = app_module.app


@pytest.fixture(scope="module")
def shared_server():
    """Starts the Dash app in a background thread so selenium can access it locally."""
    # Run server on a fixed safe port (8050)
    server_thread = threading.Thread(
        target=lambda: app.run(port=8050, debug=False, use_reloader=False)
    )
    server_thread.daemon = True
    server_thread.start()
    time.sleep(3)  # Give server ample time to completely boot up
    yield "http://127.0.0.1:8050"


@pytest.fixture(scope="function")
def driver():
    """Configures a clean Headless Chrome Driver instance for each test context."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    driver_instance = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    yield driver_instance
    driver_instance.quit()


def test_header_present(shared_server, driver):
    """Test Case 1: Direct selenium check for the application header."""
    driver.get(shared_server)

    # Explicitly wait up to 10 seconds for the element to load in DOM
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "app-header"))
    )
    assert element is not None


def test_visualisation_present(shared_server, driver):
    """Test Case 2: Direct selenium check for the sales chart canvas."""
    driver.get(shared_server)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "sales-chart"))
    )
    assert element is not None


def test_region_picker_present(shared_server, driver):
    """Test Case 3: Direct selenium check for the radio buttons block."""
    driver.get(shared_server)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "region-filter"))
    )
    assert element is not None


if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))