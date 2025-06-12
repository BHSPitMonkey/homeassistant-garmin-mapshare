import logging
from typing import Any

from homeassistant.components.device_tracker import SourceType, TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import MapShareCoordinator
from .entity import MapShareBaseEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the tracker from config entry."""
    coordinator: MapShareCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    entities: list[MapShareTrackerEntity] = []
    for imei in coordinator.raw_values.keys():
        entities.append(MapShareTrackerEntity(imei, coordinator))
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

    def __init__(self, imei: str, coordinator: MapShareCoordinator) -> None:
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(imei, coordinator)

        self._attr_unique_id = f"{coordinator.map_link_name}-{imei}-tracker"
        self._attr_name = None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return entity specific state attributes."""
        values = self.coordinator.raw_values[self.imei]
        elevation = values.get("Elevation", "I18N ME: Unknown")
        velocity = values.get("Velocity", "I18N ME: Unknown")
        course = values.get("Course", "I18N ME: Unknown")
        updated_utc = values.get("Time UTC", "I18N ME: Unknown")
        return {
            **self._attrs,
            "elevation": elevation,
            "velocity": velocity,
            "course": course,
            "updated_utc": updated_utc,
            "link_name": self.coordinator.map_link_name,
        }

    @property
    def latitude(self) -> float | None:
        """Return latitude value of the device."""
        lat = self.coordinator.raw_values[self.imei]["Latitude"]
        if len(lat):
            return float(lat)
        return None

    @property
    def longitude(self) -> float | None:
        """Return longitude value of the device."""
        lon = self.coordinator.raw_values[self.imei]["Longitude"]
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
