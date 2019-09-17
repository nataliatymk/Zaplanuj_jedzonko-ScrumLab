from django.contrib import admin

# Register your models here.
from jedzonko.models import Recipe, Plan, Dayname, Recipeplan, Page

admin.site.register(Recipe),
admin.site.register(Plan),
admin.site.register(Dayname),
admin.site.register(Recipeplan),
admin.site.register(Page),