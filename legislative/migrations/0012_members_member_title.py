# Generated by Django 4.1.12 on 2024-02-07 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legislative', '0011_alter_data_committee_alter_data_hierarchy_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='members',
            name='member_title',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]