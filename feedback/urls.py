from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('', views.complaint_list, name='complaint_list'),
]
