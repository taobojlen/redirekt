# Generated by Django 3.0.5 on 2020-05-06 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("links", "0003_auto_20200506_1621"),
    ]

    operations = [
        migrations.AlterField(
            model_name="visit",
            name="country",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="visit", name="ip", field=models.CharField(max_length=255),
        ),
    ]
