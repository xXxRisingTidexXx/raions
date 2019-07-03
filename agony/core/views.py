from functools import reduce
from django.db.models import Q
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework_jwt.views import ObtainJSONWebToken
from .parsers import JSONParser
from .models import Geolocation, Flat, Detail
from .serializers import SavedSerializer, FlatSerializer


class TemplateView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (TemplateHTMLRenderer,)

    @staticmethod
    def get(request):
        return Response()


class IndexView(TemplateView):
    template_name = 'index.html'


class SummaryView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def get(request):
        return Response({'total_flats': Flat.objects.count()})


class LoginView(TemplateView):
    template_name = 'login.html'


class AuthenticationView(ObtainJSONWebToken):
    parser_classes = (JSONParser,)


class ProfileView(TemplateView):
    template_name = 'profile.html'


class SavedView(APIView):
    _serializer_class = SavedSerializer
    _kinds = {'flats': Flat}

    def get(self, request):
        return Response(self._serializer_class(request.user).data)

    def patch(self, request, kind, pk):
        return self.__modify(request, kind, pk, 'add')

    def __modify(self, request, kind, pk, action):
        status = HTTP_200_OK
        try:
            model = self._kinds[kind]
            getattr(
                getattr(request.user, model.saved_field), action
            )(model.objects.get(id=pk))
        except (KeyError, Flat.DoesNotExist):
            status = HTTP_404_NOT_FOUND
        return Response(status=status)

    def delete(self, request, kind, pk):
        return self.__modify(request, kind, pk, 'remove')


class MapReduceView(APIView):
    def _reduce_query(self, *args):
        return reduce(lambda q1, q2: q1 & q2, self._map_queries(*args), Q())

    def _map_queries(self, *args) -> list:
        pass


class AutocompleteView(MapReduceView):
    def get(self, request):
        if request.query_params is None:
            return Response(status=HTTP_400_BAD_REQUEST)
        return Response(self._get_completions(request.query_params))

    def _get_completions(self, data):
        pass

    def _map_queries(self, *args):
        return (Q(**{f'{i[0]}__istartswith': i[1]}) for i in args[0].items())


class GeolocationAutocompleteView(AutocompleteView):
    def _get_completions(self, data):
        return list(Geolocation.objects.filter(
            self._reduce_query(data)
        ).distinct().values(
            'state', 'locality', 'county'
        ))


class DetailAutocompleteView(AutocompleteView):
    def _get_completions(self, data):
        return list(
            v[0] for v in Detail.objects.filter(
                self._reduce_query(data)
            ).values_list('value')
        )


class LookupView(MapReduceView):
    parser_classes = (JSONParser,)
    _bundles = {'flats': (Flat, FlatSerializer)}
    _chunk_size = 20

    def post(self, request, kind):
        bundle = self._bundles.get(kind)
        if bundle is None:
            return Response(status=HTTP_404_NOT_FOUND)
        return Response(bundle[1](
            self.__get_models(request.data, bundle[0]), many=True
        ).data)

    def __get_models(self, data, model):
        field, number = data.get('order_by'), int(data.get('number', 0))
        return reduce(
            lambda qs, d: qs.filter(details__value=d),
            data.get('details', []),
            model.objects.filter(self._reduce_query(data, model.lookups))
        ).order_by(field if field in model.order_by else '-published')[
            self._chunk_size * number:self._chunk_size * (number + 1)
        ]

    def _map_queries(self, *args):
        return (
            Q(**{args[1][i[0]]: i[1]})
            for i in args[0].items() if i[0] in args[1]
        )
