# Generated by Django 3.2.15 on 2022-09-12 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0010_auto_20220911_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='work_company',
            field=models.CharField(max_length=50, verbose_name='公司名称'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='work_position',
            field=models.CharField(max_length=50, verbose_name='工作职位'),
        ),
    ]
