# Generated by Django 4.2.5 on 2024-03-30 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0003_appointment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.CharField(max_length=100),
        ),
    ]