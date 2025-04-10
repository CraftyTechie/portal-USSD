# Generated by Django 5.1.7 on 2025-04-09 09:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academic', '0004_link_transcripts_to_students'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specialexam',
            name='result_session',
        ),
        migrations.RemoveField(
            model_name='supplementaryexam',
            name='result_session',
        ),
        migrations.AddField(
            model_name='specialexam',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Academic.student'),
        ),
        migrations.AddField(
            model_name='supplementaryexam',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Academic.student'),
        ),
    ]
