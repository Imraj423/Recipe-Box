"""recipebox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from recipebox.models import Author, Recipe
from recipebox import views

try:
    admin.site.register(Author)
    admin.site.register(Recipe)
except Exception:
    pass

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recipe/<int:id>', views.show_recipe),
    path('author/<int:id>', views.show_author),
    path('recipeadd/', views.recipe_add_view, name="recipeadd"),
    path('authoradd/', views.author_add_view),
    path('/', views.index, name="homepage")
]
