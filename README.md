# Birdwatcher

## Project Overview

This project is an Internet of Things (IoT) system designed to detect motion using a Raspberry Pi and PIR sensor, capture images, and analyze them using a cloud-based Custom Vision AI model. The system detects motion, takes a picture, scans the picture with Custom Vision AI, if a bird is detected the image will be uploaded to Blob Storage (otherwise stored locally), metadata is sent to Azure.

## Features

- Motion detection via PIR sensor on Raspberry Pi  
- Automatic image capture and storage  
- Cloud upload (Azure Blob & IoT Hub)  
- Integration with Custom Vision AI for image classification  
- Informational flow tracking and basic alerting/logging  

## 🛠️ Technologies Used

- **Hardware:** Raspberry Pi 4, PIR Sensor, Pi Camera  
- **Languages:** Python  
- **Cloud:** Azure (Custom Vision + Blob Storage) 

## System Logic Flow

1. **Idle:** The system waits for motion via PIR sensor.  
2. **Triggered:** When motion is detected, a photo is captured.    
3. **Classification:** The Custom Vision AI service analyzes the image.
4. **Processing:** If a bird is detected, the picture is sent to cloud storage.
5. **Output:** Based on classification, the result is logged or sent to a user system.

## Diagram Slides

See the `/diagrams` or `/slides` folder for:
- Block-level architecture  
- Algorithm/logic flowchart  
- Information flow diagram

## How to Run

1. Connect the PIR sensor and camera to the Raspberry Pi.  
2. Clone this repository onto the Raspberry Pi.  
3. Set up a Python environment and install dependencies (see requirements.txt)

    ```bash
    pip install -r requirements.txt
    ```

4. Configure cloud credentials and endpoints in `config.py eg. connections strings, device ID. etc. 
5. Run the main detection script:

    ```bash
    python app.py
    ```

## Sample Output

### Bird Detected ###
![Sample Output](bird_images/bird-detected.jpg)

### No Bird Detected ###
![Sample Output](bird_images/unsuccessful.jpg)

## 📌 Notes

- For best performance, test in a well-lit environment.  
- Camera angle and PIR sensor range may need manual adjustment.  
- Ensure cloud billing caps are in place to avoid unexpected charges.
