# Generated by Django 3.2.15 on 2022-10-11 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_auto_20221011_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='knowledge',
            field=models.CharField(default='', max_length=300, null=True, verbose_name='课程知识点'),
        ),
        migrations.AlterField(
            model_name='courses',
            name='notice',
            field=models.CharField(default='', max_length=300, null=True, verbose_name='课程须知'),
        ),
    ]
