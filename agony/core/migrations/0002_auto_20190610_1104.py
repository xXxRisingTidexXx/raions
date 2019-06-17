from django.db import migrations
from core.utils import load_details


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_details),
    ]
