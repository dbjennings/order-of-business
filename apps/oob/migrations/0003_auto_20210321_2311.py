# Generated by Django 3.1.7 on 2021-03-22 04:11

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('oob', '0002_task_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='body',
            field=models.TextField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='completed_on',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='modified_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='task',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.coreuser'),
        ),
    ]