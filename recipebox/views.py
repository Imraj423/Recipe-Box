from django.shortcuts import render, reverse, HttpResponseRedirect
from recipebox.models import Author, Recipe
from recipebox.forms import RecipeAddForm, AuthorAddForm

def index(request):
    recipes = Recipe.objects.all()
    return render(request, 'index.html', {'data': recipes})

def show_recipe(request, id):
    recipe = Recipe.objects.get(id=id)
    return render(request, 'recipe.html', {'recipe': recipe})

def show_author(request, id):
    author = Author.objects.get(id=id)
    return render(request, 'author.html', {'author': author})

def recipe_add_view(request):
    html = "generic_form.html"

    if request.method == 'POST':
        form = RecipeAddForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data['title'],
                author=data['author'],
                description=data['description'],
                time_required=data['time_required'],
                instructions=data['instructions'],
            )
        return HttpResponseRedirect(reverse('homepage'))

    form = RecipeAddForm()

    return render(request, html, {'form': form})

def author_add_view(request):
    html = 'generic_form.html'

    if request.method == 'POST':
        form = AuthorAddForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse('homepage'))
        
    form = AuthorAddForm()

    return render(request, html, {'form': form})