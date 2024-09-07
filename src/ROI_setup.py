import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import cv2
import numpy as np

image = cv2.imread('telemetry_frame.png') #change image path here

#Change the Region Of Interests (ROI) here
rois = [
    (350, 904, 100, 40),  # STAGE 1 SPEED
    (350, 942, 100, 40),  # STAGE 1 ALTITUDE
    (902, 942, 170, 50),  # TIMESTAMP
    (1530, 904, 100, 40), # STAGE 2 SPEED
    (1530, 942, 100, 40) # STAGE 2 ALTITUDE
]

for i, (x, y, w, h) in enumerate(rois, 1):
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imwrite('image_with_rois.png', image)

for i, (x, y, w, h) in enumerate(rois, 1):
    roi = image[y:y+h, x:x+w]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    #cv2.imwrite(f'roi_{i}.png', gray_roi) - export for debugging purposes
    inverted = cv2.bitwise_not(gray_roi)
    #cv2.imwrite(f'inverted_roi_{i}.png', inverted) - export for degugging purposes
    
    config = '--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789:'
    text = pytesseract.image_to_string(inverted, config=config)
    
    if not text.strip() or len(text.strip()) == 0:
        lower_white = np.array([200, 200, 200])
        mask = cv2.inRange(roi, lower_white, np.array([255, 255, 255]))
        if mask.any(): 
            white_text = cv2.bitwise_and(roi, roi, mask=mask)
            gray_text = cv2.cvtColor(white_text, cv2.COLOR_BGR2GRAY)
            inverted = cv2.bitwise_not(gray_text)
            text = pytesseract.image_to_string(inverted, config=config)
            print(f"Data from ROI {i}: {text.strip()}")
    else:
        print(f"Data from ROI {i}: {text.strip()}")
