"""scraping_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from accounts.views import (
    login_view, logout_view, register_view, update_view, delete_view, contact
)


urlpatterns = [
    path('login/', login_view,name='login'),
    path('logout/', logout_view,name='logout'),
    path('register/', register_view,name='register'),
    path('update/', update_view,name='update'),
    path('delete/', delete_view,name='delete'),
    path('contact/', contact, name='contact'),
]
