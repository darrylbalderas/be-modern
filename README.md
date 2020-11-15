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

- Can activites be used in multiple sections ?
- Is there any image extension we are limited ?
- Is your postgres hosted on AWS ? Aurora ?
