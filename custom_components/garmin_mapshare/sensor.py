from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import cast

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import DEGREE, UnitOfLength, UnitOfSpeed
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from . import MapShareBaseEntity
from .const import DOMAIN
from .coordinator import MapShareCoordinator

_LOGGER = logging.getLogger(__name__)

def float_from_first_word(text: str) -> float:
    if str == "":
        return None
    return float(text.split()[0])

SENSOR_TYPES: dict[str, tuple[SensorEntityDescription, callable]] = {
    "Latitude": (SensorEntityDescription(
        key="latitude",
        translation_key="latitude",
        native_unit_of_measurement=DEGREE,
        icon="mdi:latitude",
        entity_registry_enabled_default=False,
    ), float),
    "Longitude": (SensorEntityDescription(
        key="longitude",
        translation_key="longitude",
        native_unit_of_measurement=DEGREE,
        icon="mdi:longitude",
        entity_registry_enabled_default=False,
    ), float),
    "Elevation": (SensorEntityDescription(
        key="elevation",
        translation_key="elevation",
        icon="mdi:elevation-rise",
        native_unit_of_measurement=UnitOfLength.METERS,
    ), float_from_first_word),
    "Course": (SensorEntityDescription(
        key="course",
        translation_key="elevation",
        native_unit_of_measurement=DEGREE,
        icon="mdi:elevation-rise",
    ), float_from_first_word),
    "Velocity": (SensorEntityDescription(
        key="velocity",
        translation_key="elevation",
        icon="mdi:elevation-rise",
        native_unit_of_measurement=UnitOfSpeed.KILOMETERS_PER_HOUR
    ), float_from_first_word),
    "Text": (SensorEntityDescription(
        key="last_text",
        translation_key="last_text",
        icon="mdi:message-text",
    ), None),
    "Event": (SensorEntityDescription(
        key="last_event",
        translation_key="last_event",
        icon="mdi:history",
    ), None),
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
            MapShareSensor(coordinator, attribute_name, description[0], description[1])
            for attribute_name in coordinator.raw_values.keys()
            if (description := SENSOR_TYPES.get(attribute_name))
        ]
    )
    async_add_entities(entities)


class MapShareSensor(MapShareBaseEntity, SensorEntity):
    """Representation of a MapShare sensor."""

    entity_description: SensorEntityDescription
    kml_key: str
    transformer: callable

    def __init__(
        self,
        coordinator: MapShareCoordinator,
        kml_key: str,
        description: SensorEntityDescription,
        transformer: callable = None
    ) -> None:
        """Initialize MapShare sensor."""
        super().__init__(coordinator)
        _LOGGER.warning("Sensor time baby: %s %s", description.key, description)
        self.entity_description = description
        self.kml_key = kml_key
        self.transformer = transformer
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
        key = self.entity_description.key
        _LOGGER.debug("Updating sensor '%s' from KML key '%s'", key, self.kml_key)
        
        # Get (and maybe transform) state value
        state = self.coordinator.raw_values.get(self.kml_key)
        if callable(self.transformer):
            state = self.transformer(state)

        # self._attr_native_value = cast(
        #     StateType, self.entity_description.value(state, self.hass)
        # )
        self._attr_native_value = cast(StateType, state)
        super()._handle_coordinator_update()
