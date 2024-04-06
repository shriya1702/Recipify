from django.db import models
from django.contrib.auth.models import User
# from django.urls import reverse
# Create your models here.

class admin(models.Model):
  approved=models.BooleanField()
  user=models.CharField(max_length=100)
  

class Recipe(models.Model):
  title=models.CharField(max_length=100)
  description=models.TextField()
  author=models.ForeignKey(User, on_delete=models.CASCADE)
  created_at= models.DateTimeField(auto_now_add=True)
  updated_at= models.DateTimeField(auto_now=True)
  image = models.ImageField(upload_to='user_uploads/', null=True, blank=True)  # Image field
  approved= models.BooleanField(default=False)
  def save(self, *args, **kwargs):
        # Check if the image path starts with 'static/user_uploads/'
        if self.image.url.startswith('static/user_uploads/'):
            # Remove the 'static/user_uploads/' prefix from the image path
            self.image.name = self.image.name.replace('static/user_uploads/', '')

        super().save(*args, **kwargs)
#   # def get_absolute_url(self):
#   #     return reverse("recipes-detail", kwargs={"pk": self.pk})

  def __str__(self):
    return self.title
  
