# Generated by Django 4.1.3 on 2022-12-18 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="ordersmodel",
            name="custom_address",
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
