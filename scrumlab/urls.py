from django.urls import path, re_path
from django.contrib import admin
from django.views.i18n import JavaScriptCatalog


from jedzonko.views import (IndexView, RecipeDetailView, RecipeListView, PlanDetailView, RecipeNewModifyView,
                            LandingPageView, RecipeAddView, RecipeModifyView, PlanView, PlanAddView, PlanAddDetailsView, ContactView, AboutView, PlanEditView)
urlpatterns = [
    re_path(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    re_path(r'^admin/', admin.site.urls),
    #re_path(r'^index/$', IndexView.as_view()),
    re_path(r'^$', LandingPageView.as_view(), name='LandingPageView'),
    re_path(r'^main/$', IndexView.as_view(), name='IndexView'),
    re_path(r'^recipe/(?P<id>\d+)/$', RecipeDetailView.as_view(), name='RecipeDetailView'),
    re_path(r'^recipe/list/$', RecipeListView.as_view(), name="RecipeListView"),
    re_path(r'^recipe/add/$', RecipeAddView.as_view(), name='RecipeAddView'),
    re_path(r'^recipe/modify/(?P<id>\d+)/$', RecipeModifyView.as_view(), name='RecipeModifyView'),
    re_path(r'^recipe/new/modify/(?P<id>\d+)/$', RecipeNewModifyView.as_view(), name='RecipeNewModifyView'),
    re_path(r'^plan/list/$', PlanView.as_view(), name='PlanView'),
    re_path(r'^plan/add/$', PlanAddView.as_view(), name='PlanAddView'),
    re_path(r'^plan/edit/(?P<id>\d*)/$', PlanEditView.as_view(), name='PlanEditView'),
    re_path(r'^plan/add/details/$', PlanAddDetailsView.as_view(), name='PlanAddDetailsView'),
    re_path(r'^contact/$', ContactView.as_view(), name='ContactView'),
    re_path(r'^about/$', AboutView.as_view(), name='AboutView'),
    re_path(r'^plan/(?P<id>\d+)$', PlanDetailView.as_view(), name='PlanDetailView'),
]
