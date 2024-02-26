from django.urls import path
from . import views

urlpatterns = [
    path('', views.splash_page, name='splash'),
    path('sign_up_mk/', views.sign_up_mk, name='sign_up_mk'),
    path('success/', views.success, name='success'),
]
