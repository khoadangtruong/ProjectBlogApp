# Generated by Django 3.2.9 on 2022-02-16 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='logo',
            field=models.ImageField(blank=True, default='default-img.jpg', null=True, upload_to=''),
        ),
    ]