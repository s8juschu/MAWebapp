# Generated by Django 3.2 on 2022-01-21 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_auto_20220120_1611'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personaldata',
            name='session',
        ),
        migrations.RemoveField(
            model_name='personaldata',
            name='submission',
        ),
        migrations.AddField(
            model_name='questionnairesubmission',
            name='answer',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='age',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='finished',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='submission',
            name='gender',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='list_m1',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='list_m2',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='list_p1',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='list_p2',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='nationality',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='terms_agree',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='GeneralData',
        ),
        migrations.DeleteModel(
            name='PersonalData',
        ),
    ]
