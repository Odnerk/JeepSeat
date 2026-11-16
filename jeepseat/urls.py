from django.contrib import admin
from django.urls import path, include

from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.home_view, name='home'),
    path('routes/', include('routes.urls', namespace='routes')),
    path('vehicles/', include('vehicles.urls', namespace='vehicles')),
    path('trips/', include('trips.urls', namespace='trips')),
    path('feedback/', include('feedback.urls', namespace='feedback')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', user_views.logout_view, name='logout'),
    path('register/', user_views.register_view, name='register'),
]
