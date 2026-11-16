from django.urls import path
from . import views

app_name = 'routes'

urlpatterns = [
    path('', views.route_list, name='route_list'),
    path('<int:pk>/', views.route_detail, name='route_detail'),
]
