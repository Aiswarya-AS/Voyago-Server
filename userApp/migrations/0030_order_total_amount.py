# Generated by Django 4.2 on 2023-05-01 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0029_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_amount',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
