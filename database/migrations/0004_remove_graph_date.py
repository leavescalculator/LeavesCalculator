# Generated by Django 2.2.7 on 2019-11-19 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_auto_20191119_0313'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='graph',
            name='date',
        ),
    ]
