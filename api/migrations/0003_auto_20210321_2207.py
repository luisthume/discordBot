# Generated by Django 3.1.7 on 2021-03-21 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210321_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hour',
            name='minutes',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
