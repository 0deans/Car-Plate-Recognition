from ultralytics import YOLO
import torch

if __name__ == '__main__':
    print(torch.cuda.is_available())
    print(torch.__version__)
    print(torch.version.cuda)

    model = YOLO('yolov8m.yaml')

    model.train(data='config.yaml', epochs=3, batch=-1)

    model.save("detected_licence_number")