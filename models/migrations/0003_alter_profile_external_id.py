# Generated by Django 3.2.7 on 2021-09-20 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0002_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='external_id',
            field=models.PositiveIntegerField(unique=True, verbose_name='User ID'),
        ),
    ]