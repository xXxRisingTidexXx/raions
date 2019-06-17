from django.db.utils import IntegrityError
from django.db.transaction import atomic
from agony.settings import BASE_DIR
from os.path import join, dirname
from pathlib import Path
from json import loads


# noinspection PyUnusedLocal,PyPep8Naming
def load_details(apps, schema_editor):
    Detail = apps.get_model('core', 'Detail')
    with open(join(BASE_DIR, 'resources/details.json')) as stream:
        details = loads(stream.read())
    for detail in details:
        for value in detail['values']:
            try:
                with atomic():
                    Detail.objects.create(
                        feature=detail['feature'],
                        value=value,
                        group=detail['group']
                    )
            except IntegrityError:
                pass
