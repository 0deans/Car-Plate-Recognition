import cv2 as cv
from ultralytics import YOLO
import matplotlib.pyplot as plt
import pytesseract
import easyocr

pytesseract.pytesseract.tesseract_cmd = 'E:\\Tesseract-OCR\\tesseract.exe'

model = YOLO('model/best.pt')
img = cv.imread('source/car6.jpg')
result = model(img)
# kernel = cv.getStructuringElement(cv.MORPH_RECT, (9, 9))
last_nums = []
blackHats = []

reader = easyocr.Reader(['en'])


def get_kernel(image_width, image_height):
    kernel_size = int(0.1 * min(image_width, image_height))
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (kernel_size, kernel_size))
    return kernel


for r in result:
    boxes = r.boxes
    for box in boxes:
        print('box found')
        x, y, w, h = box.xyxy[0]
        x, y, w, h = int(x), int(y), int(w), int(h)

        img = cv.rectangle(img, (x, y), (w, h), (255, 0, 255), 3)

        roi = img[y:h, x:w]

        kernel = get_kernel(w, h)

        if roi.size != 0:
            blackhat = cv.morphologyEx(
                cv.cvtColor(roi, cv.COLOR_BGR2GRAY),
                cv.MORPH_BLACKHAT, kernel
            )

            blackHats.append(blackhat)

            # number = pytesseract.image_to_string(
            #     blackhat,
            #     config=r'--oem 3 -c tessedit_char_whitelist'
            #            r'=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
            # ).replace('\n', '')

            nRes = reader.readtext(blackhat, detail=0)
            if len(nRes) > 0:
                last_nums.append(nRes)

            # number = number.replace(' ', '')
            # print(number)
            #
            # if 5 < len(number) < 12:
            #     last_nums.append(number.upper())
            #     last_img = roi

print(last_nums)
# plt.imshow(img)
# plt.title(', '.join(last_nums))
# plt.show()

count = len(blackHats)
print(count)
f, p = plt.subplots(count + 1)

p[0].imshow(img)
for i in range(count):
    p[i + 1].imshow(blackHats[i], cmap='gray')

plt.show()
