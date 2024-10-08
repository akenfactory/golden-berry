# Generated by Django 3.2.9 on 2023-06-10 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0007_history'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consumption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_count', models.IntegerField(default=0)),
                ('Domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commons.domain')),
                ('Service', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='commons.service')),
            ],
        ),
    ]
