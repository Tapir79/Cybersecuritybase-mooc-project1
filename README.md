# MOOC Cybersecurity Base Project I 2024 
Web application that has at least five different flaws from the OWASP top ten list as well as their fixes. The project uses OWASP Top 10 2021: https://owasp.org/Top10/.  
The project was created with this tutorial: https://docs.djangoproject.com/en/5.1/intro/tutorial01/ 

# Install and Run the project

## Create python venv 
- Read this guide (Python 3): https://cybersecuritybase.mooc.fi/installation-guide
- `python -m venv recipes_env`
### Linux
- `source recipes_env/bin/activate` 
### Windows
- `.\recipes_env\Scripts\activate`

## Install dependencies to the virtual environment
- `pip install -r requirements.txt`


# The vulnerabilities and their fixes 

## 1. A01:2021 – Broken Access Control
https://owasp.org/Top10/A01_2021-Broken_Access_Control/
In `views.py`:
````
def add_recipe(request):  # Missing login_required decorator
    # Existing code for adding a recipe
````

Solution: Ensure only authenticated users can access this view.
````
from django.contrib.auth.decorators import login_required

@login_required
def add_recipe(request):
    # Code for adding a recipe
````

## 2. A02:2021 – Cryptographic Failures
https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
In `settings.py`:
````
SECRET_KEY = 'recipes-secret-key'  # Sensitive information hardcoded
````

Solution: Use environment variables to keep secrets secure.

````
import os

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'default-secret-key')
````

Set the DJANGO_SECRET_KEY in your environment instead of storing it in the codebase. 


## 3. A03:2021 – Injection
https://owasp.org/Top10/A03_2021-Injection/
In `views.py`:

````
def recipe_detail(request, recipe_id):
    # Insecure: Directly injecting `recipe_id` into the query without sanitization
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM recipe WHERE id = {recipe_id}") # vulnerable
        recipe = cursor.fetchone()
````

An attacker could send a request with javascript like this:

````
fetch("/recipe_detail?recipe_id=1; DROP TABLE recipe; --")
    .then(response => response.text())
    .then(data => console.log(data));
````

It could drop the recipe table. 

Solution: Use parameterized queries to prevent SQL injection.

````
from django.db import connection

def recipe_detail(request, recipe_id):
    # Insecure: Directly injecting `recipe_id` into the query without sanitization
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM recipe WHERE id = %s", [recipe_id]) # fixed
        recipe = cursor.fetchone()
````

## 4. A05:2021 – Security Misconfiguration
https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
Vulnerability Example: Allowing DEBUG mode in production exposes sensitive information through error messages.

In `settings.py`:

````
DEBUG = True  # Leaving DEBUG enabled in production is a risk
````

Solution: Disable DEBUG mode in production.
Set DJANGO_DEBUG=False or don't add the environment variable in production to prevent detailed error messages from being shown to users. The fallback is False meaning that no env var always return False. 

````
import os

DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'
````




## 5. A07:2021 – Identification and Authentication Failures
https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
Vulnerability Example: Using weak password policies can lead to easily guessable passwords.

In `settings.py`:

````
AUTH_PASSWORD_VALIDATORS = []  # No password validation rules
````

Solution: Implement strong password validation.

````
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
````
