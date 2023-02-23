from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from datetime import date, datetime, timedelta
from routine.models import Routine, RoutineResult, RoutineDay
from routine.serializers import RoutineCreateUpdateSerializer, RoutineResultUpdateSerializer
from rest_framework import exceptions
global day_list
day_list = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']


class RoutineViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Routine.objects.all()
    serializer_class = RoutineCreateUpdateSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(account_id=self.request.user)
        return qs

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



    def retrieve(self, request, *args, **kwargs):
        response = super(RoutineViewSet, self).retrieve(request, *args, **kwargs)
        routine = Routine.objects.get(routine_id=response.data['routine_id'])

        days = list()

        for routine_day in routine.routine_day_set.all():
            days.append(routine_day.day)

        data = {
            "goal" : routine.goal,
            "id" : routine.account_id.pk,
            "result" : routine.routine_result_set.first().result,
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

    def list(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
        global day_list
        response = super(RoutineViewSet, self).list(request, *args, **kwargs)
        routines = response.data
        if q:
            if routines:
                # yyyy-mm-dd 형태의 요청값을 RoutineDay 모델에 저장된 day 형태로 변환
                year, month, day = map(int, q.split("-"))
                day_index = date(year, month, day).weekday()
                search_key = day_list[day_index]

                results = list()

                for routine in routines:
                    for routine_day_instance in RoutineDay.objects.filter(routine_id=routine['routine_id'], day=search_key):
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
        else:
            dt_now = datetime.now()
            today_year, today_month, today_day = dt_now.year, dt_now.month, dt_now.day
            def get_date(y, m, d):
                '''y: year(4 digits)
                 m: month(2 digits)
                 d: day(2 digits'''
                s = f'{y:04d}-{m:02d}-{d:02d}'
                return datetime.strptime(s, '%Y-%m-%d')

            def get_week_no(y, m, d):
                target = get_date(y, m, d)
                firstday = target.replace(day=1)
                if firstday.weekday() == 6:
                    origin = firstday
                elif firstday.weekday() < 3:
                    origin = firstday - timedelta(days=firstday.weekday() + 1)
                else:
                    origin = firstday + timedelta(days=6 - firstday.weekday())
                return (target - origin).days // 7 + 1

            if routines:
                results = list()

                for routine in routines:
                    created = Routine.objects.get(routine_id=routine['routine_id']).created_at
                    year, month, day = created.year, created.month, created.day

                    if today_year == year and today_month == month and get_week_no(year, month, day) == get_week_no(today_year, today_month, today_day):
                        routine_result = RoutineResult.objects.get(routine_id=routine['routine_id'])
                        routine_days = RoutineDay.objects.filter(routine_id=routine['routine_id'])
                        days = list()

                        for routine_day in routine_days:
                            days.append(routine_day.day)

                        results.append({
                            "goal": routine_result.routine_id.goal,
                            "id": routine_result.routine_id.routine_id,
                            "result": routine_result.result,
                            "title": routine_result.routine_id.title,
                            "days" : days
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
                        "data" : "이번 주 작성한 루틴이 없습니다."
                    }

                response.data = data_msg

                return response

            else:
                raise exceptions.NotFound("기록된 루틴이 없습니다.")
    def destroy(self, request, *args, **kwargs):
        routine_result_instance = self.get_object()
        response = super(RoutineViewSet, self).destroy(request, *args, **kwargs)
        data = {
            "data": {
                "routine_id" : routine_result_instance.routine_id
            },
            "message": {
                "msg": "The routine has been deleted.",
                "status": "ROUTINE_DELETE_OK"
            }
        }

        response.data = data
        return response

    def perform_destroy(self, instance):
        instance.is_deleted = True
        routine_result_instance = instance.routine_day_set.first()
        routine_result_instance.is_deleted = True
        instance.save()
        routine_result_instance.save()

class RoutineResultViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = RoutineResult.objects.all()
    serializer_class = RoutineResultUpdateSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(routine_id__account_id=self.request.user)
        return qs

    def update(self, request, *args, **kwargs):
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

    def destroy(self, request, *args, **kwargs):
        routine_result_instance = self.get_object()
        response = super(RoutineResultViewSet, self).destroy(request, *args, **kwargs)
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

    def perform_destroy(self, instance):
        instance.is_deleted = True
        routine_instance = instance.routine_id
        routine_instance.is_deleted = True
        instance.save()
        routine_instance.save()
