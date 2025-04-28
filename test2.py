from gpiozero import MotionSensor

pir = MotionSensor(5)

while True:
    pir.wait_for_motion()
    print("Sensor state: 1")
    pir.wait_for_no_motion()
    print("Sensor state: 0")