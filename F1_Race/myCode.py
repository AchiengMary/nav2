# === IMPORT LIBRARIES ===
import numpy as np
import cv2

# === CONSTANTS ===
Kp = 0.005  # proportional gain (you can tune this)
v = 0.2     # constant forward speed

# === MAIN LOOP ===
while True:
    # === GET IMAGE FROM CAMERA ===
    image = camera.getImage()   # Built-in Robotics Academy API
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    height, width, _ = image.shape

    # === DETECT RED LINE ===
    lower = np.array([17, 15, 100], dtype="uint8")
    upper = np.array([50, 56, 200], dtype="uint8")
    mask = cv2.inRange(image, lower, upper)

    # === FOCUS ON BOTTOM HALF OF IMAGE ===
    roi = mask[int(height * 0.6):height, :]

    # === FIND CONTOURS ===
    contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Pick largest contour (assume it's the line)
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)

        if M["m00"] > 0:
            # Center x of the line
            cx = int(M["m10"] / M["m00"])

            # === CALCULATE ERROR ===
            error = cx - (width // 2)

            # === PROPORTIONAL CONTROLLER ===
            w = -Kp * error

            # === SEND COMMANDS TO ROBOT ===
            motors.sendV(v)  # move forward
            motors.sendW(w)  # turn
        else:
            # If no good detection, stop
            motors.sendV(0)
            motors.sendW(0)
    else:
        # If no contours, stop
        motors.sendV(0)
        motors.sendW(0)

    # Optional: short sleep to avoid overloading CPU (uncomment if needed)
    # time.sleep(0.05)
