# Generated by Django 5.1.4 on 2024-12-16 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.ImageField(upload_to='jobposters/'),
        ),
    ]