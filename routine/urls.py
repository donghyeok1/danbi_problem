from django.urls import path, include
from rest_framework.routers import DefaultRouter

from routine import views

router_routine = DefaultRouter()
router_routine.register('', views.RoutineViewSet)

router_result = DefaultRouter()
router_result.register('results', views.RoutineResultViewSet)

routine_list = views.RoutineViewSet.as_view({
    'get' : 'list',
    'post' : 'create'
})

routine_detail = views.RoutineViewSet.as_view({
    'put' : 'update',
    'get' : 'retrieve'
})

routine_result_list = views.RoutineResultViewSet.as_view({
    'get' : 'list',
    'post' : 'create',
})

urlpatterns =[
    path('routines/', routine_list, name='routine-list'),
    path('routines/<int:id>/', routine_detail, name='routine-detail'),
    path('routines/<int:pk>/results/', routine_result_list, name='routine-result-list'),
]