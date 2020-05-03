# Generated by Django 3.0.5 on 2020-05-03 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=255)),
                ('short_id', models.CharField(max_length=6, unique=True)),
                ('destination', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user_agent', models.CharField(max_length=4000)),
                ('ip', models.CharField(max_length=45)),
                ('is_bot', models.BooleanField(default=False)),
                ('fingerprint', models.CharField(max_length=40)),
                ('city', models.CharField(max_length=255, null=True)),
                ('country', models.CharField(max_length=2, null=True)),
                ('hostname', models.CharField(max_length=255, null=True)),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='links.Link')),
            ],
        ),
        migrations.AddIndex(
            model_name='visit',
            index=models.Index(fields=['fingerprint'], name='links_visit_fingerp_12c438_idx'),
        ),
    ]
