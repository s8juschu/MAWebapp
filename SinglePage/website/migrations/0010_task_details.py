# Generated by Django 3.2 on 2022-01-19 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_rename_answer_answerchoice_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='details',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
