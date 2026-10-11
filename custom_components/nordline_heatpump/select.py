"""Select platform for Nordline Heat Pump N8A Modbus integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.select import SelectEntity
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
    """Set up all configuration selects."""
    hub: NordlineHeatPumpHub = hass.data[DOMAIN][entry.entry_id]

    entities: list[SelectEntity] = []

    for item in CONFIG_REGISTERS:
        if item.get("component") != "select":
            continue
        entities.append(NordlineHeatPumpSelect(hub, item))

    async_add_entities(entities)


class NordlineHeatPumpSelect(NordlineHeatPumpEntity, SelectEntity):
    """Select entity representing an enumerated configuration register."""

    def __init__(self, hub: NordlineHeatPumpHub, meta: dict[str, Any]) -> None:
        """Initialize select entity."""
        safe_id = f"select_reg_{meta['reg']}_{meta['key']}"
        super().__init__(hub, safe_id, meta["name"])
        self._meta = meta
        self._reg = meta["reg"]
        self._key = meta["key"]
        self._attr_options = meta.get("options", [])

        if meta.get("icon"):
            self._attr_icon = meta["icon"]

        # If name has bracket prefix like [System], put into CONFIG category
        if meta["name"].startswith("["):
            self._attr_entity_category = EntityCategory.CONFIG

    @property
    def current_option(self) -> str | None:
        """Return the currently selected option."""
        val = self._hub.config_data.get(self._key)
        if val is None:
            return None
        return str(val)

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        self._hub.write_parameter(self._reg, option)
