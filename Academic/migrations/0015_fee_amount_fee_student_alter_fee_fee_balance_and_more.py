# Generated by Django 5.1.7 on 2025-04-15 12:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academic', '0014_clearancerequest_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='fee',
            name='amount',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fee',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Academic.student'),
        ),
        migrations.AlterField(
            model_name='fee',
            name='fee_balance',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='fee',
            name='fee_statement',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='fee',
            name='fee_structure',
            field=models.FloatField(blank=True),
        ),
        migrations.CreateModel(
            name='MpesaIDs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchantRequestID', models.CharField(max_length=50)),
                ('checkoutRequestID', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Academic.student')),
            ],
        ),
    ]
