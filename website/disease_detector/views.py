from django.shortcuts import render
from .models import detection, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .utils import load_image, detector

# Create your views here.
def index(request):
    fields = User._meta.get_fields()
    for field in fields:
        print(field)
    return render(request, 'pages/index.html')
@login_required(login_url='disease_detector:login')
def dashboard(request):
    detections = detection.objects.filter(by=request.user)
    return render(request, 'pages/dashboard.html', {'detections': detections, 'user': request.user})
def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('disease_detector:dashboard'))
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('disease_detector:dashboard'))
        else:
            return render(request, 'pages/login.html', {'message': 'Invalid credentials'})
    return render(request, 'pages/login.html')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('disease_detector:index'))
def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('disease_detector:dashboard'))
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        try:
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
            print("Very good")
            user.save()
        except Exception as e:
            return render(request, 'pages/register.html', {'message': 'Invalid credentials or username already exists. Error: ' + str(e)})
        login(request, user)
        return HttpResponseRedirect(reverse('disease_detector:dashboard'))
    return render(request, 'pages/register.html')
def model_intro(request):
    return render(request, 'pages/model_intro.html')
def team(request):
    return render(request, 'pages/team.html')
@login_required(login_url='disease_detector:login')
def detect(request):
    if request.method == 'POST':
        image = request.FILES['image']
        print(image)
        print(request.user)
        result = detector(image)
        result.show()
        
        
    return render(request, 'pages/detect.html')

def result(request):
    return render(request, 'pages/result.html')

