# Generated by Django 3.0.14 on 2023-02-20 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routine', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routine',
            name='category',
            field=models.CharField(choices=[('MIRACLE', 'MIRACLE(기상 관련)'), ('HOMEWORK', 'HOMEWORK(숙제 관련)')], max_length=10),
        ),
        migrations.AlterField(
            model_name='routineday',
            name='day',
            field=models.CharField(choices=[('MON', '월요일'), ('TUE', '화요일'), ('WED', '수요일'), ('THU', '목요일'), ('FRI', '금요일'), ('SAT', '토요일'), ('SUN', '일요일')], max_length=3),
        ),
        migrations.AlterField(
            model_name='routineresult',
            name='result',
            field=models.CharField(choices=[('NOT', 'NOT(안함)'), ('TRY', 'TRY(시도)'), ('DONE', 'DONE(완료)')], default='NOT', max_length=5),
        ),
    ]