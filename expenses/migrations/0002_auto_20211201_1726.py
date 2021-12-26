# Generated by Django 3.2.9 on 2021-12-01 17:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expenses',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='expenses',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='expenses',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
