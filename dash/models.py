from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    # content = models.TextField()
    content = models.ImageField(upload_to='jobposters/')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Advertisement(models.Model):
    image = models.ImageField(upload_to='advertisements/')  # To store the advertisement image
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the ad is added

    def __str__(self):
        return f"Advertisement {self.id}"
    
class Posters(models.Model):
    image = models.ImageField(upload_to='posters/')  # To store the advertisement image
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the ad is added

    def __str__(self):
        return f"Poster {self.id}"