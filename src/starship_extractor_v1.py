import pytesseract
import cv2
import csv
import os
from natsort import natsorted
import re
import numpy as np

# Path to Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_number(text):
    return re.search(r'\d+', text).group() if re.search(r'\d+', text) else ""

def process_roi(roi, config='--psm 6'):
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray, config=config).strip()
    
    if not text:
        mask = cv2.inRange(roi, np.array([200, 200, 200]), np.array([255, 255, 255]))
        roi_masked = cv2.bitwise_and(roi, roi, mask=mask)
        gray_masked = cv2.cvtColor(roi_masked, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray_masked, config=config).strip()
    
    return ''.join(c for c in text if c.isdigit() or c == ':') or ""

def process_frame(frame_path, rois, output_csv='telemetry.csv'): #change output path here
    image = cv2.imread(frame_path)
    if image is None:
        return
    
    with open(output_csv, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if csvfile.tell() == 0:
            writer.writerow(["Booster Speed", "Booster Altitude", "Timestamp", "Ship Speed", "Ship Altitude"])

        row = [process_roi(image[y:y+h, x:x+w]) for x, y, w, h in rois]
        if len(row) == 5:
            writer.writerow(row)

# Define ROIs
rois = [
    (350, 904, 100, 40),  # BOOSTER SPEED
    (350, 942, 100, 40),  # BOOSTER ALTITUDE
    (902, 942, 170, 50),  # TIMESTAMP
    (1530, 904, 100, 40), # SHIP SPEED
    (1530, 942, 100, 40) # SHIP ALTITUDE
]

def main():
    frames_folder = 'frames_folder' #change input folder path here
    if not os.path.exists(frames_folder):
        return

    frame_files = natsorted([f for f in os.listdir(frames_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    for frame in frame_files:
        process_frame(os.path.join(frames_folder, frame), rois)

if __name__ == "__main__":
    main()