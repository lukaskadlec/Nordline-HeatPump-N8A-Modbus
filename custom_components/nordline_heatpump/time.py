"""Time platform for Nordline Heat Pump N8A Modbus integration."""

from __future__ import annotations

from datetime import time
import logging
from typing import Any

from homeassistant.components.time import TimeEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, TIME_SETTINGS
from .entity import NordlineHeatPumpEntity
from .hub import NordlineHeatPumpHub

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up all configuration time entities."""
    hub: NordlineHeatPumpHub = hass.data[DOMAIN][entry.entry_id]

    entities = [NordlineHeatPumpTime(hub, item) for item in TIME_SETTINGS]
    async_add_entities(entities)


class NordlineHeatPumpTime(NordlineHeatPumpEntity, TimeEntity):
    """Time entity representing a compacted hour:minute heat pump timer setting."""

    def __init__(self, hub: NordlineHeatPumpHub, meta: dict[str, Any]) -> None:
        """Initialize time entity."""
        safe_id = f"time_{meta['key']}"
        super().__init__(hub, safe_id, meta["name"])
        self._meta = meta
        self._key = meta["key"]
        self._reg_hour = meta["reg_hour"]
        self._reg_minute = meta["reg_minute"]
        self._hour_key = meta["hour_key"]
        self._minute_key = meta["minute_key"]

        if meta.get("icon"):
            self._attr_icon = meta["icon"]

        if meta["name"].startswith("["):
            self._attr_entity_category = EntityCategory.CONFIG

    @property
    def native_value(self) -> time | None:
        """Return the current time value."""
        hour = self._hub.config_raw.get(self._reg_hour)
        if hour is None:
            hour = self._hub.config_data.get(self._hour_key)

        minute = self._hub.config_raw.get(self._reg_minute)
        if minute is None:
            minute = self._hub.config_data.get(self._minute_key)

        if hour is None or minute is None:
            return None

        try:
            h = int(hour)
            m = int(minute)
            if 0 <= h <= 23 and 0 <= m <= 59:
                return time(hour=h, minute=m)
        except (ValueError, TypeError):
            pass
        return None

    async def async_set_value(self, value: time) -> None:
        """Write new time value to heat pump."""
        self._hub.write_time_parameter(
            self._reg_hour,
            self._reg_minute,
            value.hour,
            value.minute,
        )
