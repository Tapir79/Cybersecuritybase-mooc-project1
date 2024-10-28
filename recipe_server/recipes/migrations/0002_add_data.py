# migration file (0002) with add_initial_data function
from django.db import migrations

def add_initial_data(apps, schema_editor):
    Ingredient = apps.get_model("recipes", "Ingredient")
    Recipe = apps.get_model("recipes", "Recipe")
    RecipeIngredient = apps.get_model("recipes", "RecipeIngredient")

    flour = Ingredient.objects.create(name="Flour")
    sugar = Ingredient.objects.create(name="Sugar")
    butter = Ingredient.objects.create(name="Butter")
    eggs = Ingredient.objects.create(name="Eggs")
    salt = Ingredient.objects.create(name="Salt")

    cake = Recipe.objects.create(
        title="Chocolate Cake",
        instructions="Mix ingredients and bake.",
        oven_temperature=350,
        equipment="Oven, Mixer",
        is_dessert=True,
    )

    RecipeIngredient.objects.create(recipe=cake, ingredient=flour, amount="2 dl")
    RecipeIngredient.objects.create(recipe=cake, ingredient=sugar, amount="1 dl")
    RecipeIngredient.objects.create(recipe=cake, ingredient=butter, amount="1/2 dl")
    RecipeIngredient.objects.create(recipe=cake, ingredient=eggs, amount="2 large")
    RecipeIngredient.objects.create(recipe=cake, ingredient=salt, amount="1/2 tsp")

class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(add_initial_data),
    ]
