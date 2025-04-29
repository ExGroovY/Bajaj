import pytesseract
from PIL import Image
import re

def extract_lab_tests(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))
    # Print the extracted text for debugging
    print("OCR Extracted Text:")
    print(text)
    
    # Adjust this regex as per your lab report format
    pattern = re.compile(
        r'([A-Za-z ()]+)\s+([0-9.]+)\s+([a-zA-Z%/]+)\s+([0-9.]+-[0-9.]+)'
    )

    results = []
    for match in pattern.finditer(text):
        test_name = match.group(1).strip()
        test_value = match.group(2).strip()
        test_unit = match.group(3).strip()
        bio_reference_range = match.group(4).strip()

        # Calculate if value is out of range
        ref_low, ref_high = map(float, bio_reference_range.split('-'))
        value = float(test_value)
        out_of_range = not (ref_low <= value <= ref_high)

        results.append({
            "test_name": test_name,
            "test_value": test_value,
            "bio_reference_range": bio_reference_range,
            "test_unit": test_unit,
            "lab_test_out_of_range": out_of_range
        })

    return results
