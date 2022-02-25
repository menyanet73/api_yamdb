from django.contrib import admin

from . import models


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'category', 'description')
    list_filter = ('category', 'genre')
    search_fields = ('name', 'year', 'description')


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'confirmation_code', 'role')
    list_filter = ('role',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'score', 'author', 'pub_date')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'author', 'text', 'pub_date')
    search_fields = ('text',)


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Title, TitleAdmin)
admin.site.register(models.Genre, GenreAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Review, ReviewAdmin)
admin.site.register(models.Comment, CommentAdmin)
