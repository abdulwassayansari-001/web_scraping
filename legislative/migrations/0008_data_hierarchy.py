# Generated by Django 4.1.12 on 2024-01-25 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('legislative', '0007_hierarchy_title_remove_subcommittees_hierarchy_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='hierarchy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='legislative.hierarchy'),
        ),
    ]
