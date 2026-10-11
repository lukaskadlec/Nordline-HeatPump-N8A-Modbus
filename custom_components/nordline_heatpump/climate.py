"""Climate platform for Nordline Heat Pump N8A Modbus integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import NordlineHeatPumpEntity
from .hub import NordlineHeatPumpHub

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Nordline Heat Pump climate entity."""
    hub: NordlineHeatPumpHub = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([NordlineHeatPumpClimate(hub)])


class NordlineHeatPumpClimate(NordlineHeatPumpEntity, ClimateEntity):
    """Climate entity representing the heat pump."""

    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_target_temperature_step = 0.5
    _attr_min_temp = 10.0
    _attr_max_temp = 65.0
    _attr_hvac_modes = [HVACMode.HEAT, HVACMode.COOL, HVACMode.OFF]
    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE
        | ClimateEntityFeature.TURN_ON
        | ClimateEntityFeature.TURN_OFF
    )

    def __init__(self, hub: NordlineHeatPumpHub) -> None:
        """Initialize the climate entity."""
        super().__init__(hub, "climate", "Thermostat")

    @property
    def current_temperature(self) -> float | None:
        """Return the current water outlet temperature (T02)."""
        val = self._hub.telemetry_data.get("Teplota vystup")
        if val is not None:
            return float(val)
        return None

    @property
    def target_temperature(self) -> float | None:
        """Return target setpoint based on active operation mode."""
        mode_val = self._hub.config_data.get("operating_mode")
        # Mode options: 0=Hot Water, 1=Heating, 2=Cooling, 3=Hot Water+Heating, 4=Hot Water+Cooling
        if mode_val in ("Cooling", 2):
            val = self._hub.config_data.get("cooling_target_temp")
            return float(val) if val is not None else 18.0
        elif mode_val in ("Hot Water", 0):
            val = self._hub.config_data.get("boiler_target_temp")
            return float(val) if val is not None else 50.0
        else:
            val = self._hub.config_data.get("heating_target_temp")
            return float(val) if val is not None else 40.0

    @property
    def hvac_mode(self) -> HVACMode:
        """Return current HVAC mode."""
        power_state = self._hub.config_data.get("power_state")
        if power_state is False or power_state == 0:
            return HVACMode.OFF

        mode_val = self._hub.config_data.get("operating_mode")
        if mode_val in ("Cooling", 2, "Hot Water + Cooling", 4):
            return HVACMode.COOL
        return HVACMode.HEAT

    @property
    def hvac_action(self) -> HVACAction | None:
        """Return current operational action."""
        if self.hvac_mode == HVACMode.OFF:
            return HVACAction.OFF

        # Check if compressor relay O01 is running
        comp_running = bool(self._hub.telemetry_data.get("Compressor (O01)"))
        if not comp_running:
            return HVACAction.IDLE

        if self.hvac_mode == HVACMode.COOL:
            return HVACAction.COOLING
        return HVACAction.HEATING

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target HVAC mode."""
        if hvac_mode == HVACMode.OFF:
            self._hub.write_parameter(1011, 0)
            return

        # Ensure unit is powered ON
        self._hub.write_parameter(1011, 1)

        if hvac_mode == HVACMode.COOL:
            self._hub.write_parameter(1012, 2)  # Cooling
        elif hvac_mode == HVACMode.HEAT:
            self._hub.write_parameter(1012, 1)  # Heating

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        temp = kwargs.get(ATTR_TEMPERATURE)
        if temp is None:
            return

        mode_val = self._hub.config_data.get("operating_mode")
        if mode_val in ("Cooling", 2):
            self._hub.write_parameter(1193, round(float(temp), 1))  # Cooling Setpoint
        elif mode_val in ("Hot Water", 0):
            self._hub.write_parameter(1191, round(float(temp), 1))  # DHW Setpoint
        else:
            self._hub.write_parameter(1192, round(float(temp), 1))  # Heating Setpoint
