# Generated by Django 3.2 on 2022-01-21 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0018_auto_20220121_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='study',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='website.study'),
            preserve_default=False,
        ),
    ]
