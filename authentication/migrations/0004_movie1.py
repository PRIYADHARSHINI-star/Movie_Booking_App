# Generated by Django 4.1.5 on 2023-09-03 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_movie_release_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Movie_Name', models.CharField(max_length=500, verbose_name='Movie_Name')),
                ('Theatre_Name', models.CharField(max_length=200, verbose_name='Theatre_Name')),
                ('Theatre_Location', models.CharField(max_length=200, verbose_name='Theatre_Location')),
                ('Release_Date', models.DateField(auto_now=True, help_text='Format: YYYY-MM-DD', verbose_name='Release_Date')),
            ],
        ),
    ]
