# Generated by Django 3.0.2 on 2020-01-05 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0007_auto_20200104_2331'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='file',
            field=models.FileField(null=True, upload_to='sources/'),
        ),
    ]