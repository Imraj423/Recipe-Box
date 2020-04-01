from django.shortcuts import render, reverse, HttpResponseRedirect, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .decorators import unauth_user, allowed_users
from recipebox.models import Author, Recipe
from django.contrib.auth.decorators import permission_required
from recipebox.forms import RecipeAddForm, AuthorAddForm, SignupForm, LoginForm, EditRecipe


def index(request):
    recipes = Recipe.objects.all()
    user = request.user
    return render(request, 'index.html', {
        'data': recipes,
        'user': user if user.is_authenticated else None
    })


def show_recipe(request, id):
    recipe = Recipe.objects.get(id=id)
    return render(request, 'recipe.html', {'recipe': recipe})


def show_author(request, id):
    author = Author.objects.get(id=id)
    recipes = Recipe.objects.filter(author=author)
    favorites = author.favorites.all()
    print(favorites)
    return render(request, 'author.html',
                  {
                    'author': author,
                    'recipes': recipes,
                    'favorites': favorites
                  })


@login_required()
def recipe_add_view(request):
    html = "generic_form.html"

    if request.method == 'POST':
        form = RecipeAddForm(None, request.POST)
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

    form = RecipeAddForm(request.user)

    return render(request, html, {'form': form})


@login_required()
@allowed_users(allowed_roles=['admin', 'author'])
def author_add_view(request):
    html = 'generic_form.html'

    if request.method == 'POST':
        form = AuthorAddForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse('homepage'))
        
    form = AuthorAddForm()

    return render(request, html, {'form': form})


def login_view(request):
    html = 'generic_form.html'
    
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', '/'))
    
    return render(request, html, {'form': LoginForm()})


# @unauth_user
@user_passes_test(lambda u: u.is_superuser)
def creatuser_view(request):
    html = 'generic_form.html'

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                data['username'], data['password1']
            )
            login(request, user)
            Author.objects.create(
                name=data['username'],
                user=user
            )
            return HttpResponseRedirect(reverse('login'))
        
    return render(request, html, {'form': SignupForm()})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))


@allowed_users(allowed_roles=['admin', 'author'])
def edit_recipe(request, id):
    html = 'editRecipe.html'
    instance = Recipe.objects.get(id=id)
    if request.method == 'POST':
        form = EditRecipe(request.POST, instance=instance)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse("homepage"))

    form = EditRecipe(instance=instance)

    return render(request, html, {'form': form})


# @login_required()
def add_favorite(request, id):
    recipe = None
    user = None

    try:
        recipe = Recipe.objects.get(id=id)
        user = Author.objects.get(name=request.user.username)
        user.favorites.add(recipe)
        user.save()
    except Exception as e:
        print(e)

        return HttpResponseRedirect(reverse("homepage"))
    return render(request, 'author.html', {'recipe': recipe, 'user': user})


def all_author_view(request):
    html = 'arturos.html'
    show_all = Author.objects.all()
    return render(request, html, {'show_all': show_all})
