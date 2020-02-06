from django.urls import path,re_path
from . import views

urlpatterns =[
    path('',views.home,name='blog-home'),
    re_path(r'^about/',views.about,name='blog-about'),
]