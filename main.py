import cv2 as cv
from ultralytics import YOLO
import easyocr
import matplotlib.pyplot as plt
import numpy as np

render_text = easyocr.Reader(['en'])
model = YOLO('model/best.pt')
img = cv.imread('source/car5.jpg')
kernel = np.ones((9, 9), np.uint8)

result = model(img)

for r in result:
    boxes = r.boxes
    for box in boxes:
        x, y, w, h = box.xyxy[0]
        x, y, w, h = int(x), int(y), int(w), int(h)
        img = img[y: h, x: w]

blackhat = cv.morphologyEx(img, cv.MORPH_BLACKHAT, kernel)
number = render_text.readtext(blackhat, detail=0)

print(number)

plt.imshow(blackhat)
plt.title('Result')
plt.show()