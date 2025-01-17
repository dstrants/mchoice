# Generated by Django 3.0.2 on 2020-01-04 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0005_aswer_attempt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attempt',
            name='correct',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='attempt',
            name='ended_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='attempt',
            name='started_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
