# Generated by Django 3.2.9 on 2023-08-02 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0029_auto_20230802_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='conceptobserver',
            name='title',
            field=models.CharField(default='', max_length=100),
        ),
    ]
