# Generated by Django 5.0 on 2023-12-20 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0006_alter_spotifytoken_access_token_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpotifyToken1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('refresh_token', models.CharField(max_length=150, null=True)),
                ('access_token', models.CharField(max_length=150, null=True)),
                ('expires_in', models.DateTimeField(null=True)),
                ('token_type', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='spotifytoken',
            name='access_token',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='spotifytoken',
            name='expires_in',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='spotifytoken',
            name='refresh_token',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='spotifytoken',
            name='token_type',
            field=models.CharField(max_length=50),
        ),
    ]
