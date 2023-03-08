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
class RoutineCreateUpdateSerializer(serializers.ModelSerializer):
    days = ListField(write_only=True, min_length=1, max_length=7)
    class Meta:
        model = Routine
        fields = ['routine_id','title', 'category', 'goal', 'is_alarm', 'is_deleted', 'days', 'created_at', 'modified_at']
    def validate_days(self, days):
        global day_dict
        for day in days:
            if day not in day_dict.keys():
                raise serializers.ValidationError("요일 형식이 올바르지 않습니다.")
        return days

    def create(self, validated_data):
        days = validated_data.pop('days')
        user = self.context['request'].user

        routine = Routine(
            account_id=user,
            **validated_data
        )
        routine.save()

        for day in days:
            routine_day = RoutineDay(
                routine_id=routine,
                day=day
            )
            routine_day.save()

        routine_result = RoutineResult(
            routine_id=routine,
            result='NOT'
        )
        routine_result.save()

        return routine

    def update(self, instance, validated_data):
        days = validated_data.pop('days')
        instance.title = validated_data.get('title', instance.title)
        instance.category = validated_data.get('category', instance.category)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.alarm = validated_data.get('is_alarm', instance.is_alarm)
        # client에서 특정 데이터를 보내주지 않으면 원래 데이터로 치환.

        day_next_set = set(days)
        day_prev_set = set()

        for prev in RoutineDay.objects.filter(routine_id=instance):
            day_prev_set.add(prev.day)

        day_delete = day_prev_set - day_next_set
        day_create = day_next_set - day_prev_set

        for day in day_delete:
            RoutineDay.objects.filter(routine_id=instance, day=day).delete()
        for day in day_create:
            RoutineDay.objects.create(routine_id=instance, day=day)

        instance.save()
        return instance



class RoutineResultUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutineResult
        fields = ['result', 'is_deleted']

    def to_representation(self, instance):
        res = {"routine_result_id" : instance.routine_result_id}
        return res

    def update(self, instance, validated_data):
        instance.result = validated_data.get('result', instance.result)
        instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)
        instance.save()

        return instance
