# README.md

# Allergen Extractor

A modular Django-based system to extract recipe text and allergenic ingredients from online cookbooks using Azure OpenAI.

## Features
- Input: URL of a recipe page
- Scrapes and parses recipe text
- Extracts ingredients and allergens using Azure OpenAI
- API and web interface
- Modular, extensible architecture
- Error handling and logging

## Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/NoamGivaty/Muvan.ai.git
   cd Muvan.ai
   ```
2. Create and activate a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Add your Azure OpenAI API key to the `.env` file:
   - Open the `.env` file in the project root
   - Add your Azure OpenAI API key:
     ```
     AZURE_OPENAI_KEY=your-azure-openai-api-key-here
     ```

5. Apply Django migrations (required for built-in apps):
   ```sh
   python3 manage.py migrate
   ```
6. Start the Django server:
   ```sh
   python3 manage.py runserver
   ```
   
## Usage - Web Interface
1. Open your browser and go to `http://127.0.0.1:8000/web/`.
2. Enter the URL of a recipe page into the input field.
3. Click the submit button.
4. Wait a few moments while the system scrapes the recipe, analyzes the ingredients, and extracts allergens.
5. The results will be displayed on the page, including the parsed ingredients and detected allergens.

## Architecture
- `ai_client.py`: AI client interface and Azure OpenAI implementation
- `recipe_scraper.py`: Scraper interface and default implementation
- `views.py`: API and web views
