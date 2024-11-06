from django.shortcuts import get_object_or_404, render, redirect
from .models import Recipe, Ingredient, RecipeIngredient
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import connection

import requests

def index(request):
    try:
        response = requests.get("https://picsum.photos/v2/list")
        response.raise_for_status()  

        images = response.json()
        filtered_image = None
        for i in images:    
            if i["id"] == "23":
                 filtered_image = i

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        images = [] 
    except ValueError as e:
        print(f"JSON decoding error: {e}")
        images = [] 

    return render(request, 'index.html', {'image': filtered_image})

def recipe_list(request):
    recipes = Recipe.objects.all()  # Fetch all Recipe instances
    print(recipes)
    return render(request, 'recipe_list.html', {'recipes': recipes})


def recipe_detail(request, recipe_id):
    # Fetch the recipe details using raw SQL
    with connection.cursor() as cursor:
        # A03:2021 – Injection
        # Insecure: Directly injecting `recipe_id` into the query without sanitization
        # Fix: 
        # - uncomment row 47
        # - delete row 46
        cursor.execute(f"SELECT * FROM recipe WHERE id = {recipe_id}") # vulnerable /recipes/1; DROP TABLE recipe; --
        # cursor.execute("SELECT * FROM recipe WHERE id = %s", [recipe_id])
        recipe_row = cursor.fetchone()
    
    if not recipe_row:
        raise Http404("Recipe not found")
    
    recipe = {
        'id': recipe_row[0],
        'title': recipe_row[1],
        'instructions': recipe_row[2],
        'oven_temperature': recipe_row[3],
        'equipment': recipe_row[4],
        'is_dessert': recipe_row[5],
    }
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ri.amount, i.name
            FROM recipe_ingredient ri
            JOIN ingredient i ON ri.ingredient_id = i.id
            WHERE ri.recipe_id = %s
        """, [recipe_id])
        
        ingredients = cursor.fetchall()
    
    ingredients_list = [{'amount': row[0], 'name': row[1]} for row in ingredients]

    return render(request, 'recipe_detail.html', {
        'recipe': recipe,
        'ingredients': ingredients_list
    })


# @login_required ##  A01:2021 – Broken Access Control, uncomment this line to fix the issue
def add_recipe(request):

    ingredients = Ingredient.objects.all()  

    if request.method == 'POST':
        title = request.POST.get('title')
        instructions = request.POST.get('instructions')

        # Create the new recipe
        recipe = Recipe.objects.create(title=title, instructions=instructions)

        # Process ingredient fields
        form_count = len([key for key in request.POST.keys() if key.startswith('ingredient_')])
        
        for i in range(form_count):
            ingredient_id = request.POST.get(f'ingredient_{i}')
            amount = request.POST.get(f'amount_{i}')

            if ingredient_id and amount:
                ingredient = Ingredient.objects.get(id=ingredient_id)
                
                # Check if the ingredient is already linked to this recipe
                if not RecipeIngredient.objects.filter(recipe=recipe, ingredient=ingredient).exists():
                    RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, amount=amount)

        return redirect('recipe_list')
    
    return render(request, 'add_recipe.html', {'ingredients': ingredients})

@login_required
def add_ingredient(request):
    if request.method == 'POST':
        ingredient_name = request.POST.get('ingredient_name')

        # Check if the ingredient already exists
        ingredient, created = Ingredient.objects.get_or_create(name=ingredient_name)
        if created:
            return JsonResponse({'status': 'success', 'ingredient': {'id': ingredient.id, 'name': ingredient.name}})
        else:
            return JsonResponse({'status': 'error', 'message': 'Ingredient already exists'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


#### Authentication 

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f"Welcome, {username}! Your account has been created.")
            return redirect('profile')
        else:
            messages.error(request, "Signup failed. Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect('profile')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('login')

@login_required
def profile_view(request):
    return render(request, 'registration/profile.html')