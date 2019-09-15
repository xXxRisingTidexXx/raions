from django.db import migrations
from core.utils import localize_details


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_flat_is_visible'),
    ]

    operations = [
        migrations.RunPython(localize_details)
    ]
