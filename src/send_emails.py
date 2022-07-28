import asyncio #multiprosessing/multithreading
import os, sys
import django
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

django.setup()
from scrapping.models import Vacancy


# https://docs.djangoproject.com/en/3.0/topics/email/#sending-alternative-content-types
from scraping_service.settings import EMAIL_HOST_USER
empty = '<h2> Sorry vacansies are not present today<h2/>'
subject = 'Your vacansies'
text_content = 'Your vacansies'
from_email = EMAIL_HOST_USER

User = get_user_model()
qs = User.objects.filter(send_email = True).values('city','language','email')

users_dct = {}

for i in qs:
    users_dct.setdefault((i['city'],i['language']),[])
    users_dct[(i['city'],i['language'])].append(i['email'])

if users_dct:
    params = {
        'city_id__in':[],
        'language_id__in':[],
    }

    for pair in users_dct.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])

    qs = Vacancy.objects.filter(**params).values()[:10]  # last 10 vacansy

    vacancies = {}

    for i in qs:
        vacancies.setdefault((i['city_id'],i['language_id']),[])
        vacancies[(i['city_id'],i['language_id'])].append(i)

    for keys,emails in users_dct.items():
        rows = vacancies.get(keys,[])
        html = ''
        for row in rows:
            html += f'<a href="{row["url"]}" target="_blank">link</a> Title: {row["title"]}'
            html += '<p>{row["description"]}</p>'
            html += '<p>{row["company"]}</p><br><hr>'
        _html = html if html else empty

        for email in emails:
            to= email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(_html, "text/html")
            msg.send()





