# Generated by Django 3.2.15 on 2022-10-13 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0015_courses_is_carousel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carouselbanner',
            name='index',
            field=models.IntegerField(default=0, verbose_name='顺序'),
        ),
    ]
