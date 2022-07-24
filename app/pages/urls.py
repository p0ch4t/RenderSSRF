from django.urls import path
from pages.views import render_ssrf
from pages.views import config
from pages.views import home

urlpatterns = [
    path('', home,),
    path('config/', config,),
    path('browser/', render_ssrf),
]
