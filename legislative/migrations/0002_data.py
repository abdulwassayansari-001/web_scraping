# Generated by Django 4.1.12 on 2024-01-23 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('legislative', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('committee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='legislative.committees')),
                ('member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='legislative.members')),
                ('subcommittee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='legislative.subcommittees')),
            ],
        ),
    ]
