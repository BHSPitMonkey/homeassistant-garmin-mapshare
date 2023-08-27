"""The Garmin MapShare integration."""
from __future__ import annotations
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN
from .coordinator import MapShareCoordinator

_LOGGER = logging.getLogger(__name__)

# ist the platforms that you want to support.
PLATFORMS: list[Platform] = [Platform.DEVICE_TRACKER, Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Garmin MapShare from a config entry."""

    # Set up one data coordinator per account/config entry
    coordinator = MapShareCoordinator(
        hass,
        entry=entry,
    )
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class MapShareBaseEntity(CoordinatorEntity[MapShareCoordinator]):
    """Common base for MapShare entities."""

    coordinator: MapShareCoordinator
    # _attr_attribution = ATTRIBUTION
    _attr_attribution = "Garmin MapShare"
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MapShareCoordinator,
    ) -> None:
        """Initialize entity."""
        super().__init__(coordinator)

        model = coordinator.raw_values.get("Device Type", "I18N ME: Unknown")
        ident = coordinator.raw_values.get("Id", "I18N ME: Unknown")
        map_display = coordinator.raw_values.get("Map Display Name", "I18N ME: Unknown")
        imei = coordinator.raw_values.get("IMEI", "I18N ME: Unknown")

        # self.vehicle = vehicle

        self._attrs: dict[str, str] = {
            "id": ident,
            "display_name": map_display,
            "imei": imei,
        }
        _LOGGER.warning("Doin the thing")
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, ident)},
            manufacturer="Garmin",
            model=model,
            name=model,
        )

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self._handle_coordinator_update()
