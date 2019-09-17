from datetime import datetime
from django.shortcuts import render, redirect
from django.views import View
from jedzonko.models import Recipe, Plan, Recipeplan, Dayname, Page
from django.core.paginator import Paginator
from django.urls import reverse
from django.http import HttpResponse
from django.db.models import Q
#


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        counter_recipe = Recipe.objects.count()
        counter_plan = Plan.objects.count()

        plan = Plan.objects.all().order_by("-created")[:1].get()
        return render(request, "__base__.html", context={'ctx':ctx, 'counter_of_recipes': counter_recipe,
                               'counter_of_plan': counter_plan,
                               'plan': plan})


class RecipeListView(View):
    def get(self, request):
        #jeżeli mają po tyle samo glosow to wg godziny
        recipes_list = Recipe.objects.all().order_by("-votes", "-created")
        paginator = Paginator(recipes_list, 50) #po 50 per page
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        return render(request, "recipes.html", context={"recipes":recipes})



class RecipeDetailView(View):

    def get(self, request, id):
        recipe = Recipe.objects.get(id=id)
        ingredients = recipe.ingredients
        ingredients = ingredients.split(",")
        return render(request, "app-recipe-details.html", context={"recipe": recipe, "ingredients": ingredients})

    def post(self, request, id):
        recipe = Recipe.objects.get (id=id)
        ingredients = recipe.ingredients
        ingredients = ingredients.split (",")
        vote = request.POST.get("like")
        if vote == "like":
            recipe.votes = int(recipe.votes)+1
            recipe.save()
        else:
            recipe.votes = int (recipe.votes) - 1
            recipe.save ()
        return render (request, "app-recipe-details.html", context={"recipe": recipe, "ingredients": ingredients})


class RecipeAllView(View):

    def get(self, request):
        return render(request, "app-recipes.html")


class LandingPageView(View):

    def get(self, request):
        request.session.flush()
        recipe = Recipe.objects.all().order_by('?')
        random_recipe1 = recipe[1]
        random_recipe2 = recipe[2]
        random_recipe3 = recipe[3]



        return render(request, "index.html",
                      context={'random_recipe1': random_recipe1, 'random_recipe2': random_recipe2,
                               'random_recipe3': random_recipe3})

    def post(self, request):
        try:
            search_word = request.POST.get("search_word")
            recipe = Recipe.objects.filter(
                Q(name=search_word.lower()) | Q(name=search_word.upper()) |
                Q(name=search_word[0].upper()+search_word[1:])
            ).first()

            return redirect(reverse("RecipeDetailView", args=[recipe.id]))
        except Exception:
            return redirect(reverse("LandingPageView"))


class RecipeAddView(View):
    def get(self, request):
        return render(request, "app-add-recipe.html")

    def post(self, request):
        recipe = Recipe()
        name = request.POST.get('name')
        description = request.POST.get('description')
        preparation_time = request.POST.get('preparation_time')
        preparation_recipe = request.POST.get('preparation_recipe')
        ingredients = request.POST.get('ingredients')
        votes = 0
        if name and description and preparation_recipe and preparation_time and ingredients:
            recipe.name=name
            recipe.description=description
            recipe.preparation_time=preparation_time
            recipe.preparation_recipe=preparation_recipe
            recipe.ingredients=ingredients
            recipe.votes = 0
            new_recipe = Recipe(name=name, description=description, preparation_recipe=preparation_recipe, preparation_time=preparation_time, ingredients=ingredients, votes=votes)
            new_recipe.save()
            return redirect(reverse("RecipeListView"))
        else:
            mess= f"Wypełnij poprawnie wszystkie pola"
            return render(request, 'app-add-recipe.html', context={'mess':mess})



class PlanView(View):

    def get(self, request):
        plans = Plan.objects.all().order_by("name")
        paginator = Paginator(plans, 50)
        page = request.GET.get('page')
        page_objects = paginator.get_page(page)
        return render(request, "app-schedules.html", context={'page_objects': page_objects})


class PlanAddView(View):

    def get(self, request):
        return render(request, "app-add-schedules.html")

    def post(self, request):
        plan = Plan()
        plan_name = request.POST.get("planName")
        plan_description = request.POST.get("planDescription")
        if plan_name and plan_description:
            plan.name = plan_name
            plan.description = plan_description
            plan.save()
            new_plan = Plan.objects.get(name=plan_name)
            request.session["plan_id"] = new_plan.id
            return redirect(reverse("PlanAddDetailsView"))

        else:
            message = f"Niepoprawne dane"
            return render(request, "app-add-schedules.html", context={'message': message})


class PlanDetailView(View):

    def get(self, request, id):

        plan = Plan.objects.get(id=id)
        recipeplan = Recipeplan.objects.filter(plan_id=id).order_by("day_name_id")
        counter_obj = dict()
        for obj in recipeplan:
            if obj.day_name_id not in counter_obj:
                counter_obj[obj.day_name_id] = obj

        return render(request, "app-details-schedules.html", context={"plan": plan,
                                                                      "recipeplan": recipeplan.order_by("order"),
                                                                      "counter_obj": counter_obj})

    def post(self, request, id):
        if 'delete_recipe' in request.POST:
            recipe_id = request.POST.get("delete_recipe")
            recipeplan_del = Recipeplan.objects.get(pk=recipe_id)
            recipeplan_del.delete()
        elif 'add_recipe' in request.POST:
            request.session["plan_id"] = id
            return redirect(reverse("PlanAddDetailsView"))

        return redirect(reverse("PlanDetailView", args=[id]))



