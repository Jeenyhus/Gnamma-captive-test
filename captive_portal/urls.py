from django.urls import path
from . import views

app_name = 'captive_portal'
urlpatterns = [
    path('', views.splash_page, name='splash'),
    path('sign_up/', views.sign_up, name='signup'),
    path('success/', views.success, name='success'),
]
