# Generated by Django 3.2.9 on 2023-07-05 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0016_auto_20230705_1936'),
    ]

    operations = [
        migrations.AddField(
            model_name='planxservice',
            name='description',
            field=models.CharField(default='', max_length=200),
        ),
    ]
