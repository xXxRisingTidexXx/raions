from typing import Dict, Any, Tuple
from re import compile
from core.decorators import nullable
from core.utils import find


class Geomapper:
    def map(self, location: Dict[str, Any]) -> Dict[str, Any]:
        """
        Performs JSON validation, then returns None if it failed and
        renovated dict otherwise.

        :param location: placement description (point, address, etc.)
        :return: None or location dictionary
        """
        return None if not self._check(location) else {
            'point': self._get_point(location),
            'state': self._get_state(location),
            'locality': self._get_locality(location),
            'county': self._get_county(location),
            'neighbourhood': self._get_neighbourhood(location),
            'road': self._get_road(location),
            'house_number': self._get_house_number(location)
        }

    def _check(self, location: Dict[str, Any]) -> bool:
        """
        Performs location's structure validating.

        :param location: geoposition's dictionary
        :return: whether location is valid or not
        """
        pass

    def _get_point(self, location: Dict[str, Any]) -> Tuple[float, float]:
        """
        Extracts 2D point from the "raw" JSON location

        :param location: geoposition's dictionary
        :return: 2D point in (longitude, latitude) format
        """
        pass

    def _get_state(self, location: Dict[str, Any]) -> str:
        """
        Extracts location's state (region, "oblast" or None in case of Kyiv)

        :param location: geoposition's dictionary
        :return: point's state
        """
        pass

    def _get_locality(self, location: Dict[str, Any]) -> str:
        """
        Extracts location's locality (city, town or village)

        :param location: geoposition's dictionary
        :return: point's locality
        """
        pass

    def _get_county(self, location: Dict[str, Any]) -> str:
        """
        Extracts location's county (district or "raion")

        :param location: geoposition's dictionary
        :return: point's administrative division unit
        """
        pass

    def _get_neighbourhood(self, location: Dict[str, Any]) -> str:
        """
        Extracts location's neighbourhood (suburb)

        :param location: geoposition's dictionary
        :return: point's historical area
        """
        pass

    def _get_road(self, location: Dict[str, Any]) -> str:
        """
        Extracts location's road (street, hwy, blw or ave)

        :param location: geoposition's dictionary
        :return: point's road
        """
        pass

    def _get_house_number(self, location: Dict[str, Any]) -> str:
        """
        Extracts location's house number

        :param location: geoposition's dictionary
        :return: point's house number
        """
        pass


class NominatimGeomapper(Geomapper):
    """
    'Cause *raions* concern Ukrainian real estate, all results of HTTP
    requests belongs to the Ukrainian territory.
    """
    _county_pattern = compile(r'([\w\-’\']+ район)\W*')

    def _check(self, location: Dict[str, Any]) -> bool:
        return location.get('address', {}).get('country') == 'Україна'

    def _get_point(self, location: Dict[str, Any]) -> Tuple[float, float]:
        return float(location['lon']), float(location['lat'])

    def _get_state(self, location: Dict[str, Any]) -> str:
        state = location['address'].get('state')
        if state is not None and len(state) <= 30:
            return state

    def _get_locality(self, location: Dict[str, Any]) -> str:
        address = location['address']
        return find(
            lambda l: not (
                l is None or l.endswith(' рада') or l.endswith(' район')
            ),
            (address.get('city'), address.get('town'), address.get('village'))
        )

    def _get_county(self, location: Dict[str, Any]) -> str:
        county = self._search_county(location['address'].get('county'))
        if county is not None:
            return county
        return self._search_county(location.get('display_name'))

    @nullable
    def _search_county(self, string: str) -> str:
        """
        Tries to extract location's county from the address string.

        :param string: a row which contains city, district, suburb, etc.
        :return: location's county
        """
        county = self._county_pattern.search(string).groups()[0]
        if county[0].isupper():
            return county

    def _get_neighbourhood(self, location: Dict[str, Any]) -> str:
        address = location['address']
        return address.get('neighbourhood', address.get('suburb'))

    def _get_road(self, location: Dict[str, Any]) -> str:
        address = location['address']
        return address.get('road', address.get('pedestrian'))

    def _get_house_number(self, location: Dict[str, Any]) -> str:
        house_number = location['address'].get('house_number')
        if house_number is not None and len(house_number) <= 20:
            return house_number
