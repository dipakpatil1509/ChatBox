# Generated by Django 3.0.5 on 2020-05-11 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='owner',
            field=models.CharField(default='', max_length=256),
        ),
    ]
