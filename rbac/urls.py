from django.urls import path
from . import views

app_name = 'rbac'

urlpatterns = [
    path('access/', views.AccessView.as_view(), name='access'),
]
