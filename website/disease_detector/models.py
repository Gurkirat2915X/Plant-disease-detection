from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    pass

class detection(models.Model):
    by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='detections')
    image = models.ImageField(upload_to='images/' , null=True,blank=True)
    detection_img = models.ImageField(upload_to='detection_images/', null=True,blank=True)
    result = models.CharField(max_length=100)
    confidence = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    feed_back = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.result