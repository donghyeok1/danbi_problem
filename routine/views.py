from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny

from routine.models import Routine, RoutineResult
from routine.serializers import RoutineCreateUpdateSerializer, RoutineResultCreateUpdateDeleteSerializer


class RoutineViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Routine.objects.all()
    serializer_class = RoutineCreateUpdateSerializer

    def create(self, request, *args, **kwargs):
        response = super(RoutineViewSet, self).create(request, *args, **kwargs)
        data = {
            "data": response.data,
            "message": {
                "msg": "You have successfully created the routine.",
                "status": "ROUTINE_CREATE_OK"
            }
        }

        response.data = data
        return response

    def update(self, request, *args, **kwargs):
        response = super(RoutineViewSet, self).update(request, *args, **kwargs)
        data = {
            "data": response.data,
            "message": {
                "msg": "The routine has been modified.",
                "status": "ROUTINE_UPDATE_OK"
            }
        }

        response.data = data
        return response

class RoutineResultViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = RoutineResult.objects.all()
    serializer_class = RoutineResultCreateUpdateDeleteSerializer

    def create(self, request, pk, *args, **kwargs):
        request.data['routine_id'] = id
        response = super(RoutineResultViewSet, self).create(request, *args, **kwargs)
        data = {
            "data": response.data,
            "message": {
                "msg": "You have successfully created the routine result.",
                "status": "ROUTINE_RESULT_CREATE_OK"
            }
        }

        response.data = data
        return response
