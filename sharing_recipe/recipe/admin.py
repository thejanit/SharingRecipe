from django.contrib import admin
from recipe.models import Recipe, Comment, Rating, Categories, UserProfile

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Categories)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
