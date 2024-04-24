# Generated by Django 5.0.3 on 2024-03-13 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin_student_mst',
            name='student_username',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='admin_teacher_mst',
            name='teacher_username',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
