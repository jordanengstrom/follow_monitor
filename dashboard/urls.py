from django.urls import path, re_path
from django.conf.urls import include
# from .views import (
#     TwitterUserListView
# )
from . import views

urlpatterns = [
    path('', views.home, name='dashboard-home'),
    path(r'^welcome(?state=\w+)', views.welcome, name='dashboard-welcome')
]
