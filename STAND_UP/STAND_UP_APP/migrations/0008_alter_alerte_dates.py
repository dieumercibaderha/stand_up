# Generated by Django 5.1.1 on 2024-11-11 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('STAND_UP_APP', '0007_alter_user_dates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alerte',
            name='Dates',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
