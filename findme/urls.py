"""findme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from findme.views import *
from django.conf.urls import handler404
from findme.find_cards import find_cards_view

handler404 = error404

urlpatterns = [
#    url(r'^admin/', admin.site.urls),
    url(r'^$', gen_cluster),
    url(r'^cluster([1])/', gen_cluster),
#    url(r'^find_cards/', find_cards_view)
#    url(r'^cantina/([a-z]+)', get_phished),
#    url(r'^got_phished/([a-z0-9]+)', got_phished),
#    url(r'^leaving/([a-z]+)', leaving_phish),
#    url(r'^dashboard', phish_analytics),
#    url(r'^send_phish', send_phish),
#    url(r'^sendphish/(.*)', sendphish),
#    url(r'^user-data/(?P<username>[-\w]+)/?', get_user_data)
]
