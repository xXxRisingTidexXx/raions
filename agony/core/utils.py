from django.db.utils import IntegrityError
from django.db.transaction import atomic
from agony.settings import BASE_DIR
from os.path import join, dirname
from pathlib import Path
from json import loads

DETAILS_PATHS = (
    'reapy/resources/olx/flat/values.json',
    'reapy/resources/dom_ria/flat/values.json'
)


# noinspection PyUnusedLocal,PyPep8Naming
def load_details(apps, schema_editor):
    Detail = apps.get_model('core', 'Detail')
    for details_path in DETAILS_PATHS:
        for feature_values in __json(details_path).items():
            for value in feature_values[1]['values'].values():
                try:
                    with atomic():
                        Detail.objects.create(
                            feature=feature_values[0],
                            value=value,
                            group=feature_values[1]['group']
                        )
                except IntegrityError:
                    pass


def __json(path):
    abspath = Path(join(dirname(BASE_DIR), path))
    if abspath.is_file():
        with open(abspath) as stream:
            return loads(stream.read())
    return {}
