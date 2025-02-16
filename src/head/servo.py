import RPi.GPIO as GPIO
import time

SERVO_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

pwm = GPIO.PWM(SERVO_PIN, 50)  # 50 Hz (20 ms PWM period)
pwm.start(0)

def set_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(SERVO_PIN, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(SERVO_PIN, False)
    pwm.ChangeDutyCycle(0)

try:
    while True:
        set_angle(0)   # 0 degrees
        time.sleep(1)
        set_angle(90)  # 90 degrees
        time.sleep(1)
        set_angle(180) # 180 degrees
        time.sleep(1)
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()