# Generated by Django 4.2.16 on 2024-12-08 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumni',
            name='cv',
            field=models.FileField(blank=True, null=True, upload_to='alumni_cvs/'),
        ),
        migrations.AddField(
            model_name='student',
            name='cv',
            field=models.FileField(blank=True, null=True, upload_to='student_cvs/'),
        ),
    ]
