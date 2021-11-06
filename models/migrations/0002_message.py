# Generated by Django 3.2.7 on 2021-09-19 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Text')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Receiving time')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='models.profile', verbose_name='Profile')),
            ],
            options={
                'verbose_name': 'Message',
            },
        ),
    ]
