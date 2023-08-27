from datetime import timedelta
import logging
from typing import Any

from homeassistant.components.device_tracker import SourceType, TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import MapShareBaseEntity
from .const import DOMAIN
from .coordinator import MapShareCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the tracker from config entry."""
    coordinator: MapShareCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    entities: list[MapShareTrackerEntity] = []
    entities.append(MapShareTrackerEntity(coordinator))
    async_add_entities(entities)


class MapShareTrackerEntity(MapShareBaseEntity, TrackerEntity):
    """An entity using CoordinatorEntity.

    The CoordinatorEntity class provides:
      should_poll
      async_update
      async_added_to_hass
      available

    """

    _attr_force_update = False
    _attr_icon = "mdi:satellite-uplink"

    def __init__(self, coordinator: MapShareCoordinator) -> None:
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self.coordinator = coordinator

        self._attr_unique_id = coordinator.map_link_name
        self._attr_name = None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # self._attr_is_on = self.coordinator.data[self.idx]["state"]
        self.async_write_ha_state()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return entity specific state attributes."""
        elevation = self.coordinator.raw_values.get("Elevation", "I18N ME: Unknown")
        velocity = self.coordinator.raw_values.get("Velocity", "I18N ME: Unknown")
        course = self.coordinator.raw_values.get("Course", "I18N ME: Unknown")
        updated_utc = self.coordinator.raw_values.get("Time UTC", "I18N ME: Unknown")
        return {
            **self._attrs,
            "elevation": elevation,
            "velocity": velocity,
            "course": course,
            "updated_utc": updated_utc,
        }

    @property
    def latitude(self) -> float | None:
        """Return latitude value of the device."""
        lat = self.coordinator.raw_values["Latitude"]
        if len(lat):
            return float(lat)
        return None

    @property
    def longitude(self) -> float | None:
        """Return longitude value of the device."""
        lon = self.coordinator.raw_values["Longitude"]
        if len(lon):
            return float(lon)
        return None

    @property
    def source_type(self) -> SourceType:
        """Return the source type, eg gps or router, of the device."""
        return SourceType.GPS

    # async def async_refresh(self, **kwargs):
    #     """Ask for a refresh of the MapShare KML data"""

    #     # Update the data
    #     await self.coordinator.async_request_refresh()