class PlanAddDetailsView(View):
    def get(self, request):

        try:
            print(request.session["plan_id"])
            plan_id = request.session["plan_id"]
            plan = Plan.objects.get(id=plan_id)
            days_name = Dayname.objects.all().order_by("order")
            recipes = Recipe.objects.all().order_by("name")

            return render(request, "app-schedules-meal-recipe.html",
                      context={"plan": plan, "days_name": days_name, "recipes": recipes})

        except Exception:
            raise Http404

    def post(self, request):

        if 'previous_page' not in request.POST:

            try:
                plan_id = request.POST.get("id")
                if int(plan_id) == int(request.session["plan_id"]):

                    meal_names = {
                        1: "Śniadanie",
                        2: "Drugie Śniadanie",
                        3: "Zupa",
                        4: "Drugie Danie",
                        5: "Kolacja",
                    }

                    recipeplan = Recipeplan()
                    order = int(request.POST.get("name"))
                    recipe = request.POST.get("recipe")
                    day_name = request.POST.get("day_name1")

                    recipeplan.meal_name = meal_names[order]
                    recipeplan.order = order
                    recipeplan.day_name_id = int(day_name) + 1
                    recipeplan.plan_id = plan_id
                    recipeplan.recipe_id = recipe
                    recipeplan.save()

                    return redirect(reverse("PlanAddDetailsView"))

                else:
                    return HttpResponse(status=404)


            except Exception:
                return HttpResponse(status=403)

        else:
            del request.session["plan_id"]
            return redirect(reverse("PlanView"))


class RecipeModifyView(View):

    def get(self, request, id):
        try:
            recipe = Recipe.objects.get(id=id)
            ingredients = recipe.ingredients
            ingredients = ingredients.split (",")
            preparations = recipe.preparation_recipe
            return render(request, "app-edit-recipe.html", context={"id": id, "recipe":recipe, "ingredients":ingredients, "preparations":preparations})
        except:
            return render(request, f"Błąd 404, wybrane id nie istnieje", status=404)

    def post(self,request, id):
            recipe=Recipe.objects.get(id=id)
            new_recipe_name = request.POST.get("recipe_name")
            new_recipe_description = request.POST.get ("recipe_description")
            new_recipe_time = request.POST.get ("recipe_time")
            new_recipe_preparation = request.POST.get ("recipe_preparations")
            new_recipe_ingredients = request.POST.get ("recipe_ingredients")
            if new_recipe_name and new_recipe_description and new_recipe_time and new_recipe_preparation and new_recipe_ingredients:
                recipe.name = new_recipe_name
                recipe.ingredients = new_recipe_ingredients
                recipe.description = new_recipe_description
                recipe.preparation_time = new_recipe_time
                recipe.preparation_recipe = new_recipe_preparation
                recipe.save()
                return redirect(reverse("RecipeListView"))
            else:
                message = "Wypełnij poprawnie wszystkie pola"
                recipe = Recipe.objects.get (id=id)
                ingredients = recipe.ingredients
                ingredients = ingredients.split (",")
                preparations = recipe.preparation_recipe
                return render (request, "app-edit-recipe.html",
                               context={"id": id, "recipe":recipe, "ingredients":ingredients, "preparations":preparations, "message":message})


class RecipeNewModifyView(View):
    def get (self, request, id):
        try:
            recipe = Recipe.objects.get (id=id)
            ingredients = recipe.ingredients
            ingredients = ingredients.split (",")
            preparations = recipe.preparation_recipe
            return render (request, "app-edit-recipe.html",
                           context={"id": id, "recipe": recipe, "ingredients": ingredients,
                                    "preparations": preparations})
        except:
            return HttpResponse (status=404)


    def post (self, request, id):
        new_recipe_name = request.POST.get ("recipe_name")
        new_recipe_description = request.POST.get ("recipe_description")
        new_recipe_time = request.POST.get ("recipe_time")
        new_recipe_preparation = request.POST.get ("recipe_preparations")
        new_recipe_ingredients = request.POST.get ("recipe_ingredients")
        if new_recipe_name and new_recipe_description and new_recipe_time and new_recipe_preparation and new_recipe_ingredients:
            Recipe.objects.create(name=new_recipe_name, description=new_recipe_description,
                                   preparation_time=new_recipe_time, preparation_recipe=new_recipe_preparation, votes=0,
                                   ingredients=new_recipe_ingredients)
            return redirect (reverse ("RecipeListView"))
        else:
            message = "Wypełnij poprawnie wszystkie pola"
            recipe = Recipe.objects.get (id=id)
            ingredients = recipe.ingredients
            ingredients = ingredients.split (",")
            preparations = recipe.preparation_recipe
            return render (request, "app-edit-recipe.html",
                           context={"id": id, "recipe": recipe, "ingredients": ingredients,
                                    "preparations": preparations, "message": message})



class ContactView(View):

    def get(self, request):

        try:
            page = Page.objects.get(slug="contact")
            description = page.description
            description = description.split(";")
            return render (request, "contact.html", context={"description": description})
        except:
            message = "Strona w przygotowaniu!"
            return render(request, "contact.html", context={"message":message})

        return render(request, "contact.html")



class AboutView(View):

    def get(self, request):
        about = Page.objects.filter(slug="about")
        return render(request, "about.html", context={"about": about})



class PlanEditView(View):

    def get(self, request, id):
        plan = Plan.objects.get(id=id)

        return render(request, "app-edit-schedules.html", context={"plan": plan})

    def post(self, request, id):
        plan = Plan.objects.get(id=id)
        plan.name = request.POST.get("name")
        plan.description = request.POST.get("description")
        plan.save()
        return redirect(reverse("PlanView"))

