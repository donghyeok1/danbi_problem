from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import ListField
from datetime import datetime
from .models import Routine, RoutineDay, RoutineResult

global day_dict
day_dict = {
            'MON' : 0,
            'TUE' : 1,
            'WED' : 2,
            'THU' : 3,
            'FRI' : 4,
            'SAT' : 5,
            'SUN' : 6
        }
class RoutineDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutineDay
        fields = ['day']

class RoutineCreateUpdateSerializer(serializers.ModelSerializer):
    days = ListField(write_only=True, min_length=1, max_length=7)
    class Meta:
        model = Routine
        fields = ['title', 'category', 'goal', 'is_alarm', 'days']
    def validate_days(self, days):
        global day_dict
        day_list = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']

        for day in days:
            if day not in day_dict.keys():
                raise serializers.ValidationError("요일 형식이 올바르지 않습니다.")
            today_index = datetime.today().weekday()
            if today_index > day_dict[day]:
                raise serializers.ValidationError(
                    f"오늘은 {day_list[today_index]}입니다."
                    f"{day_list[today_index]}보다 이전의 일정은 등록하실수 업습니다."
                )
        return days


    def to_representation(self, instance):
        res = {"routine_id" : instance.routine_id}
        return res

    def create(self, validated_data):
        days = validated_data.pop('days')
        user = self.context['request'].user
        routine_instance = Routine.objects.create(account_id=user, **validated_data)

        for day in days:
            RoutineDay.objects.create(routine_id=routine_instance, day=day)

        return routine_instance

    def update(self, instance, validated_data):
        days = validated_data.pop('days')
        instance.title = validated_data.get('title', instance.title)
        instance.category = validated_data.get('category', instance.category)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.alarm = validated_data.get('is_alarm', instance.is_alarm)

        day_pre_set = set(days)
        day_prev_set = set()

        for prev in RoutineDay.objects.filter(routine_id=instance):
            day_prev_set.add(prev.day)

        day_delete = day_prev_set - day_pre_set
        day_create = day_pre_set - day_prev_set

        for day in day_delete:
            RoutineDay.objects.filter(routine_id=instance, day=day).delete()
        for day in day_create:
            RoutineDay.objects.create(routine_id=instance, day=day)

        instance.save()
        return instance

class RoutineResultCreateUpdateDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutineResult
        fields = ['routine_id', 'result', 'is_deleted']

    def to_representation(self, instance):
        res = {"routine_result_id" : instance.routine_result_id}
        return res

    def create(self, validated_data):
        try:
            routine_result_instance = RoutineResult.objects.get(routine_id=validated_data['routine_id'])
            raise serializers.ValidationError("이미 결과가 존재합니다.")
        except RoutineResult.DoesNotExist:
            routine_result_instance = RoutineResult.objects.create(**validated_data)
            return routine_result_instance

