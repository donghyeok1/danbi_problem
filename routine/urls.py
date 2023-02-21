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
    'get' : 'retrieve',
    'delete' : 'destroy'
})

routine_result_list = views.RoutineResultViewSet.as_view({
    'get' : 'list',
})

routine_result_detail = views.RoutineResultViewSet.as_view({
    'put' : 'update',
    'delete' : 'destroy'
})


urlpatterns =[
    path('routines/', routine_list, name='routine-list'),
    path('routines/<int:pk>/', routine_detail, name='routine-detail'),
    path('routines/<int:pk>/results/', routine_result_list, name='routine-result-list'),
    path('routines/<int:id>/results/<int:pk>/', routine_result_detail, name='routine-result-detail'),
]