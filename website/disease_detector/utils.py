from PIL import Image
from ultralytics import YOLO
from django.conf import settings


def load_image(image_path):
    Image.open(image_path).convert('RGB').show()

def detector(image,):
    model = YOLO(settings.MEDIA_ROOT+"//models//best.pt")
    result = model(Image.open(image).convert('RGB'))
    print("detector working")
    print(result[0].to_json())
    print(type(result[0]))
    return result[0]
