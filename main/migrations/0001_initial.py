# Generated by Django 2.1.7 on 2019-04-24 03:01

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CoachPhoto',
            fields=[
                ('code', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'coach_photos',
            },
        ),
        migrations.CreateModel(
            name='CoachPost',
            fields=[
                ('code', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('title', models.TextField()),
                ('content', django.contrib.postgres.fields.jsonb.JSONField()),
                ('is_public', models.BooleanField(default=False)),
                ('tags', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'coach_posts',
            },
        ),
        migrations.CreateModel(
            name='CoachProfile',
            fields=[
                ('code', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', django.contrib.postgres.fields.jsonb.JSONField()),
                ('is_public', models.BooleanField(default=False)),
                ('photos', models.ManyToManyField(to='main.CoachPhoto')),
            ],
            options={
                'db_table': 'coach_profiles',
            },
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('code', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField()),
            ],
            options={
                'db_table': 'sports',
            },
        ),
        migrations.AddField(
            model_name='coachprofile',
            name='sports',
            field=models.ManyToManyField(to='main.Sport'),
        ),
        migrations.AddField(
            model_name='coachprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
