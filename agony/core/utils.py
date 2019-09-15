from typing import Any
from django.apps.registry import Apps
from django.db.utils import IntegrityError
from django.db.transaction import atomic
from agony.settings import BASE_DIR
from os.path import join
from json import loads


def load_details(apps: Apps, schema_editor: Any):  # noqa
    """
    Loads a predefined set of details into the DB.

    :param apps: a set of django apps
    :param schema_editor: DB schema mutator
    """
    Detail = apps.get_model('core', 'Detail')  # noqa
    with open(join(BASE_DIR, 'core/resources/details.json')) as stream:
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


def localize_details(apps: Apps, schema_editor: Any):  # noqa
    """
    Translates all existing details into Ukrainian.

    :param apps: a set of django apps
    :param schema_editor: DB schema mutator
    """
    Detail = apps.get_model('core', 'Detail')  # noqa
    with open(join(BASE_DIR, 'core/resources/translations.json')) as stream:
        translations = loads(stream.read())
    for en, uk in translations.items():
        try:
            with atomic():
                detail = Detail.objects.get(value=en)
                detail.value = uk
                detail.save()
        except (IntegrityError, Detail.DoesNotExist):
            pass


def fix_typos(apps: Apps, schema_editor: Any):  # noqa
    """
    Fixes all details' typos.

    :param apps: a set of django apps
    :param schema_editor: DB schema mutator
    """
    Detail = apps.get_model('core', 'Detail')  # noqa
    try:
        with atomic():
            detail = Detail.objects.get(value='Ксометичний ремонт')
            detail.value = 'Косметичний ремонт'
            detail.save()
    except (IntegrityError, Detail.DoesNotExist):
        pass
