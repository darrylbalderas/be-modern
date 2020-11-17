# be-modern

## Instructions

```bash
python3 -m venv graphdjango
source graphdjango/bin/activate
pip install -r requirements.txt
django-admin startproject modern_catalog .
django-admin startapp programs
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata programs
```

## Questions

- Can activities be repeated in multiple sections ?
- Can sections be repeated in multiple program ?
- Is there any image extension we are limited to?
- Is the companies PostgreSQL database hosted on AWS ? Aurora ?
- What is the minimum or maximum number of choices within an activity ?
- How big is the html content in the activity ?
- What are the limits of height and width for an overview image in a section ?
- What is an ordering index in a section ? (Is that ordering number in which the program has you follow)

## Resources

- ['Build small docker images'](https://towardsdatascience.com/how-to-build-slim-docker-images-fast-ecc246d7f4a7)
- ['Django and Uvicorn'](https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/uvicorn/)
- [](https://www.uvicorn.org/)
- [](https://docs.docker.com/compose/django/)
- [](https://docs.graphene-python.org/projects/django/en/latest/testing/)
- [](https://stackabuse.com/building-a-graphql-api-with-django/)
- [](https://www.fullstacklabs.co/blog/django-graphene-rest-graphql)
- [](https://django-graphql-jwt.domake.io/en/latest/index.html)
