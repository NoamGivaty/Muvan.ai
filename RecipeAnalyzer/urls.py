from django.urls import path
from .views import AllergenExtractorView, RecipeWebView, root_redirect

urlpatterns = [
    path('', root_redirect),
    path('api/extract/', AllergenExtractorView.as_view()),
    path('web/', RecipeWebView.as_view(), name='recipe_web'),
]
