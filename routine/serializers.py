from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import ListField

from .models import Routine, RoutineDay

class RoutineDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutineDay
        fields = ['day']

class RoutineCreateSerializer(serializers.ModelSerializer):
    days = ListField(write_only=True, min_length=1, max_length=7)
    class Meta:
        model = Routine
        fields = ['title', 'category', 'goal', 'is_alarm', 'days']

    def validate_days(self, days):
        day_set = {'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'}
        for day in days:
            if day not in day_set:
                raise serializers.ValidationError("요일 형식이 올바르지 않습니다.")
        return days

    def to_representation(self, instance):
        res = {
            'data' : {"routine_id" : instance.routine_id},
            'message' : {
                'msg' : "You have successfully created the routines.",
                'status' : "ROUTINE_CREATE_OK"
            }
        }
        return res
    # 성공 data routine_id만 나오게

    def create(self, validated_data):
        days = validated_data.pop('days')
        user = self.context['request'].user
        routine_instance = Routine.objects.create(account_id=user, **validated_data)

        for day in days:
            RoutineDay.objects.create(routine_id=routine_instance, day=day)

        return routine_instance

