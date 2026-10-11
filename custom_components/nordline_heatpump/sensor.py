"""Sensor platform for Nordline Heat Pump N8A Modbus integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    EntityCategory,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfFrequency,
    UnitOfPressure,
    UnitOfTemperature,
)
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
    """Set up all telemetry and diagnostic sensors."""
    hub: NordlineHeatPumpHub = hass.data[DOMAIN][entry.entry_id]

    entities: list[SensorEntity] = []

    for key, meta in TELEMETRY_SENSORS_META.items():
        if meta.get("component") == "binary_sensor":
            continue
        entities.append(NordlineHeatPumpTelemetrySensor(hub, key, meta))

    # Add diagnostic sensors for bus watchdog and daily EEPROM write counter
    entities.append(NordlineDailyWritesSensor(hub))
    entities.append(NordlineLcdStatusSensor(hub))

    async_add_entities(entities)


class NordlineHeatPumpTelemetrySensor(NordlineHeatPumpEntity, SensorEntity):
    """Sensor representing a live telemetry metric."""

    def __init__(self, hub: NordlineHeatPumpHub, sensor_key: str, meta: dict[str, Any]) -> None:
        """Initialize telemetry sensor."""
        safe_id = "sensor_" + sensor_key.lower().replace(" ", "_").replace("/", "_")
        super().__init__(hub, safe_id, meta["name"])
        self._sensor_key = sensor_key
        self._meta = meta

        # Assign Device Class
        dev_class = meta.get("devClass")
        if dev_class == "temperature":
            self._attr_device_class = SensorDeviceClass.TEMPERATURE
            self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif dev_class == "pressure":
            self._attr_device_class = SensorDeviceClass.PRESSURE
            self._attr_native_unit_of_measurement = UnitOfPressure.BAR
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif dev_class == "voltage":
            self._attr_device_class = SensorDeviceClass.VOLTAGE
            self._attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif dev_class == "current":
            self._attr_device_class = SensorDeviceClass.CURRENT
            self._attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif dev_class == "frequency":
            self._attr_device_class = SensorDeviceClass.FREQUENCY
            self._attr_native_unit_of_measurement = UnitOfFrequency.HERTZ
            self._attr_state_class = SensorStateClass.MEASUREMENT
        else:
            unit = meta.get("unit")
            if unit:
                self._attr_native_unit_of_measurement = unit
                if unit == "rpm":
                    self._attr_state_class = SensorStateClass.MEASUREMENT

        if meta.get("icon"):
            self._attr_icon = meta["icon"]

        if meta.get("entityCategory") == "diagnostic":
            self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self) -> Any:
        """Return the current sensor value."""
        return self._hub.telemetry_data.get(self._sensor_key)


class NordlineDailyWritesSensor(NordlineHeatPumpEntity, SensorEntity):
    """Diagnostic sensor tracking daily EEPROM configuration writes."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:counter"
    _attr_state_class = SensorStateClass.TOTAL_INCREASING

    def __init__(self, hub: NordlineHeatPumpHub) -> None:
        """Initialize daily writes counter sensor."""
        super().__init__(hub, "daily_eeprom_writes", "[System] Daily EEPROM Writes")

    @property
    def native_value(self) -> int:
        """Return daily write count."""
        return self._hub.daily_write_count

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return write limit attributes."""
        return {
            "daily_safe_limit": 20,
            "date": self._hub.daily_write_date,
            "remaining_writes": max(0, 20 - self._hub.daily_write_count),
        }


class NordlineLcdStatusSensor(NordlineHeatPumpEntity, SensorEntity):
    """Diagnostic sensor indicating LCD emulation and bus watchdog status."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:monitor"

    def __init__(self, hub: NordlineHeatPumpHub) -> None:
        """Initialize LCD status sensor."""
        super().__init__(hub, "lcd_bus_status", "[System] LCD Bus Control Status")

    @property
    def native_value(self) -> str:
        """Return active bus controller description."""
        if self._hub.lcd_emulator_enabled:
            return "Emulated (Node-RED/HA Responder)"
        return "Physical LCD Wall Unit Active"
