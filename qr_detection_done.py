import cv2 as cv
import numpy as np
from pyzbar.pyzbar import decode

# Open the camera (Laptop webcam)
cap = cv.VideoCapture(0)  # Use 0 for the default camera
cap.set(3, 1080)  # Set width to 1080px

# Load authorized patient data from file
DATABASE_FILE = 'patient_database.txt'

def load_database():
    """Load patient database from a text file and normalize keys."""
    database = {}
    with open(DATABASE_FILE, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 4:  # Ensure the data has all fields
                patient_id = parts[0].strip().upper()  # Normalize key
                database[patient_id] = {
                    "name": parts[1].strip(),
                    "issue": parts[2].strip(),
                    "tray": parts[3].strip()
                }
    return database

# Load database
database = load_database()
print("Loaded Database:", database)

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture image from camera")
        break

    # Pre-process the image
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # Convert to grayscale
    blurred = cv.GaussianBlur(gray, (5, 5), 0)  # Apply Gaussian blur
    processed_img = cv.adaptiveThreshold(
        blurred, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2
    )

    # Decode barcodes from the processed image
    decoded_objects = decode(processed_img)

    for barcode in decoded_objects:
        patient_id_raw = barcode.data.decode('utf-8').strip()
        patient_id = patient_id_raw.split(',')[0].strip().upper()  # Extract just the ID


        print(f"Scanned raw: {repr(patient_id_raw)}, stripped/upper: {repr(patient_id)}")
        #print("Available Patient IDs:", list(database.keys()))
        

        # Get the rectangle coordinates
        rect = barcode.rect

        # Check if the patient ID exists in the database
        if patient_id in database:
            patient_data = database[patient_id]
            name = patient_data["name"]
            issue = patient_data["issue"]
            tray = patient_data["tray"]

            # Display patient data on the feed
            cv.putText(img, f"Name: {name}", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)
            cv.putText(img, f"Issue: {issue}", (50, 100), cv.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)
            cv.putText(img, f"Tray: {tray}", (50, 150), cv.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)

        else:
            # If the QR code is not recognized
            cv.putText(img, "Unrecognized QR Code", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Draw a polygon around the QR code
        if barcode.polygon:
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv.polylines(img, [pts], True, (255, 0, 0), 3)

    # Display the result
    cv.imshow('Patient Info Scanner', img)

    # Exit on pressing 'd'
    if cv.waitKey(20) & 0xFF == ord('d'):
        break

# Release resources
cap.release()
cv.destroyAllWindows()
