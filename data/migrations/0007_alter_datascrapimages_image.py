# Generated by Django 3.2.5 on 2023-10-09 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_auto_20231006_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datascrapimages',
            name='image',
            field=models.ImageField(max_length=255, upload_to='images/'),
        ),
    ]