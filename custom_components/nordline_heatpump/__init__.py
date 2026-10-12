"""The Nordline Heat Pump N8A Modbus integration."""

from __future__ import annotations

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import CONF_BAUDRATE, CONF_SERIAL_PORT, DEFAULT_BAUDRATE, DOMAIN
from .hub import NordlineHeatPumpHub

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.SWITCH,
    Platform.NUMBER,
    Platform.SELECT,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Nordline Heat Pump from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    serial_port = entry.data[CONF_SERIAL_PORT]
    baudrate = entry.data.get(CONF_BAUDRATE, DEFAULT_BAUDRATE)

    hub = NordlineHeatPumpHub(hass, serial_port=serial_port, baudrate=baudrate)
    hass.data[DOMAIN][entry.entry_id] = hub

    # Start serial communication
    await hub.async_start()

    # Forward setup to all platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hub: NordlineHeatPumpHub = hass.data[DOMAIN].pop(entry.entry_id)
        await hub.async_stop()

    return unload_ok
