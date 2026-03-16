import time
import random
import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

API_BASE_URL = "http://127.0.0.1:8000/api"

def get_admin_token():
    """Retrieve an admin JWT token to authorize PUT requests."""
    try:
        response = requests.post(f"{API_BASE_URL}/token/", json={
            "username": "admin", # Default django superuser 
            "password": "admin"  # Make sure to run createsuperuser with these credentials if you haven't 
        })
        if response.status_code == 200:
            return response.json().get("access")
        else:
            logging.error(f"Failed to get token: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        logging.error("Backend server is not running at http://127.0.0.1:8000")
        return None

def fetch_devices():
    """Fetch all registered IoT devices."""
    try:
        response = requests.get(f"{API_BASE_URL}/devices/")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logging.error(f"Failed to fetch devices: {e}")
    return []

def simulate_device_data(device, token):
    """Slightly fluctuate the device's temperature and humidity and PUT it."""
    # Add a small random drift (-1 to +1 degrees/percent)
    new_temp = round(device['temperature'] + random.uniform(-1.5, 1.5), 1)
    new_humidity = round(device['humidity'] + random.uniform(-2.0, 2.0), 1)

    # Keep values within realistic bounds
    new_temp = max(-10.0, min(new_temp, 50.0))
    new_humidity = max(10.0, min(new_humidity, 99.0))

    payload = {
        "id": device['id'],
        "name": device['name'],
        "temperature": new_temp,
        "humidity": new_humidity
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.put(f"{API_BASE_URL}/devices/", headers=headers, json=payload)
        if response.status_code == 200:
            logging.info(f"Simulated {device['name']}: Temp {new_temp}°C, Humidity {new_humidity}%")
        else:
            logging.warning(f"Failed to update {device['name']}: {response.text}")
    except Exception as e:
        logging.error(f"Error updating device: {e}")

def run_simulator():
    """Main simulation loop."""
    logging.info("Starting IoT Live Data Simulator...")
    
    token = get_admin_token()
    if not token:
        logging.error("Exiting. Please make sure the Django dev server is running and the 'admin'/'admin' superuser exists.")
        return

    while True:
        devices = fetch_devices()
        
        if not devices:
            logging.warning("No devices found from the API. Please add a device in the dashboard.")
            time.sleep(5)
            continue
            
        for device in devices:
            simulate_device_data(device, token)
            
        time.sleep(3) # Wait 3 seconds before next cycle

if __name__ == "__main__":
    run_simulator()
