# Generated by Django 3.2.9 on 2023-07-06 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0020_auto_20230705_2222'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicestatus',
            name='Service',
        ),
        migrations.AddField(
            model_name='servicestatus',
            name='ProfileServices',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='commons.profileservices'),
        ),
        migrations.AlterField(
            model_name='servicestatus',
            name='Domain',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='commons.domain'),
        ),
    ]
