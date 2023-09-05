from __future__ import annotations

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import DATA_ATTRIBUTION, DOMAIN, MANUFACTURER, WEB_BASE_URL
from .coordinator import MapShareCoordinator

class MapShareBaseEntity(CoordinatorEntity[MapShareCoordinator]):
    """Common base for MapShare entities."""

    coordinator: MapShareCoordinator
    _attr_attribution = DATA_ATTRIBUTION
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MapShareCoordinator,
    ) -> None:
        """Initialize entity."""
        super().__init__(coordinator)

        model = coordinator.raw_values.get("Device Type", "Unknown")
        ident = coordinator.raw_values.get("Id", "Unknown")
        map_display = coordinator.raw_values.get("Map Display Name", "Unknown")
        imei = coordinator.raw_values.get("IMEI", "Unknown")

        self._attrs: dict[str, str] = {
            "id": ident,
            "display_name": map_display,
            "imei": imei,
        }

        name = f"{model} ({map_display})"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, ident)},
            manufacturer=MANUFACTURER,
            model=model,
            name=name,
            configuration_url=f"{WEB_BASE_URL}{coordinator.map_link_name}",
        )

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self._handle_coordinator_update()
