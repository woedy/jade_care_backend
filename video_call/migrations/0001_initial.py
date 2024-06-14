# Generated by Django 3.2.7 on 2021-10-28 19:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('callee_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='callee_user', to=settings.AUTH_USER_MODEL)),
                ('caller_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='caller_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sdp', models.TextField(blank=True, null=True)),
                ('type', models.CharField(blank=True, max_length=1000, null=True)),
                ('room', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='offer', to='video_call.room')),
            ],
        ),
        migrations.CreateModel(
            name='CallerCandidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candidate', models.TextField(blank=True, null=True)),
                ('sdp_m_line_index', models.IntegerField(blank=True, null=True)),
                ('sdp_mid', models.CharField(blank=True, max_length=1000, null=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='caller_candidates', to='video_call.room')),
            ],
        ),
        migrations.CreateModel(
            name='CalleeCandidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candidate', models.TextField(blank=True, null=True)),
                ('sdp_m_line_index', models.IntegerField(blank=True, null=True)),
                ('sdp_mid', models.CharField(blank=True, max_length=1000, null=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='callee_candidates', to='video_call.room')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sdp', models.TextField(blank=True, null=True)),
                ('type', models.CharField(blank=True, max_length=1000, null=True)),
                ('room', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='video_call.room')),
            ],
        ),
    ]
