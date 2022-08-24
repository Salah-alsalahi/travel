# Generated by Django 4.0.6 on 2022-08-24 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('photo_main', models.ImageField(upload_to='photos/%Y/%m/%d/')),
                ('price', models.IntegerField()),
                ('listing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='listings.listing')),
            ],
        ),
    ]