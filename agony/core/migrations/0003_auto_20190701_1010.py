from django.db import migrations
from core.utils import load_details


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190618_0016'),
    ]

    operations = [
        migrations.RunPython(load_details),
    ]
