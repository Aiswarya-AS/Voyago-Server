# Generated by Django 4.2 on 2023-05-11 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0037_remove_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='journey_status',
            field=models.CharField(default='pending', max_length=200),
        ),
    ]