"""Number platform for Nordline Heat Pump N8A Modbus integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONFIG_REGISTERS, DOMAIN, TIME_REGISTER_NUMBERS
from .entity import NordlineHeatPumpEntity
from .hub import NordlineHeatPumpHub

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up all configuration numbers and setpoints."""
    hub: NordlineHeatPumpHub = hass.data[DOMAIN][entry.entry_id]

    entities: list[NumberEntity] = []

    for item in CONFIG_REGISTERS:
        if item.get("component") != "number":
            continue
        # Exclude registers that have been compacted into Time entities
        if item.get("reg") in TIME_REGISTER_NUMBERS:
            continue
        entities.append(NordlineHeatPumpNumber(hub, item))

    async_add_entities(entities)


class NordlineHeatPumpNumber(NordlineHeatPumpEntity, NumberEntity):
    """Number entity representing a numerical parameter or temperature setpoint."""

    def __init__(self, hub: NordlineHeatPumpHub, meta: dict[str, Any]) -> None:
        """Initialize number entity."""
        safe_id = f"number_reg_{meta['reg']}_{meta['key']}"
        super().__init__(hub, safe_id, meta["name"])
        self._meta = meta
        self._reg = meta["reg"]
        self._key = meta["key"]

        self._attr_native_min_value = float(meta.get("min", 0.0))
        self._attr_native_max_value = float(meta.get("max", 100.0))
        self._attr_native_step = float(meta.get("step", 0.1 if meta.get("scale") == 0.1 else 1.0))

        if meta.get("devClass") == "temperature":
            self._attr_device_class = NumberDeviceClass.TEMPERATURE
            self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        elif meta.get("unit"):
            self._attr_native_unit_of_measurement = meta["unit"]

        if meta.get("mode") == "box":
            self._attr_mode = NumberMode.BOX
        else:
            self._attr_mode = NumberMode.AUTO

        if meta.get("icon"):
            self._attr_icon = meta["icon"]

        # If name has bracket prefix like [Temp] or [Defrost], assign to CONFIG category
        if meta["name"].startswith("["):
            self._attr_entity_category = EntityCategory.CONFIG

    @property
    def native_value(self) -> float | None:
        """Return the current numerical value."""
        val = self._hub.config_data.get(self._key)
        if val is None:
            return None
        try:
            return float(val)
        except (ValueError, TypeError):
            return None

    async def async_set_native_value(self, value: float) -> None:
        """Write new parameter value to heat pump."""
        self._hub.write_parameter(self._reg, value)
