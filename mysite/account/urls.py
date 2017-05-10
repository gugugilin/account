from django.conf.urls import url
from . import views 

urlpatterns = [
    url(r'^$', views.post_list),
    url(r'register/', views.register),
    url(r'login/', views.login),
    url(r'pass/', views.login_pass),
    url(r'myaccount/', views.myaccount),
]