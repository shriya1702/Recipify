import os
from django.conf import settings
from django.shortcuts import render,redirect, HttpResponse, HttpResponseRedirect
from . import models
from .models import Recipe
from django.contrib.auth.decorators import login_required ,user_passes_test
from django.contrib.auth import authenticate, login, logout
from .forms import userform, userRegister
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import RecipeForm
from django.shortcuts import render, redirect
from .forms import RecipeForm


# Create your views here.
@login_required
def user_dashboard(request):
  username= request.user.username
  return render(request,'recipes/user_dashboard.html',{'username':username})

@login_required
@user_passes_test(lambda u: u.is_staff)

def admin_dashboard(request):
  submissions= Recipe.objects.filter(approved=False)
  return render(request,'recipes/admin_dashboard.html', {'submissions': submissions})

@login_required
@user_passes_test(lambda u: u.is_staff)
def approve_recipe(request, recipe_id):
  recipe= Recipe.objects.get(pk=recipe_id)
  recipe.approved= True
  recipe.save
  return redirect('admin_dashboard')
  

def home(request):
  recipes= models.Recipe.objects.all()
  print(recipes)
  context= {
    'recipes' : recipes
  }
  return render(request,'recipes/home.html',context) 
def about(request):
  return render(request,'recipes/home')



# def login(request):
#   return render(request,'recipes/login.html')

    
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            request,
            username=username,
            password=password
        )
        print(user)
        if user is not  None:
            print('inside')
            login(request, user)
            if user.is_staff:
              print(username)
              return redirect('admin_dashboard')
            return redirect('user_dashboard')
        else:
          return render(request, 'recipes/login.html', {'error':'Invalid credentials'})
    
    else:
      return render(request, 'recipes/login.html')
        
        
        
        
def signout(request):
        logout(request)
        return redirect('/')
            
  
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "You have signed up successfully."}, status=200)
        else:
            error_messages = form.errors.as_json()
            return JsonResponse({"error": error_messages}, status=400)
    else:
        form = UserCreationForm()
    return render(request, 'recipes/signup.html', {'form': form})
  
  
def viewuploaded(request):
  
  return render(request, 'recipes/viewuploaded.html')


def user_data(request):
  author_id = request.user.id  # Assuming the logged-in user is the author
  user=User.objects.filter(id=author_id).values('username')
  
  recipe = Recipe.objects.filter(author_id=author_id).values('title', 'description',  'image', 'approved')
  print("hello",recipe)
  
  return JsonResponse({'recipe':list(recipe)})
  
  
  
from django.conf import settings
import os
from django.conf import settings
import os

def upload(request):
    print("inside upload")
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            # Define the base directory for user uploads
            base_dir = os.path.join(settings.BASE_DIR, 'static', 'user_uploads')

            # Create a directory for the user if it doesn't exist
            user_dir = os.path.join(base_dir, str(user.username))
            if not os.path.exists(user_dir):
                os.makedirs(user_dir)

            # Get the uploaded image from the form
            uploaded_image = form.cleaned_data['image']

            # Get the image name without the 'static/user_uploads/' prefix
            image_name = os.path.basename(uploaded_image.name)

            # Save the uploaded image to the user's directory
            with open(os.path.join(user_dir, image_name), 'wb') as file:
                for chunk in uploaded_image.chunks():
                    file.write(chunk)

            # Set the image path to be saved in the database
            image_path = os.path.join('user_uploads', user.username, image_name).replace("\\", "/")

            # Save the form data to the database
            recipe_instance = form.save(commit=False)
            recipe_instance.author = user
            recipe_instance.image = image_path
            recipe_instance.save()

            return redirect('user_dashboard')  # Redirect to a success page

    else:
        form = RecipeForm()
    return render(request, 'recipes/upload.html', {'form': form})


# def send_for_approval(request):
#     #this recipe author
    
#     if request.method == 'POST':
#        author_id=request.user.id
#        user=Recipe.objects.filter(author_id=author_id  ).values('id')
       
       
      

#   return render()
  






# # def upload(request):
# #     print("inside upload")
# #     if request.method == 'POST':
# #         form = RecipeForm(request.POST, request.FILES)
# #         if form.is_valid():
# #             user = request.user
# #             path = "./static/user_uploads/"
# #             user_dir = os.path.join(path, str(user.username))
# #             if not os.path.exists(user_dir):
# #                 os.makedirs(user_dir)

# #             # Get the uploaded image from the form
# #             uploaded_image = form.cleaned_data['image']
            
# #             # Save the uploaded image to the user's directory
# #             with open(os.path.join(user_dir, uploaded_image.name), 'wb') as file:
# #                 for chunk in uploaded_image.chunks():
# #                     file.write(chunk)

# #             # Save the form data to the database
# #             recipe_instance = form.save(commit=False)
# #             recipe_instance.author = user
# #             recipe_instance.save()

# #             return redirect('user_dashboard')  # Redirect to a success page
# #     else:
# #         form = RecipeForm()
# #     return render(request, 'recipes/upload.html', {'form': form})









# def handle_uploaded_file(user, uploaded_file):
#     # Define the path where you want to save the file
#     path = f"./static/user_uploads/{user.username}/"
#     if not os.path.exists(path):
#         os.makedirs(path)
    
#     # Write the file to the specified path
#     with open(os.path.join(path, uploaded_file.name), 'wb+') as destination:
#         for chunk in uploaded_file.chunks():
#             destination.write(chunk)

# # Example usage in a view function
# def upload(request):
#     if request.method == 'POST':
#         form = RecipeForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Set the author of the recipe
#             form.instance.author = request.user 
            
#             # Save the form data, including the uploaded file
#             recipe = form.save(commit=False)
#             recipe.save()

#             # Call the function to handle the uploaded file
#             handle_uploaded_file(request.user, request.FILES['file'])

#             return redirect('user_dashboard')  # Redirect to a success page
#     else:
#         form = RecipeForm()
#     return render(request, 'recipes/upload.html', {'form': form})




# def upload(request):

#     print("inside upload")
#     if request.method == 'POST':
#         print(request.FILES['file'])
#         user= request.user
#         path="./static/user_uploads/"
#         user_dir= os.path.join(path,str(user.username))
#         # print(user_dir)
#         if not os.path.exists(user_dir):
#           os.mkdir(user_dir)
#         uploaded_file = request.FILES["file"]
#         print(uploaded_file)
#               # namee=request.FILES.read()
#               # with open(os.path.join(user_dir,namee.name),'wb') as file:
#               #     print(os.path.join(user_dir,namee.name))
#               #     file.write(namee)
              
        
        
#         form = RecipeForm(request.POST, request.FILES)
#         # print(request.FILES)
        
#         if form.is_valid():
#             # print("isnide fork")
          
#             form.instance.author = request.user 
            
#             form.save()
#             return redirect('user_dashboard')  # Redirect to a success page
#     else:
#         form = RecipeForm()
#     return render(request, 'recipes/upload.html', {'form': form})




