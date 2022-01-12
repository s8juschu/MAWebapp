# Generated by Django 3.2 on 2022-01-12 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_alter_task_image_link'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='question_text',
            new_name='text',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='task_text',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='taskset',
            name='description',
        ),
        migrations.AddField(
            model_name='task',
            name='text',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]