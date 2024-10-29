from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipes', views.recipe_list, name='recipe_list'),
    path('recipes/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'), 
    path('recipes/add/', views.add_recipe, name='add_recipe'), 
    path('ingredients/add/', views.add_ingredient, name='add_ingredient'), 
    path('admin/', admin.site.urls),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/signup/', views.signup_view, name='signup'),
    path('accounts/profile/', views.profile_view, name='profile'),
]