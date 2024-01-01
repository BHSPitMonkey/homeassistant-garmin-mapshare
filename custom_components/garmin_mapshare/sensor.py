from __future__ import annotations

import logging
from datetime import datetime
from typing import cast

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import DEGREE, UnitOfLength, UnitOfSpeed
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import DOMAIN
from .coordinator import MapShareCoordinator
from .entity import MapShareBaseEntity

_LOGGER = logging.getLogger(__name__)


def float_from_first_word(text: str) -> float:
    if str == "":
        return None
    return float(text.split()[0])


def datetime_from_feed(text: str) -> datetime:
    dt = datetime.strptime(text + " +0000", "%m/%d/%Y %I:%M:%S %p %z")
    return dt


SENSOR_TYPES: dict[str, tuple[SensorEntityDescription, callable, str]] = {
    "Latitude": (
        SensorEntityDescription(
            key="latitude",
            translation_key="latitude",
            native_unit_of_measurement=DEGREE,
            icon="mdi:latitude",
            entity_registry_enabled_default=False,
        ),
        float,
        None,
    ),
    "Longitude": (
        SensorEntityDescription(
            key="longitude",
            translation_key="longitude",
            native_unit_of_measurement=DEGREE,
            icon="mdi:longitude",
            entity_registry_enabled_default=False,
        ),
        float,
        None,
    ),
    "Elevation": (
        SensorEntityDescription(
            key="elevation",
            translation_key="elevation",
            icon="mdi:elevation-rise",
            native_unit_of_measurement=UnitOfLength.METERS,
            device_class=SensorDeviceClass.DISTANCE,
        ),
        float_from_first_word,
        None,
    ),
    "Course": (
        SensorEntityDescription(
            key="course",
            translation_key="elevation",
            native_unit_of_measurement=DEGREE,
            icon="mdi:compass",
        ),
        float_from_first_word,
        None,
    ),
    "Velocity": (
        SensorEntityDescription(
            key="velocity",
            translation_key="elevation",
            icon="mdi:speedometer",
            native_unit_of_measurement=UnitOfSpeed.KILOMETERS_PER_HOUR,
            device_class=SensorDeviceClass.SPEED,
        ),
        float_from_first_word,
        None,
    ),
    "Text": (
        SensorEntityDescription(
            key="last_text",
            translation_key="last_text",
            icon="mdi:message-text",
        ),
        None,
        "Last Text",
    ),
    "Event": (
        SensorEntityDescription(
            key="last_event",
            translation_key="last_event",
            icon="mdi:history",
            entity_registry_enabled_default=False,
        ),
        None,
        "Last Event",
    ),
    "Time UTC": (
        SensorEntityDescription(
            key="last_updated",
            translation_key="last_updated",
            device_class=SensorDeviceClass.TIMESTAMP,
        ),
        datetime_from_feed,
        "Last Updated",
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
    for imei in coordinator.raw_values.keys():
        values = coordinator.raw_values[imei]
        entities.extend(
            [
                MapShareSensor(
                    imei,
                    coordinator,
                    attribute_name,
                    description[0],
                    description[1],
                    description[2],
                )
                for attribute_name in values.keys()
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
        imei: str,
        coordinator: MapShareCoordinator,
        kml_key: str,
        description: SensorEntityDescription,
        transformer: callable = None,
        override_name: str = None,
    ) -> None:
        """Initialize MapShare sensor."""
        super().__init__(imei, coordinator)
        _LOGGER.debug("Sensor init: %s %s", description.key, description)
        self.entity_description = description
        self.kml_key = kml_key
        self.transformer = transformer
        self._attr_unique_id = f"{coordinator.map_link_name}-{imei}-{description.key}"
        self._attr_name = kml_key
        if override_name is not None:
            self._attr_name = override_name

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        key = self.entity_description.key
        _LOGGER.debug("Updating sensor '%s' from KML key '%s'", key, self.kml_key)

        # Get (and maybe transform) state value
        state = self.coordinator.raw_values[self.imei].get(self.kml_key)
        if callable(self.transformer):
            state = self.transformer(state)

        self._attr_native_value = cast(StateType, state)
        super()._handle_coordinator_update()
