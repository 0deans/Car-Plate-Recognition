import cv2 as cv
from ultralytics import YOLO
import matplotlib.pyplot as plt
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\Admin\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'

model = YOLO('model/best.pt')
img = cv.imread('source/car12.jpg')
result = model(img)
kernel = cv.getStructuringElement(cv.MORPH_RECT, (11, 5))
last_nums = []

for r in result:
    boxes = r.boxes
    for box in boxes:
        x, y, w, h = box.xyxy[0]
        x, y, w, h = int(x), int(y), int(w), int(h)

        img = cv.rectangle(img, (x, y), (w, h), (255, 0, 255), 3)

        roi = img[y:h, x:w]

        if roi.size != 0:
            blackhat = cv.morphologyEx(
                cv.cvtColor(roi, cv.COLOR_BGR2GRAY),
                cv.MORPH_BLACKHAT, kernel
            )

            number = pytesseract.image_to_string(
                blackhat,
                config=r'--oem 3 -c tessedit_char_whitelist'
                       r'=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
            ).replace('\n', '')

            number = number.replace(' ', '')

            if 5 < len(number) < 12:
                last_nums.append(number.upper())
                last_img = roi

print(last_nums)
plt.imshow(img)
plt.title(', '.join(last_nums))
plt.show()
