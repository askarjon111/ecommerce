# Generated by Django 3.2.6 on 2021-08-28 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20210828_0703'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]