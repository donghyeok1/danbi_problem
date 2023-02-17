from django.contrib import admin

from routine.models import Routine, RoutineResult, RoutineDay


@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    list_display = ['routine_id', 'account_id', 'title', 'category', 'goal', 'created_at', 'modified_at']
    list_display_links = ['routine_id']

@admin.register(RoutineResult)
class RoutineResultAdmin(admin.ModelAdmin):
    list_display = ['routine_result_id', 'routine_title', 'result']
    list_display_links = ['routine_title']

    def routine_title(self, obj):
        return obj.routine_id.title

@admin.register(RoutineDay)
class RoutineDayAdmin(admin.ModelAdmin):
    list_display = ['routine_title', 'day']
    list_display_links = ['routine_title']

    def routine_title(self, obj):
        return obj.routine_id.title
