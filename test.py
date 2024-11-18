from ultralytics import YOLO,SAM
import torch
model = YOLO("models/best.pt")
result = model("imgs/image.png")
result[0].show()