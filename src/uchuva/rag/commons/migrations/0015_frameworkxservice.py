# Generated by Django 3.2.9 on 2023-07-05 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0014_service_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='FrameworkXService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField()),
                ('Framework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commons.framework')),
                ('Service', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='commons.service')),
            ],
        ),
    ]
