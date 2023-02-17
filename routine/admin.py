from django.contrib import admin

from routine.models import Routine, RoutineResult, RoutineDay


@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    list_display = ['routine_id', 'account_id', 'title', 'category', 'goal']
    list_display_links = ['routine_id']

@admin.register(RoutineResult)
class RoutineResultAdmin(admin.ModelAdmin):
    pass

@admin.register(RoutineDay)
class RoutineDayAdmin(admin.ModelAdmin):
    list_display = ['routine_title', 'day']
    list_display_links = ['routine_title']

    def routine_title(self, obj):
        return obj.routine_id.title
