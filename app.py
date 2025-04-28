import RPi.GPIO as GPIO
import time
import datetime
import os
import json
from dotenv import load_dotenv
from picamera import PiCamera
from azure.iot.device import IoTHubDeviceClient, Message
from msrest.authentication import ApiKeyCredentials
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.storage.blob import BlobServiceClient, ContentSettings

load_dotenv() # load env variables from .env

# --- Setup ---
PIR_PIN = 5
IMAGE_FOLDER = "/home/bobbyodd/birdwatcher/bird_images"

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

camera = PiCamera()
camera.rotation = 180
camera.resolution = (640, 480)

if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

# Azure IoT Hub setup
connection_string_iot = os.getenv("AZURE_IOT_HUB_CONNECTION_STRING")
device_client = IoTHubDeviceClient.create_from_connection_string(connection_string_iot)
device_client.connect()

# Azure Custom Vision setup
prediction_url = os.getenv("CUSTOM_VISION_PREDICTION_URL")
prediction_key = os.getenv("CUSTOM_VISION_PREDICTION_KEY")

parts = prediction_url.split('/')
endpoint = 'https://' + parts[2]
project_id = parts[6]
iteration_name = parts[9]

prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(endpoint, prediction_credentials)

# Azure Blob Storage setup
connection_string_blob = os.getenv("AZURE_BLOB_CONNECTION_STRING")
container_name = "images-container"

blob_service_client = BlobServiceClient.from_connection_string(connection_string_blob)
container_client = blob_service_client.get_container_client(container_name)

# --- Functions ---
def upload_bird_image(image_filename):
    blob_name = os.path.basename(image_filename)
    with open(image_filename, "rb") as data:
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(
            data,
            overwrite=True,
            content_settings=ContentSettings(content_type="image/jpeg")
        )
    print(f"Image '{blob_name}' uploaded successfully to '{container_name}'.")

# --- Main Loop ---
print("Motion sensor armed... Waiting for motion...")

try:
    while True:
        if GPIO.input(PIR_PIN):  # Motion detected
            print("Motion detected!")

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            image_path = f"{IMAGE_FOLDER}/bird_{timestamp}.jpg"

            camera.capture(image_path)
            print(f"Image saved: {image_path}")

            # Run prediction
            with open(image_path, "rb") as image_file:
                results = predictor.classify_image(project_id, iteration_name, image_file.read())

            predictions = {
                pred.tag_name: round(pred.probability * 100, 2)
                for pred in results.predictions
                if pred.probability > 0.5
            }

            for tag, prob in predictions.items():
                print(f"{tag}: {prob}%")

            if any(tag == "bird" for tag in predictions):
                print("Bird detected in image!")
                upload_bird_image(image_path)
            else:
                print("No bird detected, not uploading.")

            metadata = {
                "device_id": "feeder-pi",
                "timestamp": timestamp,
                "motion": True,
                "image_path": image_path,
                "predictions": predictions
            }

            msg = Message(json.dumps(metadata))
            device_client.send_message(msg)
            print("Metadata message sent to Azure IoT Hub.")

            # Wait for motion to stop
            print("Waiting for motion to stop...")
            while GPIO.input(PIR_PIN):
                time.sleep(0.1)

            print("No motion.")

        else:
            time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
    device_client.disconnect()
