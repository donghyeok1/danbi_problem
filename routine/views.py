from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import date, datetime, timedelta
from routine.models import Routine, RoutineResult, RoutineDay
from routine.serializers import RoutineCreateUpdateSerializer, RoutineResultUpdateSerializer
from rest_framework import exceptions, status
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
        routine = response.data
        data = {
            "data": {
                "routine_id" : routine['routine_id']
            },
            "message": {
                "msg": "You have successfully created the routine.",
                "status": "ROUTINE_CREATE_OK"
            }
        }

        response.data = data
        return response

    def update(self, request, *args, **kwargs):
        response = super(RoutineViewSet, self).update(request, *args, **kwargs)
        routine = response.data
        data = {
            "data": {
                "routine_id" : routine['routine_id']
            },
            "message": {
                "msg": "The routine has been modified.",
                "status": "ROUTINE_UPDATE_OK"
            }
        }

        response.data = data
        return response



    def retrieve(self, request, *args, **kwargs):
        response = super(RoutineViewSet, self).retrieve(request, *args, **kwargs)
        routine = response.data
        if routine['is_deleted']:
            data_msg = {
                "message": {
                    "msg": "This routine was deleted",
                    "status": "ROUTINE_DETAIL_OK"
                }
            }
        else:
            days = list()
            routine_days = RoutineDay.objects.filter(routine_id=routine['routine_id']).values('day')
            routine_result = RoutineResult.objects.get(routine_id=routine['routine_id'])
            for routine_day in routine_days:
                days.append(routine_day['day'])

            data = {
                "goal" : routine['goal'],
                "id" : request.user.id,
                "result" : routine_result.result,
                "title" : routine['title'],
                "days" : days
                # routine_day 객체를 이용해 Routine 모델에 접근을 하면 n+1 문제가 일어나기 때문에
                # serializer에서 미리 받아온 response.data를 이용해 더 이상의 쿼리문이 발생하지 않게
                # 설계함.
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
        routines = response.data # 매번 쿼리문을 발생시키지 않기 위해 데이터를 routines에 저장해놓기.
        if q:
            if routines:
                # yyyy-mm-dd 형태의 요청값을 RoutineDay 모델에 저장된 day 형태로 변환
                year, month, day = map(int, q.split("-"))
                day_index = date(year, month, day).weekday()
                search_key = day_list[day_index]

                results = list()

                for routine in routines:
                    if not routine['is_deleted']:  # 삭제된 데이터는 보이지 않게 수정.
                        routine_result = RoutineResult.objects.get(routine_id=routine['routine_id'])
                        for _ in range(RoutineDay.objects.filter(routine_id=routine['routine_id'], day=search_key).count()):
                            # ORM의 count()가 len 함수보다 시간과 메모리가 최소화된다.
                            # count()는 ORM이기 때문에 SQL COUNT 쿼리를 실행해서 개수를 직접 계산
                            # len은 SQL 쿼리에서 모든 결과를 가져와서 Python 리스트로 변환한 다음 리스트의 길이를 계산
                            results.append({
                                "goal" : routine['goal'],
                                "id" : routine['routine_id'],
                                "result" : routine_result.result,
                                "title" : routine['title']
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
                    if not routine['is_deleted']:  # 삭제된 데이터는 보이지 않게 수정.
                        created = routine['created_at'] # 원래 ORM을 써서 created를 뽑아왔는데 이러면 매번 쿼리문 발생
                                                        # 그래서 serializer에서 created_at을 같이 불러와서 저장해놓고 쿼리문을
                                                        # 발생시키지 않은 상태로 활용
                        year, month, day = map(int, created.split("T")[0].split("-"))
                        if today_year == year and today_month == month and get_week_no(year, month, day) == get_week_no(today_year, today_month, today_day):
                            routine_result = RoutineResult.objects.get(routine_id=routine['routine_id'])
                            routine_days = RoutineDay.objects.filter(routine_id=routine['routine_id'])
                            days = list()
                            for routine_day in routine_days:
                                days.append(routine_day.day)
                            results.append({
                                "goal": routine['goal'],
                                "id": routine['routine_id'],
                                "result": routine_result.result,
                                "title": routine['title'],
                                "days" : days
                            })
                            # serializer에서 주어준 쿼리셋 데이터를 활용하지 않고 routine_result를 통해 정방향 참조를 해서
                            # routine 모델을 가져왔는데, 이렇게 되면 routine을 찾는 쿼리문을 추가로 더 날리게 됨.
                            # select_related를 이용해도 되지만, 이미 serializer에서 보내준 routines를 이용해
                            # 쿼리문을 줄임.
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
        routine_instance = self.get_object()
        routine_id = self.perform_destroy(routine_instance)
        data = {
            "data": {
                "routine_id" : routine_id
            },
            "message": {
                "msg": "The routine has been deleted.",
                "status": "ROUTINE_DELETE_OK"
            }
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)


    def perform_destroy(self, instance):
        instance.is_deleted = True
        routine_result = RoutineResult.objects.get(routine_id=instance.routine_id)
        routine_result.is_deleted = True
        instance.save()
        routine_result.save()
        return instance.routine_id

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
