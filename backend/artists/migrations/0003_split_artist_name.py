# Generated migration to split Artist name into first_name and last_name
from django.db import migrations, models


def split_names(apps, schema_editor):
    """Split existing artist names into first_name and last_name"""
    Artist = apps.get_model('artists', 'Artist')
    
    for artist in Artist.objects.all():
        if hasattr(artist, 'name') and artist.name:
            # Split name into parts
            name_parts = artist.name.strip().split(' ', 1)
            artist.first_name = name_parts[0]
            artist.last_name = name_parts[1] if len(name_parts) > 1 else ''
            artist.save(update_fields=['first_name', 'last_name'])


def merge_names(apps, schema_editor):
    """Reverse migration: merge first_name and last_name back into name"""
    Artist = apps.get_model('artists', 'Artist')
    
    for artist in Artist.objects.all():
        if hasattr(artist, 'first_name'):
            full_name = f"{artist.first_name} {artist.last_name}".strip() if artist.last_name else artist.first_name
            artist.name = full_name
            artist.save(update_fields=['name'])


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0002_album_track_artist_followers_artist_popularity_and_more'),
    ]

    operations = [
        # Step 1: Add new fields (nullable first)
        migrations.AddField(
            model_name='artist',
            name='first_name',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='last_name',
            field=models.CharField(max_length=100, blank=True, default=''),
        ),
        
        # Step 2: Migrate data from name to first_name/last_name
        migrations.RunPython(split_names, reverse_code=merge_names),
        
        # Step 3: Make first_name non-nullable now that data is migrated
        migrations.AlterField(
            model_name='artist',
            name='first_name',
            field=models.CharField(max_length=100),
        ),
        
        # Step 4: Remove the old name field
        migrations.RemoveField(
            model_name='artist',
            name='name',
        ),
        
        # Step 5: Update indexes
        migrations.AlterModelOptions(
            name='artist',
            options={'ordering': ['first_name', 'last_name']},
        ),
        
        # Step 6: Remove old index and add new ones
        migrations.RemoveIndex(
            model_name='artist',
            name='artists_art_name_68abb5_idx',
        ),
        migrations.AddIndex(
            model_name='artist',
            index=models.Index(fields=['first_name', 'last_name'], name='artists_art_first_n_72bf1f_idx'),
        ),
    ]
