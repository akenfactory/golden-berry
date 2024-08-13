# Generated by Django 3.2.9 on 2023-07-05 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0010_tmphistory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='price',
        ),
        migrations.AddField(
            model_name='fee',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
