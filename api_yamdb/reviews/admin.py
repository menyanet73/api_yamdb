from django.contrib import admin

from .models import Title, Genre, Category

admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Category)
