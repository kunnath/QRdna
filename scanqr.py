import cv2
from pyzbar.pyzbar import decode
import numpy as np  # Import NumPy for point handling

# Start video capture (0 is the default camera)
cap = cv2.VideoCapture(0)

print("Scanning for QR codes. Press 'q' to quit.")

while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    if not ret:
        break

    # Decode the QR codes in the frame
    decoded_objects = decode(frame)
    for obj in decoded_objects:
        # Extract the data from the QR code
        qr_data = obj.data.decode("utf-8")
        print(f"Decoded Data: {qr_data}")

        # Draw a rectangle around the QR code
        points = obj.polygon
        if len(points) == 4:  # Ensure it forms a quadrilateral
            # Convert points to a NumPy array with integer coordinates
            pts = np.array([(point.x, point.y) for point in points], dtype=np.int32)
            # Draw the rectangle
            cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=3)

        # Put the decoded data on the frame
        cv2.putText(frame, qr_data, (obj.rect.left, obj.rect.top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the video with QR code overlays
    cv2.imshow("QR Code Scanner", frame)

    # Quit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()