# Generated by Django 3.0.5 on 2020-04-19 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0003_remove_host_last_accessed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='host',
            name='original_ip',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='threat',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]