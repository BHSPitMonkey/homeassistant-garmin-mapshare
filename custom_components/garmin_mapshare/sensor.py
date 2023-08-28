from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import cast

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import DEGREE, LENGTH, UnitOfLength
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from . import MapShareBaseEntity
from .const import DOMAIN
from .coordinator import MapShareCoordinator

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES: dict[str, SensorEntityDescription] = {
    "Latitude": SensorEntityDescription(
        key="latitude",
        translation_key="latitude",
        # unit_type=DEGREE,
        icon="mdi:latitude",
        entity_registry_enabled_default=False,
    ),
    "Longitude": SensorEntityDescription(
        key="longitude",
        translation_key="longitude",
        # unit_type=DEGREE,
        icon="mdi:longitude",
        entity_registry_enabled_default=False,
    ),
    "Elevation": SensorEntityDescription(
        key="elevation",
        translation_key="elevation",
        icon="mdi:elevation-rise",
        # unit_type=UnitOfLength.METERS,
    ),
    "Course": SensorEntityDescription(
        key="course",
        translation_key="elevation",
        icon="mdi:elevation-rise",
    ),
    "Velocity": SensorEntityDescription(
        key="velocity",
        translation_key="elevation",
        icon="mdi:elevation-rise",
        # unit_type=UnitOfSpeed.KILOMETERS_PER_HOUR
    ),
    "Text": SensorEntityDescription(
        key="last_text",
        translation_key="last_text",
        icon="mdi:message-text",
    ),
    "Event": SensorEntityDescription(
        key="last_event",
        translation_key="last_event",
        icon="mdi:history",
    ),
}


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the MapShare sensors from config entry."""
    coordinator: MapShareCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities: list[MapShareSensor] = []
    entities.extend(
        [
            MapShareSensor(coordinator, description)
            for attribute_name in coordinator.raw_values.keys()
            if (description := SENSOR_TYPES.get(attribute_name))
        ]
    )
    async_add_entities(entities)


class MapShareSensor(MapShareBaseEntity, SensorEntity):
    """Representation of a MapShare sensor."""

    entity_description: SensorEntityDescription

    def __init__(
        self,
        coordinator: MapShareCoordinator,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize MapShare sensor."""
        super().__init__(coordinator)
        _LOGGER.warning("Sensor time baby: %s %s", description.key, description)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.map_link_name}-{description.key}"
        self._attr_name = description.key

        # Set the correct unit of measurement based on the unit_type
        # if description.unit_type:
        #     self._attr_native_unit_of_measurement = (
        #         coordinator.hass.config.units.as_dict().get(description.unit_type)
        #         or description.unit_type
        #     )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug("Updating sensor '%s'", self.entity_description.key)
        state = self.coordinator.raw_values.get(self.entity_description.key)

        # self._attr_native_value = cast(
        #     StateType, self.entity_description.value(state, self.hass)
        # )
        self._attr_native_value = cast(StateType, state)
        super()._handle_coordinator_update()
