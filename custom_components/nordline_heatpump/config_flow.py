"""Config flow for Nordline Heat Pump N8A Modbus integration."""

from __future__ import annotations

import logging
from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
import serial.tools.list_ports

from .const import (
    CONF_BAUDRATE,
    CONF_SERIAL_PORT,
    DEFAULT_BAUDRATE,
    DEFAULT_SERIAL_PORT,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


def get_available_serial_ports() -> list[str]:
    """List available serial ports on host."""
    ports = [port.device for port in serial.tools.list_ports.comports()]
    if DEFAULT_SERIAL_PORT not in ports:
        ports.append(DEFAULT_SERIAL_PORT)
    return ports


class NordlineHeatPumpConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Nordline Heat Pump N8A Modbus."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            serial_port = user_input[CONF_SERIAL_PORT]

            # Ensure unique entry per serial port
            await self.async_set_unique_id(serial_port)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"Nordline Heat Pump ({serial_port})",
                data=user_input,
            )

        available_ports = await self.hass.async_add_executor_job(get_available_serial_ports)

        # Build schema
        schema = vol.Schema(
            {
                vol.Required(CONF_SERIAL_PORT, default=available_ports[0] if available_ports else DEFAULT_SERIAL_PORT): (
                    vol.In(available_ports) if len(available_ports) > 1 else str
                ),
                vol.Required(CONF_BAUDRATE, default=DEFAULT_BAUDRATE): vol.In([9600, 19200, 38400, 115200]),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
