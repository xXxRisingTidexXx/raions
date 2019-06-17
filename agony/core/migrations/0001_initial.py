import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.CharField(max_length=30)),
                ('value', models.CharField(max_length=60)),
                ('group', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'details',
            },
        ),
        migrations.CreateModel(
            name='Geolocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=30, null=True)),
                ('locality', models.CharField(max_length=40, null=True)),
                ('county', models.CharField(max_length=40, null=True)),
                ('neighbourhood', models.CharField(max_length=90, null=True)),
                ('road', models.CharField(max_length=80, null=True)),
                ('house_number', models.CharField(max_length=20, null=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326, unique=True)),
            ],
            options={
                'db_table': 'geolocations',
            },
        ),
        migrations.CreateModel(
            name='Flat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=400, unique=True)),
                ('avatar', models.URLField(max_length=400, null=True)),
                ('published', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('area', models.FloatField()),
                ('living_area', models.FloatField(null=True)),
                ('kitchen_area', models.FloatField(null=True)),
                ('rooms', models.SmallIntegerField()),
                ('floor', models.SmallIntegerField()),
                ('total_floor', models.SmallIntegerField()),
                ('ceiling_height', models.FloatField(null=True)),
                ('details', models.ManyToManyField(db_table='flats_details', to='core.Detail')),
                ('geolocation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Geolocation')),
            ],
            options={
                'db_table': 'flats',
                'ordering': ['-published'],
            },
        ),
        migrations.AddConstraint(
            model_name='detail',
            constraint=models.UniqueConstraint(fields=('feature', 'value'), name='detail_feature_value_key'),
        ),
        migrations.AddField(
            model_name='user',
            name='saved_flats',
            field=models.ManyToManyField(to='core.Flat'),
        ),
        migrations.AddConstraint(
            model_name='flat',
            constraint=models.UniqueConstraint(fields=('geolocation_id', 'rooms', 'floor', 'total_floor'), name='flat_geolocation_id_rooms_floor_total_floor_key'),
        ),
    ]
