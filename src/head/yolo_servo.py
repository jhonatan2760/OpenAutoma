import cv2
import torch
import RPi.GPIO as GPIO
import time
import pyttsx3

# Initialize GPIO for servo
SERVO_PIN = 18  # GPIO pin connected to the servo
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
pwm = GPIO.PWM(SERVO_PIN, 50)  # 50 Hz (20 ms PWM period)
pwm.start(0)
engine = pyttsx3.init()

# Set properties (optional)
engine.setProperty('rate', 150)  # Speed of speech (words per minute)
engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)

def speak(text):
    engine.say(text)
    engine.runAndWait()


# Function to set servo angle
def set_servo_angle(angle):
    duty = angle / 18 + 2  # Convert angle to duty cycle
    GPIO.output(SERVO_PIN, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)  # Allow time for the servo to move
    GPIO.output(SERVO_PIN, False)
    pwm.ChangeDutyCycle(0)
    
# Load YOLOv5n model (nano version for Raspberry Pi)
model = torch.hub.load('ultralytics/yolov5', 'yolov5n')  # Use YOLOv5 nano model

# Open webcam
cap = cv2.VideoCapture(0)  # Use 0 for the default webcam

# Main loop
try:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    while True:
        ret, frame = cap.read()
        time.sleep(1)
        if not ret:
            break

        # Perform object detection
        results = model(frame)

        # Parse detection results
        detections = results.xyxy[0].numpy()
        for detection in detections:
            x1, y1, x2, y2, conf, cls = detection
            label = model.names[int(cls)]
            print(f"Detected {label} with confidence {conf:.2f}")
            
            if conf > 0.3:
                speak(f"It's a {label} and my confidence is: {conf:.2f}")

            # Calculate the center of the detected object
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2

            # Move servo based on the object's position
            #if center_x < frame.shape[1] / 3:  # Object is on the left
            #    set_servo_angle(0)  # Move servo to 0 degrees
            #elif center_x > 2 * frame.shape[1] / 3:  # Object is on the right
            #    set_servo_angle(180)  # Move servo to 180 degrees
            #else:  # Object is in the center
            #    set_servo_angle(90)  # Move servo to 90 degrees

        # Display the frame
        #cv2.imshow('YOLO Object Detection', frame)
        #if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        #    break

finally:
    # Clean up
    cap.release()
    cv2.destroyAllWindows()
    pwm.stop()
    GPIO.cleanup()