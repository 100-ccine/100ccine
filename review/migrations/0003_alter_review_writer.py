# Generated by Django 3.2.7 on 2021-09-25 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_alter_review_writer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='writer',
            field=models.CharField(max_length=30, null=True, verbose_name='작성자'),
        ),
    ]