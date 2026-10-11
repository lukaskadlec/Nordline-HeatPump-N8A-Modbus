"""Switch platform for Nordline Heat Pump N8A Modbus integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONFIG_REGISTERS, DOMAIN
from .entity import NordlineHeatPumpEntity
from .hub import NordlineHeatPumpHub

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up all configuration switches."""
    hub: NordlineHeatPumpHub = hass.data[DOMAIN][entry.entry_id]

    entities: list[SwitchEntity] = []

    for item in CONFIG_REGISTERS:
        if item.get("component") != "switch":
            continue
        entities.append(NordlineHeatPumpSwitch(hub, item))

    async_add_entities(entities)


class NordlineHeatPumpSwitch(NordlineHeatPumpEntity, SwitchEntity):
    """Switch representing a writable boolean configuration register."""

    def __init__(self, hub: NordlineHeatPumpHub, meta: dict[str, Any]) -> None:
        """Initialize switch entity."""
        safe_id = f"switch_reg_{meta['reg']}_{meta['key']}"
        super().__init__(hub, safe_id, meta["name"])
        self._meta = meta
        self._reg = meta["reg"]
        self._key = meta["key"]

        if meta.get("icon"):
            self._attr_icon = meta["icon"]

        # If name has brackets like [System], put in configuration category
        if meta["name"].startswith("["):
            self._attr_entity_category = EntityCategory.CONFIG

    @property
    def is_on(self) -> bool | None:
        """Return True if switch is ON."""
        val = self._hub.config_data.get(self._key)
        if val is None:
            return None
        return bool(val)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch ON."""
        self._hub.write_parameter(self._reg, 1)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch OFF."""
        self._hub.write_parameter(self._reg, 0)
