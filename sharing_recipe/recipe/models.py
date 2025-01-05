from typing import Iterable
from django.db import models
from django.contrib.auth.models import User
from recipe.constants import *

# Create your models here.
class Categories(models.Model):
    category_name = models.CharField(max_length=50, choices=RECIPE_CATEGORY, unique=True)
    
    def __str__(self):
        return self.category_name

class Recipe(models.Model):
    title = models.CharField(max_length=200, help_text="Name of the Recipe")
    ingredients = models.TextField()
    instructions = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='recipe_images/', null=True, blank=True)
    category_name = models.ForeignKey(Categories, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} by {self.user} under {self.category_name} section."

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['recipe', 'user']
        
    def __str__(self):
        return f"Comment by {self.user.username} on {self.recipe.title}"
    
class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=1, choices=[(i, i) for i in range(1, 6)])

    class Meta:
        unique_together = ['recipe', 'user']    
        
    def __str__(self):
        return f"Rating {self.score} by {self.user.username} on {self.recipe.title}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    favorite_recipes = models.ManyToManyField(Recipe, blank=True)
    
    def __str__(self):
        return self.user.username 
