# Generated by Django 5.1.2 on 2024-10-29 17:53

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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('INF', 'Infrastructure'), ('GEN', 'Generic'), ('CUR', 'Curriculum')], default='GEN', max_length=3)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('text', models.CharField(max_length=400)),
                ('email', models.EmailField(max_length=254)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
    ]
