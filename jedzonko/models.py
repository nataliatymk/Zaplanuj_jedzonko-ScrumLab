from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    preparation_time = models.IntegerField()
    preparation_recipe = models.CharField(max_length=255)
    votes = models.IntegerField()

    def show_name(self):
        return self.name

class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now=True)


class Dayname(models.Model):

    day_names = (
        (0, "poniedziałek"),
        (1, "wtorek"),
        (2, "środa"),
        (3, "czwartek"),
        (4, "piątek"),
        (5, "sobota"),
        (6, "niedziela"),
    )
    id = models.IntegerField(primary_key=True)
    order = models.IntegerField(choices=day_names)

    def show_day_name(self):
        name_day = ""
        for day in Dayname.day_names:
            if day[0] == self.order:
                name_day = day[1]
        return name_day


class Recipeplan(models.Model):
    meal_name = models.CharField(max_length=255)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    order = models.IntegerField()
    day_name = models.ForeignKey(Dayname, on_delete=models.CASCADE)


class Page(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(
        default='',
        editable=False,
    )

    def get_absolute_url(self):
        kwargs = {
            'pk': self.id,
            'slug': self.slug
        }
        return reverse('article-pk-slug-detail', kwargs=kwargs)

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value)
        super().save(*args, **kwargs)
