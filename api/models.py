from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    bio = models.TextField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='media/profile_photos/', null=True, blank=True)

    def get_profile_photo_url(self):
        if self.profile_photo:
            # If using default storage, construct the URL
            if settings.DEFAULT_FILE_STORAGE == 'django.core.files.storage.FileSystemStorage':
                return self.profile_photo.url
            else:
                # For other storage backends like cloud-based storages
                return self.profile_photo.url
        return None

class PlantImage(models.Model):
    image = models.ImageField(upload_to='plant_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Detection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='detections')
    image = models.ImageField(upload_to='detections/')
    prediction = models.CharField(max_length=255)
    confidence = models.FloatField()
    description = models.TextField()
    recommendations = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
