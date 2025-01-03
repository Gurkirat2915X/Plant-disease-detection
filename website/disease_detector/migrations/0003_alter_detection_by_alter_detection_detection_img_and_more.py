# Generated by Django 4.2.16 on 2024-11-21 13:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('disease_detector', '0002_rename_detections_detection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detection',
            name='by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detections', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='detection',
            name='detection_img',
            field=models.ImageField(blank=True, null=True, upload_to='detection_images/'),
        ),
        migrations.AlterField(
            model_name='detection',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
