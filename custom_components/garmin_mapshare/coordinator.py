"""Example integration using DataUpdateCoordinator."""

from datetime import timedelta
import logging

import async_timeout

from homeassistant.components.light import LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, CONF_LINK_NAME, CONF_LINK_PASSWORD
from .kml_fetch import KmlFetch

_LOGGER = logging.getLogger(__name__)


# async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
#     """Config entry example."""
#     # assuming API object stored here by __init__.py
#     my_api = hass.data[DOMAIN][entry.entry_id]
#     coordinator = MapShareCoordinator(hass, my_api)

#     # Fetch initial data so we have data when entities subscribe
#     #
#     # If the refresh fails, async_config_entry_first_refresh will
#     # raise ConfigEntryNotReady and setup will try again later
#     #
#     # If you do not want to retry setup on failure, use
#     # coordinator.async_refresh() instead
#     #
#     await coordinator.async_config_entry_first_refresh()

#     async_add_entities(
#         MapShareTrackerEntity(coordinator, idx) for idx, ent in enumerate(coordinator.data)
#     )


class MapShareCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize my coordinator."""
        _LOGGER.warning("MapShareCoordinator: %s", entry.data)

        self.mapshare = KmlFetch(
            hass, entry.data[CONF_LINK_NAME], entry.data[CONF_LINK_PASSWORD]
        )
        self.map_link_name: str = entry.data[CONF_LINK_NAME]
        self.raw_values: dict[str, str] = dict()

        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name=f"{DOMAIN}-{entry.data[CONF_LINK_NAME]}",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(minutes=10),
        )

    async def _async_update_data(self) -> dict[str, str]:
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            async with async_timeout.timeout(10):
                # Grab active context variables to limit data required to be fetched from API
                # Note: using context is not required if there is no need or ability to limit
                # data retrieved from API.
                self.raw_values = await self.mapshare.fetch_data()
                return self.raw_values
        # except ApiAuthError as err:
        #     # Raising ConfigEntryAuthFailed will cancel future updates
        #     # and start a config flow with SOURCE_REAUTH (async_step_reauth)
        #     raise ConfigEntryAuthFailed from err
        # except ApiError as err:
        #     raise UpdateFailed(f"Error communicating with API: {err}")
        finally:
            pass
