from PIL import Image
from ultralytics import YOLO
from django.conf import settings
import json
import nltk
from nltk.stem.porter import PorterStemmer
import numpy as np
import torch.nn as nn
import random
import torch


def detector(image, id):
    model = YOLO(settings.MEDIA_ROOT + "//models//best.pt")
    try:
        result = model(Image.open(image).convert("RGB"))
        result_conv = json.loads(result[0].to_json())[0]
        result[0].save(settings.MEDIA_ROOT + "/detection_images/" + str(id) + ".jpg")
        result_dict = {
            "name": result_conv["name"],
            "confidence": float(result_conv["confidence"]) * 100,
            "image": settings.MEDIA_ROOT + "/detection_images/" + str(id) + ".jpg",
            "class": result_conv["class"],
        }
        return result_dict
    except Exception as e:
        print(e)
        return {
            "name": None,
            "confidence": 0,
            "image": None,
            "class": 8,
        }



nltk.download("punkt_tab")
stemmer = PorterStemmer()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def tokenize(sentence):
    return nltk.word_tokenize(sentence)


def stem(word):
    return stemmer.stem(word.lower())


def bag_of_words(tokenized_sentence, all_words):
    tokenized_sentence = [stem(w) for w in tokenized_sentence]
    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, w in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1
    return bag


class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, num_classes)
        self.relu = nn.ReLU()

    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        return out


def chatbot(sentence):
    with open(settings.MEDIA_ROOT + "//Chatbot//intents.json", "r") as json_data:
        intents = json.load(json_data)
    FILE = settings.MEDIA_ROOT + "//Chatbot//data.pth"
    data = torch.load(FILE)
    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data["all_words"]
    tags = data["tags"]
    model_state = data["model_state"]
    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()
    bot_name = "AgriBot"

    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                return f"{bot_name}: {random.choice(intent['responses'])}"
    else:
        return f"{bot_name}: I do not understand..."


care_tips = {
    0: {
        "disease": "Tomato Early Blight",
        "cure": [
            "Remove infected leaves immediately",
            "Apply copper-based or chlorothalonil fungicides",
            "Ensure proper spacing between plants",
        ],
    },
    1: {
        "disease": "Tomato Septoria Leaf Spot",
        "cure": [
            "Remove infected leaves",
            "Apply fungicides containing chlorothalonil",
            "Copper-based sprays for organic gardens",
        ],
    },
    2: {"disease": "Tomato Leaf", "cure": []},
    3: {
        "disease": "Tomato Bacterial Spot",
        "cure": [
            "Copper fungicides application",
            "Remove severely infected plants",
            "Improve drainage",
        ],
    },
    4: {
        "disease": "Tomato Late Blight",
        "cure": [
            "Apply fungicides containing chlorothalonil or copper",
            "Remove infected plants immediately",
            "Dispose of infected material properly",
        ],
    },
    5: {
        "disease": "Tomato Mosaic Virus",
        "cure": ["No cure available; remove infected plants", "Control insect vectors"],
    },
    6: {
        "disease": "Tomato Yellow Leaf Curl Virus",
        "cure": [
            "No direct cure; remove infected plants",
            "Control whitefly populations",
        ],
    },
    7: {
        "disease": "Tomato Leaf Mold",
        "cure": ["Apply fungicides", "Improve air circulation", "Reduce humidity"],
    },
    8: {
        "disease": "No found disease",
        "cure": ["No cure"],
    },
}
