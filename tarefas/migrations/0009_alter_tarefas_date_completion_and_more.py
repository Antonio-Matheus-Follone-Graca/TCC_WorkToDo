# Generated by Django 4.1.1 on 2022-11-01 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tarefas', '0008_alter_tarefas_date_completion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarefas',
            name='date_completion',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tarefas',
            name='date_conclusao',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tarefas',
            name='date_start',
            field=models.DateTimeField(),
        ),
    ]
