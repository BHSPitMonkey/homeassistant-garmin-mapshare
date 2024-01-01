from __future__ import annotations

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import DATA_ATTRIBUTION, DOMAIN, MANUFACTURER, WEB_BASE_URL
from .coordinator import MapShareCoordinator


class MapShareBaseEntity(CoordinatorEntity[MapShareCoordinator]):
    """Common base for MapShare entities."""

    coordinator: MapShareCoordinator
    imei: str
    _attr_attribution = DATA_ATTRIBUTION
    _attr_has_entity_name = True

    def __init__(
        self,
        imei: str,
        coordinator: MapShareCoordinator,
    ) -> None:
        """Initialize entity."""
        super().__init__(coordinator)

        self.imei = imei
        values = coordinator.raw_values[imei]
        model = values.get("Device Type", "Unknown")
        map_display = values.get("Map Display Name", "Unknown")

        self._attrs: dict[str, str] = {
            "display_name": map_display,
            "imei": imei,
        }

        name = f"{model} ({map_display})"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, imei)},
            manufacturer=MANUFACTURER,
            model=model,
            name=name,
            configuration_url=f"{WEB_BASE_URL}{coordinator.map_link_name}",
        )

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self._handle_coordinator_update()
