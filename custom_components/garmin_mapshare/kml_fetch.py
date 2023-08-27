import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers.httpx_client import get_async_client
import defusedxml.ElementTree as ET

from .const import BASE_URL

_LOGGER = logging.getLogger(__name__)


class KmlFetch:
    def __init__(self, hass: HomeAssistant, link_name: str, link_password: str) -> None:
        self.httpx = get_async_client(hass)
        self.link_name = link_name
        self.link_password = link_password

    async def authenticate(self) -> bool:
        """Test if we can authenticate with the host. Used during config flow."""
        # FIXME: Implement this
        # Or, remove this and have the ConfigFlow just retrieve the data and hang on to it as the first poll
        return True

    async def fetch_data(self):
        url = BASE_URL + self.link_name

        # Try to download (httpx?)
        async with self.httpx as client:
            r = await client.get(url, auth=("", self.link_password))

        # Parse response and populate data key/value pairs
        # TODO: Parse and return the lat/lon, altitude, last update timestamp, ID, Name, Map Display Name, Device Type, IMEI, Velocity, Incident ID, Course, In Emergency, Text, Event
        _LOGGER.warning("Found me some xml: %s", r.text)
        root = ET.fromstring(r.text)
        _LOGGER.warning("Found me some ET: %s", root)

        xmlns_prefix = "{http://www.opengis.net/kml/2.2}"

        data = root.find(f".//{xmlns_prefix}ExtendedData")
        _LOGGER.warning("Found me some extdata: %s", data)  # None!

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

        _LOGGER.warning("Found me some values: %s", values)
        return values
