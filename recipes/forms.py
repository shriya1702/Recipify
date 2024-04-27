from django.contrib.auth.models import User
from django import forms
from taggit.forms import TagField

from .models import Recipe, Ingredient


class userform(forms.ModelForm):
  class Meta:
    model= User 
    fields =['username','password']
  

class userRegister(forms.ModelForm):
  email = forms.EmailField(required=True)
  class Meta:
    model= User
    fields= [
      'username',
      'password',
      'email',
      'first_name',
      'last_name',
    ]
    def save(self, commit=True):
      user = super(userRegister, self).save(commit=False)
      user.email = self.cleaned_data['email']
      if commit:
        user.save()
      return user
    

class RecipeForm(forms.ModelForm):
    tags = TagField(required=False)
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'image', 'servings', 'time', 'ingredients'] 