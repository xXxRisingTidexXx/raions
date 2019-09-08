from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20190701_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='flat',
            name='is_visible',
            field=models.BooleanField(default=True),
        ),
    ]
