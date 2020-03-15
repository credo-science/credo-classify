# Generated by Django 3.0.4 on 2020-03-15 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, default='', verbose_name='Description')),
                ('active', models.BooleanField(default=False, verbose_name='Active')),
                ('kind', models.CharField(choices=[('b', 'Build-in'), ('c', 'Classification by user'), ('cs', 'Scaled classification (1 to 5)'), ('co', 'One class'), ('o', 'Others')], default='o', max_length=2, verbose_name='Kind')),
            ],
            options={
                'verbose_name': 'Attribute',
                'verbose_name_plural': 'Attributes',
                'ordering': ['name'],
                'default_permissions': ('view', 'add', 'change', 'delete'),
            },
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='')),
                ('evaluation', models.CharField(default='x', max_length=255)),
            ],
            options={
                'default_permissions': ('view', 'add', 'change', 'delete'),
            },
        ),
    ]
