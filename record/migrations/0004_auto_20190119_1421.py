# Generated by Django 2.1.4 on 2019-01-19 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0003_monthlyrecord_installment_filled'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='address',
            field=models.CharField(default='new delhi', max_length=1024),
        ),
        migrations.AddField(
            model_name='member',
            name='mobile_no',
            field=models.IntegerField(default=0),
        ),
    ]
