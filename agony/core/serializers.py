from rest_framework.serializers import ModelSerializer
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from core.models import User, Flat, Geolocation, Detail


class GeolocationSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Geolocation
        geo_field = 'point'
        fields = (
            'state', 'locality', 'county', 'neighbourhood',
            'road', 'house_number', 'point'
        )


class DetailSerializer(ModelSerializer):
    class Meta:
        model = Detail
        fields = ('feature', 'value', 'group')


class FlatSerializer(ModelSerializer):
    geolocation = GeolocationSerializer(read_only=True)
    details = DetailSerializer(many=True, read_only=True)

    class Meta:
        model = Flat
        fields = (
            'id', 'url', 'avatar', 'geolocation', 'price', 'rate', 'area',
            'living_area', 'kitchen_area', 'rooms', 'floor', 'total_floor',
            'ceiling_height', 'details'
        )


class SavedSerializer(ModelSerializer):
    saved_flats = FlatSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('saved_flats',)
