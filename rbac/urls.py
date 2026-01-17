from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'rbac'

router = DefaultRouter()
router.register(r'roles', views.RoleViewSet)
router.register(r'business-elements', views.BusinessElementViewSet)
router.register(r'access-rules', views.AccessRoleRuleViewSet)

urlpatterns = [
    path('access/', views.AccessView.as_view(), name='access'),
    path('', include(router.urls)),
]
