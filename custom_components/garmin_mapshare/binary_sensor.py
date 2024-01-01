from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import logging
from typing import Final

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import MapShareCoordinator
from .entity import MapShareBaseEntity

_LOGGER = logging.getLogger(__name__)


@dataclass
class MapShareBinarySensorEntityDescription(BinarySensorEntityDescription):
    """A class that describes custom binary sensor entities."""

    is_on: Callable[[dict[str, str]], bool] | None = None
    on_icon: str | None = None
    off_icon: str | None = None


SENSOR_DESCRIPTIONS: Final[tuple[MapShareBinarySensorEntityDescription, ...]] = (
    MapShareBinarySensorEntityDescription(
        key="in_emergency",
        name="In Emergency",
        is_on=lambda raw_values: raw_values.get("In Emergency", False) == "True",
        on_icon="mdi:alert-circle",
        off_icon="mdi:alert-circle",
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
    MapShareBinarySensorEntityDescription(
        key="valid_gps_fix",
        name="Valid GPS Fix",
        is_on=lambda raw_values: raw_values.get("Valid GPS Fix", False) == "True",
        on_icon="mdi:crosshairs-gps",
        off_icon="mdi:crosshairs",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up binary_sensor platform."""
    coordinator: MapShareCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    entities: list[MapShareConnectBinarySensor] = []
    for imei in coordinator.raw_values.keys():
        for description in SENSOR_DESCRIPTIONS:
            entities.append(MapShareConnectBinarySensor(imei, coordinator, description))
    async_add_entities(entities)
    return True


class MapShareConnectBinarySensor(BinarySensorEntity, MapShareBaseEntity):
    def __init__(
        self,
        imei: str,
        coordinator: MapShareCoordinator,
        description: MapShareBinarySensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(imei, coordinator)
        self.entity_description: MapShareBinarySensorEntityDescription = description
        self._attr_unique_id = f"{coordinator.map_link_name}-{imei}-{description.key}"
        self._attr_name = f"{description.name}"

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        if self.entity_description.is_on is not None:
            return self.entity_description.is_on(self.coordinator.raw_values[self.imei])
        return None

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        if (
            self.entity_description.on_icon == self.entity_description.off_icon
        ) is None:
            return BinarySensorEntity.icon
        return (
            self.entity_description.on_icon
            if self.is_on
            else self.entity_description.off_icon
        )
