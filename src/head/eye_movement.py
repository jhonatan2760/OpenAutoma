import RPi.GPIO as GPIO
import time

# GPIO pin for the servo signal
SERVO_PIN = 18

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Set up PWM on the servo pin (50 Hz frequency)
pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

def set_servo_angle(angle):
    duty = angle / 18 + 2  # Convert angle to duty cycle
    GPIO.output(SERVO_PIN, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.3)  # Allow time for the servo to move
    GPIO.output(SERVO_PIN, False)
    pwm.ChangeDutyCycle(0)

try:
    while True:
        # Move servo to the left (e.g., 0 degrees)
        set_servo_angle(0)
        time.sleep(1)

        # Move servo to the right (e.g., 180 degrees)
        set_servo_angle(180)
        time.sleep(1)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()