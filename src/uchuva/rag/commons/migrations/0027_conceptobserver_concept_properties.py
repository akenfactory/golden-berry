# Generated by Django 3.2.9 on 2023-08-02 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0026_auto_20230801_2130'),
    ]

    operations = [
        migrations.AddField(
            model_name='conceptobserver',
            name='concept_properties',
            field=models.CharField(default='', max_length=30),
        ),
    ]