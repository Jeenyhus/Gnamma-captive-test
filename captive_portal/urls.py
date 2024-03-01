from django.urls import path
from . import views

urlpatterns = [
    path('', views.splash, name='splash'),
    path('sign_up_vc/', views.signup, name='sign_up_vc'),
    path('success/', views.success, name='success'),
]
