# Generated by Django 3.2 on 2022-03-09 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0024_auto_20220216_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='request_delete',
            field=models.BooleanField(default=False),
        ),
    ]