# Generated by Django 4.2 on 2023-04-23 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0022_request_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='location',
            field=models.CharField(max_length=2100),
        ),
    ]