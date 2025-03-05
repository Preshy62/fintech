from django.urls import path
from  .views import index
from django.contrib.auth.views import LoginView
from .views import signup_view



urlpatterns = [
    path('', index, name="index"),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
        path('register/', signup_view, name='register'),
]

