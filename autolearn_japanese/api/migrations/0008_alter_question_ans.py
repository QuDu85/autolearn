# Generated by Django 3.2.8 on 2022-01-19 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20220119_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='ans',
            field=models.CharField(choices=[('A', models.CharField(max_length=200, null=True)), ('B', models.CharField(max_length=200, null=True)), ('C', models.CharField(max_length=200, null=True)), ('D', models.CharField(max_length=200, null=True))], default='A', max_length=1),
        ),
    ]
