from django.shortcuts import render
from recipebox.models import Author, Recipe

def index(request):
    recipes = Recipe.objects.all()
    return render(request, 'index.html', {'data': recipes})

def show_recipe(request, id):
    recipe = Recipe.objects.get(id=id)
    return render(request, 'recipe.html', {'recipe': recipe})

def show_author(request, id):
    author = Author.objects.get(id=id)
    return render(request, 'author.html', {'author': author})