# Generated by Django 3.2.5 on 2021-07-26 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20210725_0641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='is_draft',
            field=models.BooleanField(default=True),
        ),
    ]
