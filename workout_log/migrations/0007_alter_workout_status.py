# Generated by Django 5.0.2 on 2024-03-07 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout_log', '0006_alter_workoutexercisedetail_reps_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='status',
            field=models.CharField(choices=[('Started', 'Started'), ('Finished', 'Finished'), ('Template', 'Template')], default='Template', max_length=16),
        ),
    ]
