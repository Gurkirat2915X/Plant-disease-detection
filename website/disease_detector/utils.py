from PIL import Image
from ultralytics import YOLO
from django.conf import settings
import json

def detector(image,id):
    model = YOLO(settings.MEDIA_ROOT+"//models//best.pt")
    
    try:
        result = model(Image.open(image).convert('RGB'))
        print("detector working")
        print(result)
        result_conv = json.loads(result[0].to_json())[0]
        result[0].save(settings.MEDIA_ROOT+"//detection_images//"+str(id)+".jpg")
        result_dict = {'name' : result_conv['name'],'confidence' : float(result_conv['confidence'])*100,'image' : "//detection_images//"+str(id)+".jpg"}
        return result_dict
    except Exception as e:
        print(e)
        return {'name' : None,'confidence' : 0,'image' : None}

