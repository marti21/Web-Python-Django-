# Generated by Django 3.2.5 on 2022-03-12 16:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pangolin', '0003_remove_userpangolin_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpangolin',
            name='my_date_field',
            field=models.DateField(default=datetime.date(2022, 3, 12), verbose_name='birth'),
        ),
    ]
