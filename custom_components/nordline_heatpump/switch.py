"""Switch platform for Nordline Heat Pump N8A Modbus integration."""

from __future__ import annotations

import logging
import time
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

        self._pending_write: bool | None = None
        self._last_write_time: float = 0.0

        if meta.get("icon"):
            self._attr_icon = meta["icon"]

        # If name has brackets like [System], put in configuration category
        if meta["name"].startswith("["):
            self._attr_entity_category = EntityCategory.CONFIG

    @property
    def is_on(self) -> bool | None:
        """Return True if switch is ON."""
        # Prevent incoming frames from overwriting pending user selection during 5s write lock
        if self._pending_write is not None:
            if time.time() - self._last_write_time < 5.0:
                return self._pending_write
            self._pending_write = None

        hub_pending = self._hub.get_pending_write(self._reg)
        if hub_pending is not None:
            return bool(hub_pending)

        val = self._hub.config_data.get(self._key)
        if val is None:
            return None
        return bool(val)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch ON."""
        self._pending_write = True
        self._last_write_time = time.time()
        self._hub.write_parameter(self._reg, 1)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch OFF."""
        self._pending_write = False
        self._last_write_time = time.time()
        self._hub.write_parameter(self._reg, 0)
        self.async_write_ha_state()
