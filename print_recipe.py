import sys
import requests

def print_ingredients_and_allergens(url):
    resp = requests.post('http://127.0.0.1:8000/api/extract/', data={'url': url})
    data = resp.json()
    print('\n==== All Ingredients ====')
    for line in data['original_text'].split('\n'):
        print(f'  - {line}')
    print('\n==== Allergenic Ingredients ====')
    for a in data['allergens']:
        print(f'  - {a}')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python print_recipe.py <recipe_url>")
        sys.exit(1)
    print_ingredients_and_allergens(sys.argv[1])
