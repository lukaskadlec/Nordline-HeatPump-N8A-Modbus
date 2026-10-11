"""Base entity class for Nordline Heat Pump integration."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity

from .const import DOMAIN
from .hub import NordlineHeatPumpHub


class NordlineHeatPumpEntity(Entity):
    """Base class for all Nordline Heat Pump entities."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, hub: NordlineHeatPumpHub, unique_id_suffix: str, name: str) -> None:
        """Initialize base entity."""
        self._hub = hub
        self._attr_unique_id = f"nordline_heatpump_{unique_id_suffix}"
        self._attr_name = name

    @property
    def device_info(self) -> DeviceInfo:
        """Return unified device information for Home Assistant."""
        return DeviceInfo(
            identifiers={(DOMAIN, "nordline_heatpump_001")},
            name="Nordline Heat Pump",
            manufacturer="Nordline",
            model="PC8002 PCB Controller (N8A)",
            sw_version="1.2.0",
        )

    @property
    def available(self) -> bool:
        """Return True if hub is connected to serial bus."""
        return self._hub.is_connected

    async def async_added_to_hass(self) -> None:
        """Register callback when entity is added to Home Assistant."""
        self.async_on_remove(self._hub.register_callback(self.async_write_ha_state))
