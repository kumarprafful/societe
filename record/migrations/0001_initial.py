# Generated by Django 2.1.4 on 2018-12-31 18:25

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('starting_share', models.IntegerField()),
                ('starting_loan', models.IntegerField()),
                ('date_of_creation', models.DateTimeField(default=datetime.datetime.now)),
                ('month_of_creation', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='MonthlyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('month', models.IntegerField(blank=True, default=0, null=True)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('previous_share', models.IntegerField(blank=True, null=True)),
                ('previous_loan', models.IntegerField(blank=True, null=True)),
                ('share', models.IntegerField(blank=True, null=True)),
                ('total_share', models.IntegerField(blank=True, null=True)),
                ('installment', models.IntegerField(blank=True, null=True)),
                ('balance_loan', models.IntegerField(blank=True, null=True)),
                ('interest', models.IntegerField(blank=True, null=True)),
                ('late_fees', models.IntegerField(blank=True, default=0, null=True)),
                ('total_amount', models.IntegerField(blank=True, default=10, null=True)),
                ('remarks', models.CharField(blank=True, max_length=30, null=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='record.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Society',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('society_name', models.CharField(max_length=1024, unique=True)),
                ('president', models.CharField(max_length=1024)),
                ('address', models.CharField(max_length=1024)),
                ('date_of_creation', models.DateTimeField(default=datetime.datetime.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Society',
                'verbose_name_plural': 'Societies',
            },
        ),
        migrations.AddField(
            model_name='member',
            name='society',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='society', to='record.Society'),
        ),
    ]
