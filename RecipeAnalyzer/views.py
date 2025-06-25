from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest
from .ai_client import AzureOpenAIAIClient
from .forms import RecipeURLForm
from .recipe_scraper import DefaultRecipeScraper
import logging

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class AllergenExtractorView(View):
    """
    API endpoint for extracting allergens from recipe URLs.
    """
    
    def post(self, request):
        url = request.POST.get('url')
        if not url:
            return HttpResponseBadRequest('Missing URL')
        scraper = DefaultRecipeScraper()
        try:
            all_text = scraper.scrape(url)
        except ValueError as e:
            return HttpResponseBadRequest(str(e))
        ai_client = AzureOpenAIAIClient()
        ingredient_lines = ai_client.extract_ingredients(all_text)
        recipe_text = '\n'.join(ingredient_lines)
        allergens = ai_client.extract_allergens(recipe_text)
        return JsonResponse({
            'original_text': recipe_text,
            'allergens': allergens
        })

class RecipeWebView(View):
    """
    Web interface for submitting recipe URLs and displaying extracted ingredients and allergens.
    """
    
    def get(self, request):
        form = RecipeURLForm()
        return render(request, 'RecipeAnalyzer/recipe_form.html', {'form': form})

    def post(self, request):
        form = RecipeURLForm(request.POST)
        ingredients = allergens = error = None
        if form.is_valid():
            url = form.cleaned_data['url']
            logger.info(f"\nReceived recipe URL: {url}\n")
            scraper = DefaultRecipeScraper()
            try:
                all_text = scraper.scrape(url)
                ai_client = AzureOpenAIAIClient()
                ingredient_lines = ai_client.extract_ingredients(all_text)
                ingredients = ingredient_lines
                allergens = ai_client.extract_allergens('\n'.join(ingredient_lines))
            except Exception as e:
                error = str(e)
        return render(request, 'RecipeAnalyzer/recipe_form.html', {'form': form, 'ingredients': ingredients, 'allergens': allergens, 'error': error})

def root_redirect(request):
    """
    Redirects root URL to the web interface.
    """
    return redirect('/web/')
