"""Binary sensor platform for Nordline Heat Pump N8A Modbus integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, TELEMETRY_SENSORS_META
from .entity import NordlineHeatPumpEntity
from .hub import NordlineHeatPumpHub

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up all relay and safety switch binary sensors."""
    hub: NordlineHeatPumpHub = hass.data[DOMAIN][entry.entry_id]

    entities: list[BinarySensorEntity] = []

    for key, meta in TELEMETRY_SENSORS_META.items():
        if meta.get("component") != "binary_sensor":
            continue
        entities.append(NordlineHeatPumpBinarySensor(hub, key, meta))

    async_add_entities(entities)


class NordlineHeatPumpBinarySensor(NordlineHeatPumpEntity, BinarySensorEntity):
    """Binary sensor representing a digital relay output or safety switch input."""

    def __init__(self, hub: NordlineHeatPumpHub, sensor_key: str, meta: dict[str, Any]) -> None:
        """Initialize binary sensor."""
        safe_id = "binary_" + sensor_key.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_")
        super().__init__(hub, safe_id, meta["name"])
        self._sensor_key = sensor_key
        self._meta = meta

        dev_class = meta.get("devClass")
        if dev_class == "problem":
            self._attr_device_class = BinarySensorDeviceClass.PROBLEM
        elif dev_class:
            self._attr_device_class = dev_class

        if meta.get("icon"):
            self._attr_icon = meta["icon"]

        if meta.get("entityCategory") == "diagnostic":
            self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def is_on(self) -> bool | None:
        """Return True if relay is ON or alarm switch is tripped."""
        val = self._hub.telemetry_data.get(self._sensor_key)
        if val is None:
            return None
        return bool(val)
