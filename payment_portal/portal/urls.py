
from django.urls import path,include
from . import views
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('oauth2/', include('django_auth_adfs.urls')),
    path('home/', views.home_view, name='home'),
]