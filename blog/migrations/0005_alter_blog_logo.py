# Generated by Django 3.2.9 on 2022-03-15 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_blog_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
