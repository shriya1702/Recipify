import os,json
from django.conf import settings
from django.shortcuts import render,redirect, HttpResponse, HttpResponseRedirect
from . import models
from .models import Recipe, adminn
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
  submissions= Recipe.objects.filter(status=False)
  return render(request,'recipes/admin_dashboard.html', {'submissions': submissions})


def submissions(request): #admin's submission page
  
  submission_data= submission_table()
  print(submission_data)
  return render(request,'recipes/submissions.html',{'submissions_data': submission_data})

  
def all_recipe(request):
   
   return render(request, 'recipes/all_recipes.html')

def show_all_recipe(request):
  
   recipe = Recipe.objects.values('id','title', 'description', 'image') 
       
   return JsonResponse({'recipe':list(recipe)})

   


def submission_table():
  
    admin_submissions = adminn.objects.all()
    ds = []
    for submission in admin_submissions:
        # Get associated Recipe object
        recipe = submission.Recipe_id

        # Get additional details
        recipe_data = {
            'id': recipe.id,
            'title': recipe.title,
            'author': recipe.author.username,
            'status': submission.status
            # Add any other fields you want to include
        }
        ds.append(recipe_data)

    return ds


@login_required
@user_passes_test(lambda u: u.is_staff)

def approve_recipe(request, recipe_id):
  recipe= Recipe.objects.get(pk=recipe_id)
  recipe.approved= True
  recipe.save
  return redirect('admin_dashboard')
  

def home(request):
  recipe = Recipe.objects.values('id','title', 'description', 'image')  
  print(recipe)
   
  return render(request,'recipes/homee.html', {'user':request.user}) 


def about(request):
  return render(request,'recipes/homee.html')


def full_recipe(request):
  return render(request, "recipes/full_recipe.html")
      
    
def viewuploaded(request):
  return render(request, 'recipes/viewuploaded.html')

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
  
  

#userdashboard mai view data par saari uski recipes 
def user_data(request):
  author_id = request.user.id  # Assuming the logged-in user is the author
  user=User.objects.filter(id=author_id).values('username')
  print(user)
  recipe = Recipe.objects.filter(author_id=author_id).values('id','title', 'description', 'image')
  
  return JsonResponse({'recipe':list(recipe)})



  
def recipe_content(request):
    # Assuming the logged-in user is the author
    
    
    print("hello inside")
    id=json.loads(request.body)['item']
    print(id)
    recipe= Recipe.objects.filter(id=id).values()
    print(recipe)
    
    return JsonResponse({'recipe':list(recipe)})
    
  


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


from django.http import JsonResponse

def send_for_approval(request):
    if request.method == 'POST':
        print("im in")
        # Get the recipe ID from the request data
        recipe_id = request.POST.get('id')
        print(recipe_id)
        
        # Retrieve the current user
        user = request.user
        
        # Create an entry in the adminn table with the recipe ID and status
        
        recipe = Recipe.objects.get(pk=recipe_id)
        recipe.status = 'SentForApproval'
        recipe.save()

        
        
        admin_entry = adminn.objects.create(
            Recipe_id=Recipe.objects.get(pk=recipe_id),
            status='SentForApproval'
        )
       
        #check ki id already exist karti hai ki nahi
        # Return a success response
        return JsonResponse({'message': 'Recipe sent for approval successfully.'})
    else:
        # Return an error response if the request method is not POST
        return JsonResponse({'error': 'Invalid request method.'}, status=400)








