# ocr.py
# Скриншоттан 'km' немесе 'км' көрсетілген қашықтықты OCR арқылы тану

import pytesseract
from PIL import Image
import re

def extract_km_from_image(image_path):
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        text = text.replace(",", ".")  # , → . (мысалы, 3,2 км → 3.2 км)

        # Барлық "сан + km/км" шаблондарын іздеу
        matches = re.findall(r"(\d+\.\d+|\d+)\s?(km|км)", text, re.IGNORECASE)

        if matches:
            # Алғашқы табылған мәнді аламыз
            distance = matches[0][0]  # Мысалы: "3.2"
            return float(distance)
        return None
    except Exception as e:
        print(f"OCR error: {e}")
        return None
