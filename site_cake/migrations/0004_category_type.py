# Generated by Django 4.2.1 on 2023-06-08 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_cake', '0003_cookerpost'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Тип',
                'verbose_name_plural': 'Типы',
            },
        ),
    ]
