# birdwatcher
#### Robert O'Donnell 20089483

This project implements an IoT-based bird monitoring system using a Raspberry Pi 4 equipped with a camera module and a PIR motion sensor. When motion is detected near a bird feeder, the system captures an image and securely transmits it to an Azure IoT Hub using MQTT. The images are stored in Azure, and telemetry data, including motion timestamps, is visualized using Power BI or Azure Time Series Insights. Additionally, Azure Functions can process the images to notify users via email or SMS. An AI-based bird species recognition model using Azure Custom Vision is used by the system to identify birds before sending alerts. 

## Tools, Technologies and Equipment

### Hardware
- Raspberry Pi 4
- Camera Module
- Motion Sensor

### Software
- Python - for scripting
- MQTT - for secure messaging between Raspberry Pi and Azure IoT Hub
- Azure IoT Hub - for telemetry transmission
- Azure Functions - to analyse and send alerts
- Azure Custom Vision AI - to recognise birds
- Email/SMS API - to notify user of bird encounters




