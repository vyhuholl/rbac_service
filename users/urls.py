from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    AccountDeleteView,
    UserUpdateView,
)

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete/', AccountDeleteView.as_view(), name='delete'),
    path('update/', UserUpdateView.as_view(), name='update'),
]
