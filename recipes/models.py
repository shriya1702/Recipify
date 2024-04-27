from django.db import models
from taggit.managers import TaggableManager 
#pip install django-taggit input tags key liye
from django.contrib.auth.models import User


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='user_uploads/', null=True, blank=True)
    time = models.CharField(max_length=20)
    rating = models.IntegerField(default=0)
    servings = models.IntegerField(default=1)
    ingredients = TaggableManager()
    status = models.CharField(max_length=50, default='Pending')

    def save(self, *args, **kwargs):
        if self.image and self.image.url.startswith('static/user_uploads/'):
            self.image.name = self.image.name.replace('static/user_uploads/', '')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name


class adminn(models.Model):  # Renamed the class to follow Python naming conventions
    Recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='Pending')
