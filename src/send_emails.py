import asyncio #multiprosessing/multithreading
import os, sys
import django
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
import datetime
from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

django.setup()
from scrapping.models import Vacancy,Error,url
# https://docs.djangoproject.com/en/3.0/topics/email/#sending-alternative-content-types
from scraping_service.settings import EMAIL_HOST_USER
ADMIN_USER = EMAIL_HOST_USER
today = datetime.date.today()

empty = '<h2> Sorry vacansies are not present today<h2/>'
subject = f'Your vacansies on {today}'
text_content = f'Your vacansies on {today}'
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

    qs = Vacancy.objects.filter(**params,timestamp = today).values()

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

qs = Error.objects.filter(timestemp = today)
subject = ''
text_content = ''
to = ADMIN_USER
if qs.exists():
    error = qs.first()
    data = error.data

    content = ''
    for i in data:
        content+=f'<a href="{i["url"]}" target="_blank">link</a> ERROR: {i["title"]}'

    subject = f'Errors scraping on {today}'
    text_content = 'Errors scraping'

    # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    # msg.attach_alternative(content, "text/html")
    # msg.send()

qs = url.objects.all().values('city','language')
urls_dct = {(i['city'],i['language']):True for i in qs}
urls_err = ''
for keys in users_dct.keys():
    if  keys not in urls_dct:
        urls_err += f'<p> "for city {i["keys[0]"]}" ERROR: {i["keys[1]"]} is not url </p><br>'

if urls_err:
    subject+='Is not find urls'


if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(content, "text/html")
    msg.send()




