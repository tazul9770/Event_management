# Generated by Django 5.1.5 on 2025-02-02 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_remove_participant_events_event_participants'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='participants',
        ),
        migrations.AddField(
            model_name='participant',
            name='events',
            field=models.ManyToManyField(related_name='participants', to='events.event'),
        ),
    ]
