# Generated by Django 3.2.9 on 2021-11-29 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20211129_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(db_index=True, max_length=255),
        ),
    ]