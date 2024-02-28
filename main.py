import cv2 as cv
import numpy as np
from typing import List
from dataclasses import dataclass
from ultralytics import YOLO
import easyocr
from blacksheep import Application, post, FromFiles, bad_request, no_content, json
import uvicorn

app = Application()
model = YOLO('models/best.pt')
reader = easyocr.Reader(['en'])
ALLOWED_TYPES = ['image/jpeg', 'image/png']


@dataclass
class CarNumber:
    text: str
    image: bytes


@dataclass
class CarResponse:
    car_numbers: List[CarNumber] = None


def recognize_car_numbers(img) -> List[CarNumber]:
    result = model(img)
    car_numbers = []

    for r in result:
        boxes = r.boxes
        for box in boxes:
            x, y, w, h = map(int, box.xyxy[0])
            roi = img[y:h, x:w]

            if roi.size == 0:
                continue

            blackhat = cv.morphologyEx(
                cv.cvtColor(roi, cv.COLOR_BGR2GRAY),
                cv.MORPH_BLACKHAT,
                cv.getStructuringElement(cv.MORPH_ELLIPSE, (int(0.1 * min(w, h)), int(0.1 * min(w, h))))
            )

            plate_text = reader.readtext(blackhat, detail=0)
            plate_text = ''.join(plate_text).replace(' ', '')
            if 2 < len(plate_text) < 9:
                car_numbers.append(CarNumber(plate_text, cv.imencode('.jpg', blackhat)[1].tobytes()))

    return car_numbers


@post("/recognize")
def post_example(files: FromFiles):
    if not files.value:
        return bad_request("No files provided")

    file = files.value[0]
    content_type = file.content_type.decode('utf-8')

    if content_type not in ALLOWED_TYPES:
        return bad_request("Invalid file type. Only jpeg and png are allowed")

    img_array = np.frombuffer(file.data, np.uint8)
    img = cv.imdecode(img_array, cv.IMREAD_COLOR)
    car_numbers = recognize_car_numbers(img)

    if len(car_numbers) == 0:
        return no_content()

    return json(CarResponse(car_numbers))


if __name__ == '__main__':
    uvicorn.run("main:app", port=5000, log_level="info")
