# Generated by Django 4.1.1 on 2022-11-01 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tarefas', '0005_alter_tarefas_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarefas',
            name='date_conclusao',
            field=models.DateField(blank=True, null=True),
        ),
    ]
