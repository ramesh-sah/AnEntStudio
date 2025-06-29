# Generated by Django 5.1.1 on 2024-09-27 11:42

import ckeditor.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Add',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='addimage/')),
            ],
            options={
                'verbose_name': 'Add',
                'verbose_name_plural': 'Adds',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='albumimage/')),
                ('title', models.CharField(max_length=200)),
                ('company_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='genreimage/')),
            ],
            options={
                'verbose_name': 'genre',
                'verbose_name_plural': 'genres',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='OrganizationSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization_name', models.CharField(max_length=150)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='companylogo/')),
                ('address', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=200)),
                ('phone_no', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PrivacyAndPolicy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('privacy', ckeditor.fields.RichTextField()),
            ],
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='sliderimage/')),
            ],
            options={
                'verbose_name': 'Slider',
                'verbose_name_plural': 'Sliders',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='TermsAndCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('terms', ckeditor.fields.RichTextField()),
            ],
        ),
        migrations.CreateModel(
            name='VideoCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='VideoMenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('video', models.URLField(max_length=500)),
                ('thubnail_image', models.ImageField(upload_to='thubnail_image')),
            ],
        ),
        migrations.CreateModel(
            name='AlbumImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='albumimage/')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='album', to='api.album')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='eventimage/')),
                ('another_image', models.ImageField(blank=True, null=True, upload_to='eventimage/')),
                ('event_date', models.DateTimeField(blank=True, null=True)),
                ('week_day', models.IntegerField(choices=[(0, 'Sunday'), (1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday')])),
                ('participate_start_time', models.DateTimeField(blank=True, null=True)),
                ('participate_end_time', models.DateTimeField(blank=True, null=True)),
                ('participate_status', models.BooleanField(default=False)),
                ('voting_start_time', models.DateTimeField(blank=True, null=True)),
                ('voting_end_time', models.DateTimeField(blank=True, null=True)),
                ('voting_status', models.BooleanField(default=False)),
                ('location', models.CharField(max_length=200)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('description', models.TextField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_category', to='api.category')),
                ('participants', models.ManyToManyField(blank=True, related_name='events', to=settings.AUTH_USER_MODEL)),
                ('genre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_genre', to='api.genre')),
            ],
            options={
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='EventVotingSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voting_list', models.JSONField()),
                ('max_vote', models.IntegerField()),
                ('min_vote', models.IntegerField()),
                ('price_per_vote', models.DecimalField(decimal_places=2, max_digits=10)),
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='voting_settings', to='api.event')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='userimage/')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserEventVoting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voting_id', models.IntegerField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_event_votes', to='api.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_votes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('video', models.URLField(max_length=500)),
                ('thubnail_image', models.ImageField(upload_to='thubnail_image')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_category', to='api.videocategory')),
            ],
        ),
    ]
