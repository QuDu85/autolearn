# Generated by Django 3.2.8 on 2022-01-11 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_language_level_material_topic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='material',
            name='category',
        ),
        migrations.AddField(
            model_name='material',
            name='skill',
            field=models.ManyToManyField(to='api.Skill'),
        ),
    ]