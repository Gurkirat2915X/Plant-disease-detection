from ultralytics import YOLO,SAM
import torch
model = YOLO("Plant-disease-detection/models/best.pt")
result = model("Plant-disease-detection/imgs/image.png")
result[0].show()