from typing import Optional, Any
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.gis.db.models import (
    EmailField, BooleanField, Model, DateField, URLField, CharField, FloatField,
    DecimalField, ManyToManyField, SmallIntegerField, ForeignKey, CASCADE,
    UniqueConstraint, PointField
)


class Geolocation(Model):
    state = CharField(max_length=30, null=True)
    locality = CharField(max_length=40, null=True)
    county = CharField(max_length=40, null=True)
    neighbourhood = CharField(max_length=90, null=True)
    road = CharField(max_length=80, null=True)
    house_number = CharField(max_length=20, null=True)
    point = PointField(unique=True)

    class Meta:
        db_table = 'geolocations'

    def __str__(self) -> str:
        return f'{self.state}, {self.locality}, {self.county}'


class Detail(Model):
    feature = CharField(max_length=30)
    value = CharField(max_length=60, unique=True)
    group = CharField(max_length=20)

    class Meta:
        db_table = 'details'


class Estate(Model):
    url = URLField(max_length=400, unique=True)
    avatar = URLField(max_length=400, null=True)
    published = DateField()
    geolocation = ForeignKey(Geolocation, on_delete=CASCADE)
    price = DecimalField(max_digits=10, decimal_places=2)
    rate = DecimalField(max_digits=10, decimal_places=2)
    area = FloatField()
    is_visible = BooleanField(default=True)
    lookups = {}
    order_by = set()

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f'[{self.url}, {self.area}, {self.rate}]'


class Flat(Estate):
    living_area = FloatField(null=True)
    kitchen_area = FloatField(null=True)
    rooms = SmallIntegerField()
    floor = SmallIntegerField()
    total_floor = SmallIntegerField()
    ceiling_height = FloatField(null=True)
    details = ManyToManyField(Detail, db_table='flats_details')
    saved_field = 'saved_flats'
    lookups = {
        'state': 'geolocation__state',
        'locality': 'geolocation__locality',
        'county': 'geolocation__county',
        'neighbourhood': 'geolocation__neighbourhood',
        'road': 'geolocation__road',
        'house_number': 'geolocation__house_number',
        'area_from': 'area__gte',
        'area_to': 'area__lte',
        'living_area_from': 'living_area__gte',
        'living_area_to': 'living_area__lte',
        'kitchen_area_from': 'kitchen_area__gte',
        'kitchen_area_to': 'kitchen_area__lte',
        'rooms_from': 'rooms__gte',
        'rooms_to': 'rooms__lte',
        'floor_from': 'floor__gte',
        'floor_to': 'floor__lte',
        'total_floor_from': 'total_floor__gte',
        'total_floor_to': 'total_floor__lte',
        'ceiling_height_from': 'ceiling_height__gte',
        'ceiling_height_to': 'ceiling_height__lte'
    }
    order_by = {'area', '-area', 'rooms', '-rooms', 'price', '-price'}

    class Meta:
        db_table = 'flats'
        constraints = [
            UniqueConstraint(
                fields=['geolocation_id', 'rooms', 'floor', 'total_floor'],
                name='flat_geolocation_id_rooms_floor_total_floor_key'
            )
        ]


class UserManager(BaseUserManager):
    def create_user(self, email: Optional[str], password: str) -> 'User':
        if email is None:
            raise TypeError('An email address should be provided.')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str) -> 'User':
        user = self.model(email=self.normalize_email(email), is_staff=True)
        user.set_password(password)
        user.is_superuser = True
        user.save()
        return user


# noinspection PyUnusedLocal
class User(AbstractBaseUser):
    email = EmailField(db_index=True, unique=True)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    saved_flats = ManyToManyField(Flat)
    objects = UserManager()
    USERNAME_FIELD = 'email'

    @staticmethod
    def has_perm(perm: Any, obj: Any = None) -> bool:
        return True

    @staticmethod
    def has_module_perms(app_label: Any) -> bool:
        return True

    def __str__(self) -> str:
        return self.email
