# Generated by Django 3.2 on 2022-02-16 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0023_submission_framing'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnairesubmission',
            name='name',
            field=models.CharField(default='IMI', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='questionnairesubmission',
            name='question_id',
            field=models.IntegerField(null=True),
        ),
    ]
