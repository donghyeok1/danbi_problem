from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from datetime import date
from routine.models import Routine, RoutineResult, RoutineDay
from routine.serializers import RoutineCreateUpdateSerializer, RoutineResultUpdateDeleteSerializer
from rest_framework import exceptions
global day_list
day_list = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
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
        try:
            routine_instance = Routine.objects.get(routine_id=self.kwargs.get('pk'))
            if request.user.pk == routine_instance.account_id.pk:
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
            else:
                raise exceptions.PermissionDenied("해당 루틴을 수정할 권한이 없습니다.")
        except Routine.DoesNotExist:
            raise exceptions.NotFound("수정할 루틴이 없습니다.")


    def retrieve(self, request, *args, **kwargs):
        try:
            routine = Routine.objects.get(
                routine_id=self.kwargs.get('pk')
            )
            if routine.account_id.pk == request.user.pk:
                response = super(RoutineViewSet, self).retrieve(request, *args, **kwargs)
                day_instances = routine.routine_day_set.all()

                days = list()

                for day_instance in day_instances:
                    days.append(day_instance.day)

                result_instance = routine.routine_result_set.first()

                data = {
                    "goal" : routine.goal,
                    "id" : routine.account_id.pk,
                    "result" : result_instance.result,
                    "title" : routine.title,
                    "days" : days
                }

                data_msg = {
                    "data": data,
                    "message": {
                        "msg": "Routine lookup was successful.",
                        "status": "ROUTINE_DETAIL_OK"
                    }
                }

                response.data = data_msg
                return response
            else:
                raise exceptions.PermissionDenied("해당 루틴을 열람할 권한이 없습니다.")
        except Routine.DoesNotExist:
            raise exceptions.NotFound("기록된 루틴이 없습니다.")
    def list(self, request, *args, **kwargs):
        global day_list
        routines = Routine.objects.filter(account_id=request.user.pk)
        if routines:
            response = super(RoutineViewSet, self).list(request, *args, **kwargs)
            # yyyy-mm-dd 형태의 요청값을 RoutineDay 모델에 저장된 day 형태로 변환
            year, month, day = map(int, request.data['today'].split("-"))
            day_index = date(year, month, day).weekday()
            search_key = day_list[day_index]

            results = list()

            for routine in routines:
                for routine_day_instance in RoutineDay.objects.filter(routine_id=routine.routine_id, day=search_key):
                    routine_result_instance = routine_day_instance.routine_id.routine_result_set.first()
                    results.append({
                        "goal" : routine_day_instance.routine_id.goal,
                        "id" : routine_day_instance.routine_id.routine_id,
                        "result" : routine_result_instance.result,
                        "title" : routine_day_instance.routine_id.title
                    })
            if results:
                data_msg = {
                    "data": results,
                    "message": {
                        "msg": "Routine lookup was successful.",
                        "status": "ROUTINE_LIST_OK"
                    }
                }
            else:
                data_msg = {
                    "data" : "검색한 요일의 루틴이 없습니다."
                }

            response.data = data_msg

            return response

        else:
            raise exceptions.NotFound("기록된 루틴이 없습니다.")

    def destroy(self, request, *args, **kwargs):
        try:
            routine_instance = Routine.objects.get(routine_id=self.kwargs.get('pk'))

            if request.user.pk == routine_instance.account_id.pk:
                response = super(RoutineViewSet, self).destroy(request, *args, **kwargs)
                self.perform_destroy(routine_instance)
                data = {
                    "data": {
                        "routine_id" : routine_instance.routine_id
                    },
                    "message": {
                        "msg": "The routine has been deleted.",
                        "status": "ROUTINE_DELETE_OK"
                    }
                }

                response.data = data
                return response
            else:
                raise exceptions.PermissionDenied("해당 루틴을 삭제할 권한이 없습니다.")
            return response
        except Routine.DoesNotExist:
            raise exceptions.NotFound("존재하지 않는 루틴입니다.")
    def perform_destroy(self, instance):
        instance.is_deleted = True
        routine_result_instance = instance.routine_day_set.first()
        routine_result_instance.is_deleted = True
        instance.save()
        routine_result_instance.save()

class RoutineResultViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = RoutineResult.objects.all()
    serializer_class = RoutineResultUpdateDeleteSerializer

    def update(self, request, *args, **kwargs):
        try:
            routine_instance = Routine.objects.get(routine_id=self.kwargs.get('pk'))
            if request.user.pk == routine_instance.account_id.pk:
                response = super(RoutineResultViewSet, self).update(request, *args, **kwargs)
                data = {
                    "data": response.data,
                    "message": {
                        "msg": "The Routine's result has been modified",
                        "status": "ROUTINE_RESULT_UPDATE_OK"
                    }
                }

                response.data = data
                return response
            else:
                raise exceptions.PermissionDenied("해당 루틴 결과를 수정할 권한이 없습니다.")
        except Routine.DoesNotExist:
            raise exceptions.NotFound("수정할 루틴 결과가 없습니다.")
    def destroy(self, request, *args, **kwargs):
        try:
            routine_result_instance = RoutineResult.objects.get(routine_result_id=self.kwargs.get('pk'))
            if request.user.pk == routine_result_instance.routine_id.account_id.pk:
                response = super(RoutineResultViewSet, self).destroy(request, *args, **kwargs)
                self.perform_destroy(routine_result_instance)

                data = {
                    "data": {
                        "routine_result_id" : routine_result_instance.routine_id.routine_id
                    },
                    "message": {
                        "msg": "The routine result has been deleted.",
                        "status": "ROUTINE_DELETE_OK"
                    }
                }

                response.data = data
                return response
            else:
                raise exceptions.PermissionDenied("해당 루틴 결과를 삭제할 권한이 없습니다.")
        except Routine.DoesNotExist:
            raise exceptions.NotFound("존재하지 않는 루틴입니다.")
    def perform_destroy(self, instance):
        instance.is_deleted = True
        routine_instance = instance.routine_id
        routine_instance.is_deleted = True
        instance.save()
        routine_instance.save()

class TrashViewSet(ModelViewSet):
    pass