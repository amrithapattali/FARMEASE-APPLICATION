# Generated by Django 5.0.3 on 2024-03-07 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmease_app', '0008_plantimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlantHealthResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_healthy', models.BooleanField()),
                ('name', models.CharField(max_length=255)),
                ('probability', models.FloatField()),
                ('description', models.TextField()),
                ('treatment', models.TextField()),
            ],
        ),
    ]
