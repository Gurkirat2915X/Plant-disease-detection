from django.shortcuts import render
from .models import detection, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .utils import detector, chatbot, care_tips
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.
def index(request):
    fields = User._meta.get_fields()
    return render(request, "pages/index.html")


@login_required(login_url="disease_detector:login")
def dashboard(request):
    detections = detection.objects.filter(by=request.user).order_by("-date")
    return render(
        request,
        "pages/dashboard.html",
        {"detections": detections, "user": request.user},
    )


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("disease_detector:dashboard"))
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("disease_detector:dashboard"))
        else:
            return render(
                request, "pages/login.html", {"message": "Invalid credentials"}
            )
    return render(request, "pages/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("disease_detector:index"))


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("disease_detector:dashboard"))
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            user.save()
        except Exception as e:
            return render(
                request,
                "pages/register.html",
                {
                    "message": "Invalid credentials or username already exists. Error: "
                    + str(e)
                },
            )
        login(request, user)
        return HttpResponseRedirect(reverse("disease_detector:dashboard"))
    return render(request, "pages/register.html")


def model_intro(request):
    return render(request, "pages/model_intro.html")


def team(request):
    return render(request, "pages/team.html")


@login_required(login_url="disease_detector:login")
def detect(request):
    if request.method == "POST":
        image = request.FILES["image"]
        new_detection = detection(by=request.user, image=image)
        new_detection.save()
        result = detector(image, new_detection.id)
        new_detection.result = result["name"]
        new_detection.confidence = result["confidence"]
        new_detection.detection_img = result["image"]
        new_detection.class_name = int(result["class"])
        new_detection.save()
        return HttpResponseRedirect(
            reverse("disease_detector:result", args=(new_detection.id,))
        )

    return render(request, "pages/detect.html")


@login_required(login_url="disease_detector:login")
def result(request, id):
    try:
        detection_obj = detection.objects.get(id=id)
        print(detection_obj)
        if detection_obj.by != request.user:
            return HttpResponseRedirect(
                reverse(
                    "disease_detector:dashboard",
                    {"message": "You are not authorized to view this page"},
                )
            )
        return render(
            request,
            "pages/result.html",
            {
                "detection": detection_obj,
                "media_url": settings.MEDIA_URL,
                "tips": care_tips[detection_obj.class_name]["cure"],
            },
        )
    except:
        return HttpResponseRedirect(
            reverse("disease_detector:dashboard", {"message": "Detection not found"})
        )


@csrf_exempt
def chat(request):
    if request.method == "POST":
        chat = json.loads(request.body)
        response = chatbot(chat["message"])
        return JsonResponse({"response": response})
    return JsonResponse({"response": "Invalid request"})
