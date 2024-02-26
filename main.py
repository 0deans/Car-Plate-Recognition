from ultralytics import YOLO

model = YOLO('yolov8n.yaml')

model.train(data='config.yaml', epochs=1)

model.save("detected_licence_number")