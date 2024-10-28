from django.shortcuts import get_object_or_404, render, redirect
from .models import Recipe

def index(request):
    return render(request, 'index.html') 

def recipe_list(request):
    recipes = Recipe.objects.all()  # Fetch all Recipe instances
    print(recipes)
    return render(request, 'recipe_list.html', {'recipes': recipes})

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipe_detail.html', {'recipe': recipe})