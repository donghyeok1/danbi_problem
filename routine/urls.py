from django.urls import path, include
from rest_framework.routers import DefaultRouter

from routine import views

router = DefaultRouter()
router.register('routine', views.RoutineViewSet)

urlpatterns =[
    path('', include(router.urls)),
]