# Generated by Django 3.2.9 on 2022-02-17 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_blog_logo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-updated', '-created']},
        ),
    ]