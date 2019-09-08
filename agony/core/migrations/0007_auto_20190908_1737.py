from django.db import migrations
from core.utils import fix_typos


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20190908_1308'),
    ]

    operations = [
        migrations.RunPython(fix_typos)
    ]
