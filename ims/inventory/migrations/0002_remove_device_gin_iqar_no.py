# Generated by Django 3.2.8 on 2021-12-30 05:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='gin_iqar_no',
        ),
    ]
