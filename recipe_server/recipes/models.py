from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ingredient'  
        
class Recipe(models.Model):
    title = models.CharField(max_length=100)
    instructions = models.TextField()
    oven_temperature = models.IntegerField(null=True, blank=True)  # Optional for non-baked items
    equipment = models.TextField()  # List required equipment if any
    is_dessert = models.BooleanField(default=False)  # Flag to indicate dessert vs. regular food
    ingredients = models.ManyToManyField('Ingredient', through='RecipeIngredient', related_name="recipes")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'recipe' 

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.CharField(max_length=50, default="1 dl")  

    def __str__(self):
        return f"{self.amount} of {self.ingredient.name} in {self.recipe.title}"

    class Meta:
        unique_together = ('recipe', 'ingredient')
        db_table = 'recipe_ingredient'
