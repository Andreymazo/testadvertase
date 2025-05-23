# Generated by Django 5.2.1 on 2025-05-22 21:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=150, verbose_name="Ads's category")),
                ('title', models.CharField(max_length=150, verbose_name="Ads's title")),
                ('description', models.CharField(max_length=2000, verbose_name='Description')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media')),
                ('created', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(choices=[('STATUS_NEW', 'new'), ('STATUS_USED', 'used')], default='STATUS_USED')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
