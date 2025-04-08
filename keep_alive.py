import requests
import time

# Replace with your deployed Render URL (make sure it points to a lightweight endpoint that runs quickly)
URL = "https://your-app-on-render.com/get-notes/your_test_page_id"

# Set the delay (in seconds) between pings. For example, 600 seconds = 10 minutes.
DELAY = 600

while True:
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            print("Ping successful!")
        else:
            print("Ping failed with status code:", response.status_code)
    except Exception as e:
        print("Error pinging:", e)
    time.sleep(DELAY)
