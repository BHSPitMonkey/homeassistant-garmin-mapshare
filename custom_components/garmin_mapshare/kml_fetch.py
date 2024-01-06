import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers.httpx_client import get_async_client
import defusedxml.ElementTree as ET

from .const import BASE_URL, MOCK_LINK_NAME

_LOGGER = logging.getLogger(__name__)
MOCK_VALUES = {
    "100110011001100": {
        "Id": 123456789,
        "Time UTC": "8/26/2023 8:58:45 PM",
        "Time": "8/26/2023 1:58:45 PM",
        "Name": "John Muir",
        "Map Display Name": "John Muir",
        "Device Type": "inReach Mini",
        "IMEI": "100110011001100",
        "Latitude": "48.468750",
        "Longitude": "-121.059358",
        "Elevation": "1628.12 m from MSL",
        "Velocity": "6.0 km/h",
        "Course": "22.50 ° True",
        "Valid GPS Fix": "True",
        "In Emergency": "False",
        "Event": "Tracking message received.",
        "SpatialRefSystem": "WGS84",
    }
}


class PasswordRequired(Exception):
    """Raised after attempting to access a Link without supplying a password, when one is required"""

    pass


class PasswordInvalid(Exception):
    """Raised after attempting to access a Link with an incorrect password supplied"""

    pass


class LinkInvalid(Exception):
    """Raised after likely accessing a Link which does not exist"""

    pass


class KmlFetch:
    def __init__(self, hass: HomeAssistant, link_name: str, link_password: str) -> None:
        self.httpx = get_async_client(hass)
        self.link_name = link_name
        self.link_password = link_password

    async def authenticate(self) -> bool:
        """Test if we can authenticate with the host. Used during config flow."""
        devices = await self.fetch_data()
        return len(devices) > 0

    async def fetch_data(self):
        if self.link_name == MOCK_LINK_NAME:
            return MOCK_VALUES
        else:
            url = BASE_URL + self.link_name

            auth = None
            if self.link_password != None:
                auth = ("", self.link_password)

            # Try to download (httpx?)
            async with self.httpx as client:
                r = await client.get(url, auth=auth, follow_redirects=True)

            body = r.text
            status_code = r.status_code
            _LOGGER.debug(
                f"Feed URL {url} (auth: {bool(auth)}) returned HTTP status {status_code}, body length {len(body)}"
            )

            if status_code == 401 and auth == None:
                raise PasswordRequired

            if status_code == 401 and auth != None:
                raise PasswordInvalid

            # Make sure response is not empty
            if status_code == 200 and len(body) == 0:
                _LOGGER.warning(
                    f"Server returned an empty response. This usually means the MapShare link name is not valid. Make sure you can successfully visit this map at: https://share.garmin.com/{self.link_name}"
                )
                raise LinkInvalid

            r.raise_for_status()

        return parse_response(body)


def parse_response(body: str):
    """Parse response and populate data key/value pairs"""
    _LOGGER.debug("Fetched KML data: %s", body)
    root = ET.fromstring(body)
    _LOGGER.debug("Parsed KML: %s", root)

    xmlns_prefix = "{http://www.opengis.net/kml/2.2}"

    datas = root.findall(f".//{xmlns_prefix}ExtendedData")

    all_devices = dict()  # Dict keyed by IMEI string
    for data in datas:
        values = dict()
        for el in data.iter(f"{xmlns_prefix}Data"):
            name = el.attrib["name"]
            value_el = el.find(f"{xmlns_prefix}value")
            if value_el is not None:
                last_el = value_el
                value = value_el.text
            else:
                value = ""
            values[name] = value
        # Only keep this event if it's the latest one we've seen for this IMEI
        imei = values["IMEI"]
        if imei not in all_devices or all_devices[imei]["Id"] < values["Id"]:
            all_devices[imei] = values

    _LOGGER.debug("Extracted raw KML values: %s", all_devices)
    return all_devices
