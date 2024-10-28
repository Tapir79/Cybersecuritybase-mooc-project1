from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipes', views.recipe_list, name='recipe_list'),
    path('recipes/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'), 
    path('recipes/add/', views.add_recipe, name='add_recipe'), 
    path('ingredients/add/', views.add_ingredient, name='add_ingredient'),
]