from django.db import models

from danbi_problem import settings


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class MEta:
        abstract = True

class Routine(TimestampedModel):
    CATEGORY_CHOICE = (
        ('MIRACLE', 'MIRACLE(기상 관련)'),
        ('HOMEWORK', 'HOMEWORK(숙제 관련)'),
    )
    routine_id = models.AutoField(primary_key=True)
    account_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='routine_set', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICE)
    goal = models.CharField(max_length=500)
    is_alarm = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class RoutineResult(TimestampedModel):
    RESULT_CHOICE = (
        ('NOT', 'NOT(안함)'),
        ('TRY', 'TRY(시도)'),
        ('DONE', 'DONE(완료)'),
    )
    routine_result_id = models.AutoField(primary_key=True)
    routine_id = models.ForeignKey(Routine, related_name='routine_result_set', on_delete=models.CASCADE)
    result = models.CharField(max_length=5, choices=RESULT_CHOICE, default='NOT')
    is_deleted = models.BooleanField(default=False)

class RoutineDay(TimestampedModel):
    DAYS = (
        ('MON', '월요일'),
        ('TUE', '화요일'),
        ('WED', '수요일'),
        ('THU', '목요일'),
        ('FRI', '금요일'),
        ('SAT', '토요일'),
        ('SUN', '일요일'),
    )
    day = models.CharField(max_length=3, choices=DAYS)
    routine_id = models.ForeignKey(Routine, related_name='routine_day_set', on_delete=models.CASCADE)
