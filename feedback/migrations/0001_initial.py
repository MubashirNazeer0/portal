# Generated by Django 5.1.3 on 2024-11-24 15:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('INF', 'Infrastructure'), ('GEN', 'Generic'), ('CUR', 'Curriculum')], default='GEN', max_length=3)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('text', models.CharField(max_length=400)),
                ('email', models.EmailField(max_length=254)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
    ]
