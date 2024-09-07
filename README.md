# spacex-telemetry-extractor
[WIP] Rocket Telemetry Extractor

## Overview

This project aims to extract telemetry data from SpaceX launch webcasts. It focuses on:

- Stage 1 Speed
- Stage 1 Altitude
- Timestamp
- Stage 2 Speed
- Stage 2 Altitude

The extracted data is formatted into CSV for easy analysis.

## Regions of Interest
Launch companies do not share the same overlay during their webcasts. Even SpaceX doesn't have the same overlay for Falcon launches and Starship.
That's why I started this project by writing ROI_setup.py. A tool used to calibrate the various regions of interest, basically where we will be looking for our telemetry data.

![image_processing](https://github.com/user-attachments/assets/f2a29cb9-8366-465e-bbc5-e8c33e78415c)

## Image Processing
A challenge I faced was the semi-transparent nature of the overlay, which, during bright camera shots, made character recognition by Tesseract quite difficult. To address this, I worked on an Image Processing Algorithm that effectively enhances the visibility of the text, improving OCR accuracy.

  - Grayscale Conversion: Each ROI is converted to grayscale to enhance text recognition.
  - Inversion: Images are inverted to improve OCR performance on dark backgrounds.
    
If initial OCR fails or returns low-confidence results, the script applies a white color mask to isolate potential white text against darker backgrounds, enhancing readability. Still working on it.

## Tesserect OCR
Utilizes Tesseract for optical character recognition within the defined ROIs. Assuming a single uniform block of text (psm 6). Configured to recognize only numbers and colons for cleaner output.

## CSV Extraction
The CSV file, named telemetry.csv, is created in the same directory and contains the following columns:

Stage 1 Speed (km/h): Speed of the first stage (booster) of the rocket.
Stage 1 Altitude (km): Altitude of the first stage above sea level.
Timestamp: Time elapsed since the launch. (HH:MM:SS)
Stage 2 Speed (km/h): Speed of the second stage
Stage 2 Altitude (km): Altitude of the second stage 

If any data point fails to be extracted, a null value is recorded in its place within the CSV row to maintain column consistency.

## Ongoing Work

Starship: Calibration and extraction tailored for Starship telemetry.

## Upcoming

Falcon: Specialized code for recent Falcon 9 and Falcon Heavy launches.
Falcon: Specialized code for older Falcon 9 and Falcon Heavy launches. (previous launch overlay)
