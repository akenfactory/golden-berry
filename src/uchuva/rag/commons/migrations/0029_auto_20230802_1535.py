# Generated by Django 3.2.9 on 2023-08-02 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0028_alter_conceptobserver_concept_properties'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='completion_tokens',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='history',
            name='prompt_tokens',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='history',
            name='total_tokens',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tmphistory',
            name='completion_tokens',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tmphistory',
            name='prompt_tokens',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tmphistory',
            name='total_tokens',
            field=models.IntegerField(default=0),
        ),
    ]