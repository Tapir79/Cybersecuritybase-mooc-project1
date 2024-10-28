from django.shortcuts import render
from .models import Recipe

def index(request):
    return render(request, 'index.html') 

def recipe_list(request):
    recipes = Recipe.objects.all()  # Fetch all Recipe instances
    print(recipes)
    return render(request, 'recipe_list.html', {'recipes': recipes})