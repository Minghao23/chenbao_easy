"""chenbao_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
# from django.contrib import admin
from chenbao import views

urlpatterns = [
    url(r'^init', views.get_init_data),
    url(r'^update', views.update_absent_persons),
    url(r'^check', views.check_chat_content),
    url(r'^generate', views.generate_email),
    url(r'^person_stat', views.person_stat),
    url(r'^person_history', views.person_history),
    url(r'^total_stat', views.total_stat),
    url(r'^', views.run),
]
