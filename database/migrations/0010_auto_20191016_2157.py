# Generated by Django 2.2.6 on 2019-10-16 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0009_auto_20191016_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perleav',
            name='Current_Balance',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='perleav',
            name='perleav_accrued',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='perleav',
            name='perleav_begin_balance',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='perleav',
            name='perleav_pidm',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='perleav',
            name='perleav_taken',
            field=models.IntegerField(default=0),
        ),
    ]
