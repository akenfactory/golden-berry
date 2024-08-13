# Generated by Django 3.2.9 on 2023-06-10 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0009_fee'),
    ]

    operations = [
        migrations.CreateModel(
            name='TmpHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('search', models.CharField(max_length=200)),
                ('result', models.CharField(max_length=1000)),
                ('area', models.IntegerField()),
                ('guest_ip', models.CharField(max_length=1000)),
                ('guest_attemps', models.IntegerField()),
            ],
        ),
    ]
