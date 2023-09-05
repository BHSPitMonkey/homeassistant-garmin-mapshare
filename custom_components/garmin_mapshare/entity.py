from __future__ import annotations
import logging

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN
from .coordinator import MapShareCoordinator

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

        self._attrs: dict[str, str] = {
            "id": ident,
            "display_name": map_display,
            "imei": imei,
        }

        name = f"{model} ({map_display})"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, ident)},
            manufacturer="Garmin",
            model=model,
            name=model,
            configuration_url=f"https://share.garmin.com/share/{coordinator.map_link_name}",
        )

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self._handle_coordinator_update()
