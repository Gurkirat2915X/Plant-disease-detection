from PIL import Image

def load_image(image_path):
    Image.open(image_path).convert('RGB').show()
