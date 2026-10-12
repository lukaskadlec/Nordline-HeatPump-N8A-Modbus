"""Constants and register definitions for Nordline Heat Pump N8A Modbus integration."""

from typing import Any

DOMAIN = "nordline_heatpump"
CONF_SERIAL_PORT = "serial_port"
CONF_BAUDRATE = "baudrate"

DEFAULT_SERIAL_PORT = "/dev/ttyUSB-TC"
DEFAULT_BAUDRATE = 9600
DEFAULT_NAME = "Nordline Heat Pump"

# Modbus slave ID and function codes
SLAVE_ID = 1
FC_READ_HOLDING = 3
FC_WRITE_MULTIPLE = 16

# Telemetry raw decoder specifications (42 items from Broadcast Part A)
TELEMETRY_DECODER_ITEMS: list[dict[str, Any]] = [
    {
        "type": "int16be",
        "name": "Teplota vstup",
        "offset": 95,
        "length": 1,
        "offsetbit": 0,
        "scale": "/10",
        "mask": ""
    },
    {
        "type": "int16be",
        "name": "Teplota vystup",
        "offset": 97,
        "length": 1,
        "offsetbit": 0,
        "scale": "/10",
        "mask": ""
    },
    {
        "type": "int16be",
        "name": "Teplota vytlak",
        "offset": 99,
        "length": 1,
        "offsetbit": 0,
        "scale": "/10",
        "mask": ""
    },
    {
        "type": "int16be",
        "name": "Teplota bojler",
        "offset": 101,
        "length": 1,
        "offsetbit": 0,
        "scale": "/10",
        "mask": ""
    },
    {
        "type": "int16be",
        "name": "Teplota sani",
        "offset": 103,
        "length": 1,
        "offsetbit": 0,
        "scale": "/10",
        "mask": ""
    },
    {
        "type": "int16be",
        "name": "Teplota vyparnik",
        "offset": 105,
        "length": 1,
        "offsetbit": 0,
        "scale": "/10",
        "mask": ""
    },
    {
        "type": "int16be",
        "name": "Teplota okoli",
        "offset": 107,
        "length": 1,
        "offsetbit": 0,
        "scale": "/10",
        "mask": ""
    },
    {
        "type": "int16be",
        "name": "Tlak sani",
        "offset": 109,
        "length": 1,
        "offsetbit": 0,
        "scale": "/10",
        "mask": ""
    },
    {
        "type": "int16be",
        "name": "Tlak vytlak",
        "offset": 111,
        "length": 1,
        "offsetbit": 0,
        "scale": "/10",
        "mask": ""
    },
    {
        "type": "int16be",
        "name": "Frekvence nastavena",
        "offset": 113,
        "length": 1,
        "offsetbit": 0,
        "scale": "1",
        "mask": ""
    },
    {
        "type": "int16be",
        "name": "Frekvence skutecna",
        "offset": 115,
        "length": 1,
        "offsetbit": 0,
        "scale": "1",
        "mask": ""
    },
    {
        "type": "uint16be",
        "name": "Ventilator rychlost",
        "offset": 117,
        "length": 1,
        "offsetbit": 0,
        "scale": "0",
        "mask": ""
    },
    {
        "type": "int16be",
        "name": "Prehrati sani",
        "offset": 121,
        "length": 1,
        "offsetbit": 0,
        "scale": "/10",
        "mask": ""
    },
    {
        "type": "int16be",
        "name": "Prehrati vytlak",
        "offset": 123,
        "length": 1,
        "offsetbit": 0,
        "scale": "/10",
        "mask": ""
    },
    {
        "type": "int16be",
        "name": "Hodnota ochrane teploty modulu",
        "offset": 125,
        "length": 1,
        "offsetbit": 0,
        "scale": "/10",
        "mask": ""
    },
    {
        "type": "uint16be",
        "name": "AC vstupni napeti",
        "offset": 127,
        "length": 1,
        "offsetbit": 0,
        "scale": "0",
        "mask": ""
    },
    {
        "type": "uint16be",
        "name": "AC vstupni proud",
        "offset": 129,
        "length": 1,
        "offsetbit": 0,
        "scale": "/10",
        "mask": ""
    },
    {
        "type": "uint16be",
        "name": "Fazovy proud kompresoru",
        "offset": 131,
        "length": 1,
        "offsetbit": 0,
        "scale": "/10",
        "mask": ""
    },
    {
        "type": "uint16be",
        "name": "Napeti sbernice",
        "offset": 133,
        "length": 1,
        "offsetbit": 0,
        "scale": "0",
        "mask": ""
    },
    {
        "type": "int16be",
        "name": "Teplota invertoru",
        "offset": 135,
        "length": 1,
        "offsetbit": 0,
        "scale": "/10",
        "mask": ""
    },
    {
        "type": "uint16be",
        "name": "Ventilator nastavena rychlost",
        "offset": 137,
        "length": 1,
        "offsetbit": 0,
        "scale": "0",
        "mask": ""
    },
    {
        "type": "bool",
        "name": "Compressor (O01)",
        "offset": 44,
        "length": 1,
        "offsetbit": 0,
        "scale": "1",
        "mask": ""
    },
    {
        "type": "bool",
        "name": "Water Pump (O02)",
        "offset": 44,
        "length": 1,
        "offsetbit": 1,
        "scale": "1",
        "mask": ""
    },
    {
        "type": "bool",
        "name": "4-way Valve (O03)",
        "offset": 44,
        "length": 1,
        "offsetbit": 2,
        "scale": "1",
        "mask": ""
    },
    {
        "type": "bool",
        "name": "Fan Motor (O04)",
        "offset": 44,
        "length": 1,
        "offsetbit": 3,
        "scale": "1",
        "mask": ""
    },
    {
        "type": "bool",
        "name": "Antifreeze Heating Strip (O06)",
        "offset": 44,
        "length": 1,
        "offsetbit": 5,
        "scale": "1",
        "mask": ""
    },
    {
        "type": "bool",
        "name": "Crank Antifreeze Heating Strip (O07)",
        "offset": 44,
        "length": 1,
        "offsetbit": 6,
        "scale": "1",
        "mask": ""
    },
    {
        "type": "bool",
        "name": "Spray Valve (O08)",
        "offset": 44,
        "length": 1,
        "offsetbit": 7,
        "scale": "1",
        "mask": ""
    },
    {
        "type": "bool",
        "name": "Auxiliary Electric Heater (O09)",
        "offset": 43,
        "length": 1,
        "offsetbit": 0,
        "scale": "1",
        "mask": ""
    },
    {
        "type": "bool",
        "name": "Alarm (O11)",
        "offset": 43,
        "length": 1,
        "offsetbit": 2,
        "scale": "1",
        "mask": ""
    },
    {
        "type": "bool",
        "name": "Hot Water Pump (O12)",
        "offset": 43,
        "length": 1,
        "offsetbit": 3,
        "scale": "1",
        "mask": ""
    },
    {
        "type": "bool",
        "name": "3-way Valve (O13)",
        "offset": 43,
        "length": 1,
        "offsetbit": 4,
        "scale": "1",
        "mask": ""
    },
    {
        "type": "int16be",
        "name": "EVV",
        "offset": 45,
        "length": 1,
        "offsetbit": 0,
        "scale": "0",
        "mask": ""
    },
    {
        "type": "int16be",
        "name": "ON/OFF",
        "offset": 27,
        "length": 1,
        "offsetbit": 0,
        "scale": "0",
        "mask": ""
    },
    {
        "type": "int16be",
        "name": "Unit Status",
        "offset": 73,
        "length": 1,
        "offsetbit": 0,
        "scale": "0",
        "mask": ""
    },
    {
        "type": "bool",
        "name": "High Pressure Alarm (S01)",
        "offset": 176,
        "length": 1,
        "offsetbit": 0,
        "scale": "1",
        "mask": ""
    },
    {
        "type": "bool",
        "name": "Low Pressure Alarm (S02)",
        "offset": 176,
        "length": 1,
        "offsetbit": 1,
        "scale": "1",
        "mask": ""
    },
    {
        "type": "bool",
        "name": "Water Flow Alarm (S03)",
        "offset": 176,
        "length": 1,
        "offsetbit": 2,
        "scale": "1",
        "mask": ""
    },
    {
        "type": "bool",
        "name": "Emergency Switch Alarm (S04)",
        "offset": 176,
        "length": 1,
        "offsetbit": 3,
        "scale": "1",
        "mask": ""
    },
    {
        "type": "bool",
        "name": "Mode Switch (S05)",
        "offset": 176,
        "length": 1,
        "offsetbit": 4,
        "scale": "1",
        "mask": ""
    },
    {
        "type": "bool",
        "name": "Heater Overload Alarm (S07)",
        "offset": 176,
        "length": 1,
        "offsetbit": 6,
        "scale": "1",
        "mask": ""
    },
    {
        "type": "uint8",
        "name": "Alarm detail",
        "offset": 175,
        "length": 1,
        "offsetbit": 0,
        "scale": "0",
        "mask": ""
    }
]

# Telemetry Home Assistant sensor metadata
TELEMETRY_SENSORS_META: dict[str, dict[str, Any]] = {
    "Teplota vstup": {
        "unit": "°C",
        "devClass": "temperature",
        "name": "[Temp] Water - Inlet",
        "icon": "mdi:thermometer-chevron-down"
    },
    "Teplota vystup": {
        "unit": "°C",
        "devClass": "temperature",
        "name": "[Temp] Water - Outlet",
        "icon": "mdi:thermometer-chevron-up"
    },
    "Teplota vytlak": {
        "unit": "°C",
        "devClass": "temperature",
        "name": "[Temp] Refrig - Discharge",
        "icon": "mdi:thermometer-alert"
    },
    "Teplota bojler": {
        "unit": "°C",
        "devClass": "temperature",
        "name": "[Temp] Water - Boiler",
        "icon": "mdi:water-boiler"
    },
    "Teplota sani": {
        "unit": "°C",
        "devClass": "temperature",
        "name": "[Temp] Refrig - Suction",
        "icon": "mdi:thermometer-low"
    },
    "Teplota vyparnik": {
        "unit": "°C",
        "devClass": "temperature",
        "name": "[Temp] Refrig - Evaporator",
        "icon": "mdi:snowflake-thermometer"
    },
    "Teplota okoli": {
        "unit": "°C",
        "devClass": "temperature",
        "name": "[Temp] System - Ambient",
        "icon": "mdi:thermometer"
    },
    "Teplota invertoru": {
        "unit": "°C",
        "devClass": "temperature",
        "name": "[Temp] System - Inverter",
        "icon": "mdi:chip"
    },
    "Hodnota ochrane teploty modulu": {
        "unit": "°C",
        "devClass": "temperature",
        "name": "[Temp] System - Module Protection",
        "icon": "mdi:shield-alert"
    },
    "Prehrati sani": {
        "unit": "°C",
        "devClass": "temperature",
        "name": "[Temp] Refrig - Superheat Suction",
        "icon": "mdi:thermometer-lines"
    },
    "Prehrati vytlak": {
        "unit": "°C",
        "devClass": "temperature",
        "name": "[Temp] Refrig - Superheat Discharge",
        "icon": "mdi:thermometer-lines"
    },
    "Tlak sani": {
        "unit": "bar",
        "devClass": "pressure",
        "name": "[Pressure] Refrig - Suction Pressure",
        "icon": "mdi:gauge-low"
    },
    "Tlak vytlak": {
        "unit": "bar",
        "devClass": "pressure",
        "name": "[Pressure] Refrig - Discharge Pressure",
        "icon": "mdi:gauge"
    },
    "Frekvence nastavena": {
        "unit": "Hz",
        "devClass": "frequency",
        "name": "[System] Status - Freq Set",
        "icon": "mdi:sine-wave"
    },
    "Frekvence skutecna": {
        "unit": "Hz",
        "devClass": "frequency",
        "name": "[System] Status - Freq Actual",
        "icon": "mdi:sine-wave"
    },
    "Ventilator rychlost": {
        "unit": "rpm",
        "icon": "mdi:fan",
        "name": "[Fan] Motor - Speed"
    },
    "Ventilator nastavena rychlost": {
        "unit": "rpm",
        "icon": "mdi:fan",
        "name": "[Fan] Motor - Speed Set"
    },
    "AC vstupni napeti": {
        "unit": "V",
        "devClass": "voltage",
        "name": "[Electrical] AC - Input Voltage",
        "icon": "mdi:lightning-bolt"
    },
    "Napeti sbernice": {
        "unit": "V",
        "devClass": "voltage",
        "name": "[Electrical] DC - Bus Voltage",
        "icon": "mdi:flash"
    },
    "AC vstupni proud": {
        "unit": "A",
        "devClass": "current",
        "name": "[Electrical] AC - Input Current",
        "icon": "mdi:current-ac"
    },
    "Fazovy proud kompresoru": {
        "unit": "A",
        "devClass": "current",
        "name": "[Electrical] Comp - Compressor Current",
        "icon": "mdi:current-ac"
    },
    "Compressor (O01)": {
        "component": "binary_sensor",
        "name": "[Output] O01 Compressor",
        "icon": "mdi:air-conditioner"
    },
    "Water Pump (O02)": {
        "component": "binary_sensor",
        "name": "[Output] O02 Water Pump",
        "icon": "mdi:water-pump"
    },
    "4-way Valve (O03)": {
        "component": "binary_sensor",
        "name": "[Output] O03 4-way Valve",
        "icon": "mdi:valve"
    },
    "Fan Motor (O04)": {
        "component": "binary_sensor",
        "name": "[Output] O04 Fan Motor",
        "icon": "mdi:fan"
    },
    "Antifreeze Heating Strip (O06)": {
        "component": "binary_sensor",
        "name": "[Output] O06 Antifreeze Heat Strip",
        "icon": "mdi:heating-coil"
    },
    "Crank Antifreeze Heating Strip (O07)": {
        "component": "binary_sensor",
        "name": "[Output] O07 Crankcase Heat Strip",
        "icon": "mdi:heating-coil"
    },
    "Spray Valve (O08)": {
        "component": "binary_sensor",
        "name": "[Output] O08 Spray Valve",
        "icon": "mdi:spray"
    },
    "Auxiliary Electric Heater (O09)": {
        "component": "binary_sensor",
        "name": "[Output] O09 Aux Electric Heater",
        "icon": "mdi:patio-heater"
    },
    "Alarm (O11)": {
        "component": "binary_sensor",
        "devClass": "problem",
        "name": "[Output] O11 Alarm Output",
        "icon": "mdi:alert-circle"
    },
    "Hot Water Pump (O12)": {
        "component": "binary_sensor",
        "name": "[Output] O12 Hot Water Pump",
        "icon": "mdi:water-pump"
    },
    "3-way Valve (O13)": {
        "component": "binary_sensor",
        "name": "[Output] O13 3-way Valve",
        "icon": "mdi:valve"
    },
    "EVV": {
        "icon": "mdi:pipe-valve",
        "name": "[EEV] Valve - Steps"
    },
    "ON/OFF": {
        "name": "[System] Status - Power ON/OFF",
        "icon": "mdi:power"
    },
    "Unit Status": {
        "name": "[System] Status - Status",
        "icon": "mdi:list-status"
    },
    "High Pressure Alarm (S01)": {
        "component": "binary_sensor",
        "devClass": "problem",
        "entityCategory": "diagnostic",
        "name": "[Alarm] S01 High Pressure",
        "icon": "mdi:gauge-full"
    },
    "Low Pressure Alarm (S02)": {
        "component": "binary_sensor",
        "devClass": "problem",
        "entityCategory": "diagnostic",
        "name": "[Alarm] S02 Low Pressure",
        "icon": "mdi:gauge-empty"
    },
    "Water Flow Alarm (S03)": {
        "component": "binary_sensor",
        "devClass": "problem",
        "entityCategory": "diagnostic",
        "name": "[Alarm] S03 Water Flow",
        "icon": "mdi:water-alert"
    },
    "Emergency Switch Alarm (S04)": {
        "component": "binary_sensor",
        "devClass": "problem",
        "entityCategory": "diagnostic",
        "name": "[Alarm] S04 Emergency Switch",
        "icon": "mdi:alert-octagon"
    },
    "Mode Switch (S05)": {
        "component": "binary_sensor",
        "entityCategory": "diagnostic",
        "name": "[Alarm] S05 Mode Switch",
        "icon": "mdi:toggle-switch"
    },
    "Heater Overload Alarm (S07)": {
        "component": "binary_sensor",
        "devClass": "problem",
        "entityCategory": "diagnostic",
        "name": "[Alarm] S07 Heater Overload",
        "icon": "mdi:heat-wave"
    },
    "Alarm detail": {
        "entityCategory": "diagnostic",
        "name": "[Alarm] Detail - Code",
        "icon": "mdi:alert-circle-outline"
    }
}

# Configuration registers specification (109 parameters)
CONFIG_REGISTERS: list[dict[str, Any]] = [
    {
        "reg": 1011,
        "key": "power_state",
        "name": "Power State",
        "component": "switch",
        "icon": "mdi:power",
        "block": 1
    },
    {
        "reg": 1012,
        "key": "operating_mode",
        "name": "Operating Mode",
        "component": "select",
        "options": [
            "Hot Water",
            "Heating",
            "Cooling",
            "Hot Water + Heating",
            "Hot Water + Cooling"
        ],
        "icon": "mdi:hvac",
        "block": 1
    },
    {
        "reg": 1192,
        "key": "heating_target_temp",
        "name": "Heating Setpoint",
        "component": "number",
        "devClass": "temperature",
        "unit": "°C",
        "scale": 0.1,
        "min": 20.0,
        "max": 50.0,
        "step": 0.5,
        "mode": "box",
        "icon": "mdi:radiator",
        "block": 3
    },
    {
        "reg": 1191,
        "key": "boiler_target_temp",
        "name": "Hot Water Setpoint",
        "component": "number",
        "devClass": "temperature",
        "unit": "°C",
        "scale": 0.1,
        "min": 40.0,
        "max": 65.0,
        "step": 0.5,
        "mode": "box",
        "icon": "mdi:water-boiler",
        "block": 3
    },
    {
        "reg": 1193,
        "key": "cooling_target_temp",
        "name": "Cooling Setpoint",
        "component": "number",
        "devClass": "temperature",
        "unit": "°C",
        "scale": 0.1,
        "min": 12.0,
        "max": 20.0,
        "step": 0.5,
        "mode": "box",
        "icon": "mdi:snowflake",
        "block": 3
    },
    {
        "reg": 1255,
        "key": "timer_1_enable",
        "name": "Timer 1 (ON) Enable",
        "component": "switch",
        "icon": "mdi:timer-play",
        "block": 3
    },
    {
        "reg": 1256,
        "key": "timer_1_hour",
        "name": "Timer 1 (ON) Hour",
        "component": "number",
        "unit": "h",
        "min": 0,
        "max": 23,
        "step": 1,
        "mode": "box",
        "icon": "mdi:clock-outline",
        "block": 3
    },
    {
        "reg": 1259,
        "key": "timer_1_minute",
        "name": "Timer 1 (ON) Minute",
        "component": "number",
        "unit": "min",
        "min": 0,
        "max": 59,
        "step": 1,
        "mode": "box",
        "icon": "mdi:clock-outline",
        "block": 3
    },
    {
        "reg": 1257,
        "key": "timer_2_enable",
        "name": "Timer 2 (OFF) Enable",
        "component": "switch",
        "icon": "mdi:timer-stop",
        "block": 3
    },
    {
        "reg": 1258,
        "key": "timer_2_hour",
        "name": "Timer 2 (OFF) Hour",
        "component": "number",
        "unit": "h",
        "min": 0,
        "max": 23,
        "step": 1,
        "mode": "box",
        "icon": "mdi:clock-outline",
        "block": 3
    },
    {
        "reg": 1260,
        "key": "timer_2_minute",
        "name": "Timer 2 (OFF) Minute",
        "component": "number",
        "unit": "min",
        "min": 0,
        "max": 59,
        "step": 1,
        "mode": "box",
        "icon": "mdi:clock-outline",
        "block": 3
    },
    {
        "reg": 1074,
        "key": "fast_mute",
        "name": "Fast Mute",
        "component": "switch",
        "icon": "mdi:volume-mute",
        "block": 1
    },
    {
        "reg": 1068,
        "key": "mute_timer_enable",
        "name": "Mute Timer Enable",
        "component": "switch",
        "icon": "mdi:timer-cog",
        "block": 1
    },
    {
        "reg": 1069,
        "key": "mute_start_hour",
        "name": "Mute Timer Start Hour",
        "component": "number",
        "unit": "h",
        "min": 0,
        "max": 23,
        "step": 1,
        "mode": "box",
        "icon": "mdi:clock-start",
        "block": 1
    },
    {
        "reg": 1261,
        "key": "mute_start_minute",
        "name": "Mute Timer Start Min",
        "component": "number",
        "unit": "min",
        "min": 0,
        "max": 59,
        "step": 1,
        "mode": "box",
        "icon": "mdi:clock-start",
        "block": 3
    },
    {
        "reg": 1070,
        "key": "mute_end_hour",
        "name": "Mute Timer End Hour",
        "component": "number",
        "unit": "h",
        "min": 0,
        "max": 23,
        "step": 1,
        "mode": "box",
        "icon": "mdi:clock-end",
        "block": 1
    },
    {
        "reg": 1262,
        "key": "mute_end_minute",
        "name": "Mute Timer End Min",
        "component": "number",
        "unit": "min",
        "min": 0,
        "max": 59,
        "step": 1,
        "mode": "box",
        "icon": "mdi:clock-end",
        "block": 3
    },
    {
        "reg": 1031,
        "key": "electric_heater",
        "name": "Electric Heater",
        "component": "switch",
        "icon": "mdi:patio-heater",
        "block": 1
    },
    {
        "reg": 1167,
        "key": "pump_running_mode",
        "name": "Pump Running Mode",
        "component": "select",
        "options": [
            "Ordinary",
            "Special",
            "Interval"
        ],
        "icon": "mdi:water-pump",
        "block": 2
    },
    {
        "reg": 1168,
        "key": "pump_running_interval",
        "name": "Pump Running Interval",
        "component": "number",
        "unit": "min",
        "min": 0,
        "max": 120,
        "step": 1,
        "mode": "slider",
        "icon": "mdi:timer-sand",
        "block": 2
    },
    {
        "reg": 1169,
        "key": "pump_running_duration",
        "name": "Pump Running Duration",
        "component": "number",
        "unit": "min",
        "min": 0,
        "max": 30,
        "step": 1,
        "mode": "slider",
        "icon": "mdi:timer-outline",
        "block": 2
    },
    {
        "reg": 1018,
        "key": "auto_start",
        "name": "[System] General - H01 Auto Start",
        "entityCategory": "config",
        "block": 1,
        "component": "switch",
        "icon": "mdi:toggle-switch"
    },
    {
        "reg": 1019,
        "key": "master_slave_unit",
        "name": "[System] Network - H02 Master/Slave Unit",
        "entityCategory": "config",
        "block": 1,
        "component": "select",
        "options": [
            "Master",
            "Slave"
        ],
        "icon": "mdi:form-dropdown"
    },
    {
        "reg": 1020,
        "key": "temperature_unit",
        "name": "[System] Unit - H03 Temperature Unit",
        "entityCategory": "config",
        "block": 1,
        "component": "select",
        "options": [
            "°C",
            "°F"
        ],
        "icon": "mdi:form-dropdown"
    },
    {
        "reg": 1021,
        "key": "4_way_valve_polarity",
        "name": "[System] Valve - H04 4-way Valve Polarity",
        "entityCategory": "config",
        "block": 1,
        "component": "select",
        "options": [
            "On-heating",
            "Off-heating"
        ],
        "icon": "mdi:form-dropdown"
    },
    {
        "reg": 1022,
        "key": "3_way_valve_polarity",
        "name": "[System] Valve - H05 3-way Valve Polarity",
        "entityCategory": "config",
        "block": 1,
        "component": "select",
        "options": [
            "On-heat water",
            "Off-heat water"
        ],
        "icon": "mdi:form-dropdown"
    },
    {
        "reg": 1023,
        "key": "frequency_control_p_value",
        "name": "[System] Inverter - H06 Frequency Control P Value",
        "entityCategory": "config",
        "block": 1,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "Hz",
        "devClass": "frequency",
        "icon": "mdi:sine-wave",
        "min": 1,
        "max": 100
    },
    {
        "reg": 1024,
        "key": "frequency_control_i_value",
        "name": "[System] Inverter - H07 Frequency Control I Value",
        "entityCategory": "config",
        "block": 1,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "Hz",
        "devClass": "frequency",
        "icon": "mdi:sine-wave",
        "min": 1,
        "max": 100
    },
    {
        "reg": 1025,
        "key": "frequency_control_d_value",
        "name": "[System] Inverter - H08 Frequency Control D Value",
        "entityCategory": "config",
        "block": 1,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "Hz",
        "devClass": "frequency",
        "icon": "mdi:sine-wave",
        "min": 0,
        "max": 100
    },
    {
        "reg": 1026,
        "key": "min_compressor_frequency",
        "name": "[System] Inverter - H09 Min Compressor Frequency",
        "entityCategory": "config",
        "block": 1,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "Hz",
        "devClass": "frequency",
        "icon": "mdi:sine-wave",
        "min": 20,
        "max": 60
    },
    {
        "reg": 1027,
        "key": "max_compressor_frequency",
        "name": "[System] Inverter - H10 Max Compressor Frequency",
        "entityCategory": "config",
        "block": 1,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "Hz",
        "devClass": "frequency",
        "icon": "mdi:sine-wave",
        "min": 30,
        "max": 120
    },
    {
        "reg": 1028,
        "key": "model_selection",
        "name": "[System] Model - H11 Model Selection",
        "entityCategory": "config",
        "block": 1,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "icon": "mdi:tune",
        "min": 0,
        "max": 50
    },
    {
        "reg": 1029,
        "key": "manual_drive_frequency",
        "name": "[System] Inverter - H12 Manual Drive Frequency",
        "entityCategory": "config",
        "block": 1,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "Hz",
        "devClass": "frequency",
        "icon": "mdi:sine-wave",
        "min": 0,
        "max": 90
    },
    {
        "reg": 1030,
        "key": "pfc_function_enable",
        "name": "[System] Inverter - H13 PFC Function Enable",
        "entityCategory": "config",
        "block": 1,
        "component": "switch",
        "icon": "mdi:toggle-switch"
    },
    {
        "reg": 1032,
        "key": "unit_address",
        "name": "[System] Network - H15 Unit Address",
        "entityCategory": "config",
        "block": 1,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "icon": "mdi:tune",
        "min": 1,
        "max": 247
    },
    {
        "reg": 1040,
        "key": "antifreeze_temp",
        "name": "[Protect] Antifreeze - A01 Antifreeze Temp",
        "entityCategory": "config",
        "block": 1,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:snowflake-thermometer",
        "min": -10.0,
        "max": 10.0
    },
    {
        "reg": 1041,
        "key": "antifreeze_low_pressure",
        "name": "[Protect] Antifreeze - A02 Antifreeze Low Pressure",
        "entityCategory": "config",
        "block": 1,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "bar",
        "devClass": "pressure",
        "icon": "mdi:gauge",
        "min": 0.0,
        "max": 10.0
    },
    {
        "reg": 1042,
        "key": "antifreeze_temp_difference",
        "name": "[Protect] Antifreeze - A03 Antifreeze Temp Difference",
        "entityCategory": "config",
        "block": 1,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:thermometer-lines",
        "min": 0.0,
        "max": 10.0
    },
    {
        "reg": 1043,
        "key": "shutdown_ambient_temp",
        "name": "[Protect] Limits - A04 Shutdown Ambient Temp",
        "entityCategory": "config",
        "block": 1,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:thermometer-low",
        "min": -30.0,
        "max": 10.0
    },
    {
        "reg": 1044,
        "key": "safe_discharge_temp",
        "name": "[Protect] Limits - A05 Safe Discharge Temp",
        "entityCategory": "config",
        "block": 1,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:thermometer-alert",
        "min": 80.0,
        "max": 130.0
    },
    {
        "reg": 1045,
        "key": "spray_valve_open_temp",
        "name": "[Protect] Valve - A06 Spray Valve Open Temp",
        "entityCategory": "config",
        "block": 1,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:spray",
        "min": 10.0,
        "max": 50.0
    },
    {
        "reg": 1059,
        "key": "max_speed_in_heating",
        "name": "[Fan] Heating - F01 Max Speed in Heating",
        "entityCategory": "config",
        "block": 1,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "rpm",
        "icon": "mdi:fan",
        "min": 0,
        "max": 2000
    },
    {
        "reg": 1060,
        "key": "min_speed_in_heating",
        "name": "[Fan] Heating - F02 Min Speed in Heating",
        "entityCategory": "config",
        "block": 1,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "rpm",
        "icon": "mdi:fan",
        "min": 0,
        "max": 2000
    },
    {
        "reg": 1061,
        "key": "suction_lp_for_heating",
        "name": "[Fan] Heating - F03 Suction LP for Heating",
        "entityCategory": "config",
        "block": 1,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "bar",
        "devClass": "pressure",
        "icon": "mdi:gauge",
        "min": 0.0,
        "max": 20.0
    },
    {
        "reg": 1062,
        "key": "suction_hp_for_heating",
        "name": "[Fan] Heating - F04 Suction HP for Heating",
        "entityCategory": "config",
        "block": 1,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "bar",
        "devClass": "pressure",
        "icon": "mdi:gauge",
        "min": 0.0,
        "max": 20.0
    },
    {
        "reg": 1063,
        "key": "max_speed_in_cooling",
        "name": "[Fan] Cooling - F05 Max Speed in Cooling",
        "entityCategory": "config",
        "block": 1,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "rpm",
        "icon": "mdi:fan",
        "min": 0,
        "max": 2000
    },
    {
        "reg": 1064,
        "key": "min_speed_in_cooling",
        "name": "[Fan] Cooling - F06 Min Speed in Cooling",
        "entityCategory": "config",
        "block": 1,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "rpm",
        "icon": "mdi:fan",
        "min": 0,
        "max": 2000
    },
    {
        "reg": 1065,
        "key": "discharge_hp_for_cooling",
        "name": "[Fan] Cooling - F07 Discharge HP for Cooling",
        "entityCategory": "config",
        "block": 1,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "bar",
        "devClass": "pressure",
        "icon": "mdi:gauge",
        "min": 0.0,
        "max": 50.0
    },
    {
        "reg": 1066,
        "key": "discharge_lp_for_cooling",
        "name": "[Fan] Cooling - F08 Discharge LP for Cooling",
        "entityCategory": "config",
        "block": 1,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "bar",
        "devClass": "pressure",
        "icon": "mdi:gauge",
        "min": 0.0,
        "max": 50.0
    },
    {
        "reg": 1067,
        "key": "manual_fan_speed",
        "name": "[Fan] Manual - F09 Manual Fan Speed",
        "entityCategory": "config",
        "block": 1,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "rpm",
        "icon": "mdi:fan",
        "min": 0,
        "max": 2000
    },
    {
        "reg": 1071,
        "key": "mute_mode_fan_speed",
        "name": "[Fan] Mute - F13 Mute Mode Fan Speed",
        "entityCategory": "config",
        "block": 1,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "rpm",
        "icon": "mdi:fan",
        "min": 300,
        "max": 1300
    },
    {
        "reg": 1072,
        "key": "dc_ec_fan_rated_speed",
        "name": "[Fan] Motor - F14 DC/EC Fan Rated Speed",
        "entityCategory": "config",
        "block": 1,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "rpm",
        "icon": "mdi:fan",
        "min": 0,
        "max": 1300
    },
    {
        "reg": 1073,
        "key": "fan_motor_type",
        "name": "[Fan] Motor - F15 Fan Motor Type",
        "entityCategory": "config",
        "block": 1,
        "component": "select",
        "options": [
            "AC",
            "DC",
            "2xDC"
        ],
        "icon": "mdi:form-dropdown"
    },
    {
        "reg": 1101,
        "key": "exit_defrost_temp",
        "name": "[Defrost] Exit - D01 Exit Defrost Temp",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:snowflake-melt",
        "min": 1.0,
        "max": 40.0
    },
    {
        "reg": 1102,
        "key": "exit_defrost_pressure",
        "name": "[Defrost] Exit - D02 Exit Defrost Pressure",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "bar",
        "devClass": "pressure",
        "icon": "mdi:gauge",
        "min": 1.0,
        "max": 25.0
    },
    {
        "reg": 1103,
        "key": "defrost_cycle",
        "name": "[Defrost] Cycle - D03 Defrost Cycle",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "min",
        "icon": "mdi:timer-sand",
        "min": 1,
        "max": 90
    },
    {
        "reg": 1104,
        "key": "max_defrost_time",
        "name": "[Defrost] Cycle - D04 Max Defrost Time",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "min",
        "icon": "mdi:timer-sand",
        "min": 1,
        "max": 20
    },
    {
        "reg": 1105,
        "key": "sliding_high_point_lp",
        "name": "[Defrost] Sliding - D05 Sliding High Point LP",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "bar",
        "devClass": "pressure",
        "icon": "mdi:gauge",
        "min": 1.0,
        "max": 20.0
    },
    {
        "reg": 1106,
        "key": "sliding_low_point_lp",
        "name": "[Defrost] Sliding - D06 Sliding Low Point LP",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "bar",
        "devClass": "pressure",
        "icon": "mdi:gauge",
        "min": 1.0,
        "max": 20.0
    },
    {
        "reg": 1107,
        "key": "sliding_high_point_of_at",
        "name": "[Defrost] Sliding - D07 Sliding High Point of AT",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:thermometer-chevron-up",
        "min": -10.0,
        "max": 10.0
    },
    {
        "reg": 1108,
        "key": "sliding_low_point_of_at",
        "name": "[Defrost] Sliding - D08 Sliding Low Point of AT",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:thermometer-chevron-down",
        "min": -30.0,
        "max": 10.0
    },
    {
        "reg": 1109,
        "key": "sliding_defrost",
        "name": "[Defrost] Sliding - D09 Sliding Defrost",
        "entityCategory": "config",
        "block": 2,
        "component": "switch",
        "icon": "mdi:toggle-switch"
    },
    {
        "reg": 1110,
        "key": "electric_heater_defrost",
        "name": "[Defrost] Heater - D10 Electric Heater Defrost",
        "entityCategory": "config",
        "block": 2,
        "component": "switch",
        "icon": "mdi:toggle-switch"
    },
    {
        "reg": 1111,
        "key": "defrost_frequency",
        "name": "[Defrost] Comp - D11 Defrost Frequency",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "Hz",
        "devClass": "frequency",
        "icon": "mdi:sine-wave",
        "min": 0,
        "max": 90
    },
    {
        "reg": 1127,
        "key": "adjustment_mode",
        "name": "[EEV] Mode - E01 Adjustment Mode",
        "entityCategory": "config",
        "block": 2,
        "component": "select",
        "options": [
            "Manual",
            "Auto"
        ],
        "icon": "mdi:form-dropdown"
    },
    {
        "reg": 1128,
        "key": "superheat_in_heating",
        "name": "[EEV] Heat - E02 Superheat in Heating",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:thermometer-lines",
        "min": -10.0,
        "max": 10.0
    },
    {
        "reg": 1129,
        "key": "superheat_comp_1_heat",
        "name": "[EEV] Heat - E03 Superheat Comp 1 Heat",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:thermometer-lines",
        "min": -10.0,
        "max": 10.0
    },
    {
        "reg": 1130,
        "key": "superheat_comp_2_heat",
        "name": "[EEV] Heat - E04 Superheat Comp 2 Heat",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:thermometer-lines",
        "min": -10.0,
        "max": 10.0
    },
    {
        "reg": 1131,
        "key": "initial_steps_in_heat",
        "name": "[EEV] Heat - E05 Initial Steps in Heat",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "steps",
        "icon": "mdi:valve",
        "min": 0,
        "max": 480
    },
    {
        "reg": 1132,
        "key": "initial_steps_comp_1",
        "name": "[EEV] Initial - E06 Initial Steps Comp 1",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "steps",
        "icon": "mdi:valve",
        "min": 0,
        "max": 200
    },
    {
        "reg": 1133,
        "key": "initial_steps_comp_2",
        "name": "[EEV] Initial - E07 Initial Steps Comp 2",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "steps",
        "icon": "mdi:valve",
        "min": 0,
        "max": 200
    },
    {
        "reg": 1134,
        "key": "initial_steps_comp_3",
        "name": "[EEV] Initial - E08 Initial Steps Comp 3",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "steps",
        "icon": "mdi:valve",
        "min": 0,
        "max": 200
    },
    {
        "reg": 1135,
        "key": "min_initial_steps",
        "name": "[EEV] Initial - E09 Min Initial Steps",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "steps",
        "icon": "mdi:valve",
        "min": 0,
        "max": 200
    },
    {
        "reg": 1136,
        "key": "defrost_steps",
        "name": "[EEV] Defrost - E10 Defrost Steps",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "steps",
        "icon": "mdi:valve",
        "min": 0,
        "max": 480
    },
    {
        "reg": 1137,
        "key": "superheat_in_cooling",
        "name": "[EEV] Cool - E11 Superheat in Cooling",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:thermometer-lines",
        "min": -10.0,
        "max": 10.0
    },
    {
        "reg": 1138,
        "key": "initial_steps_in_cool",
        "name": "[EEV] Cool - E12 Initial Steps in Cool",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "steps",
        "icon": "mdi:valve",
        "min": 0,
        "max": 480
    },
    {
        "reg": 1139,
        "key": "exhaust_assist_open_time",
        "name": "[EEV] Timing - E13 Exhaust Assist Open Time",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "min",
        "icon": "mdi:timer-sand",
        "min": 0,
        "max": 100
    },
    {
        "reg": 1140,
        "key": "suction_superheat_open_time",
        "name": "[EEV] Timing - E14 Suction Superheat Open Time",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "min",
        "icon": "mdi:timer-sand",
        "min": 0,
        "max": 100
    },
    {
        "reg": 1141,
        "key": "control_p_value",
        "name": "[EEV] PID - E15 Control P Value",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "icon": "mdi:tune",
        "min": 0,
        "max": 100
    },
    {
        "reg": 1142,
        "key": "control_i_value",
        "name": "[EEV] PID - E16 Control I Value",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "icon": "mdi:tune",
        "min": 0,
        "max": 100
    },
    {
        "reg": 1143,
        "key": "control_d_value",
        "name": "[EEV] PID - E17 Control D Value",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "icon": "mdi:tune",
        "min": 0,
        "max": 100
    },
    {
        "reg": 1144,
        "key": "manual_steps",
        "name": "[EEV] Manual - E18 Manual Steps",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "steps",
        "icon": "mdi:valve",
        "min": 0,
        "max": 550
    },
    {
        "reg": 1145,
        "key": "superheat_comp_1",
        "name": "[EEV] Cool - E19 Superheat Comp 1 (Cool)",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:thermometer-lines",
        "min": -10.0,
        "max": 10.0
    },
    {
        "reg": 1146,
        "key": "superheat_comp_2",
        "name": "[EEV] Cool - E20 Superheat Comp 2 (Cool)",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:thermometer-lines",
        "min": -10.0,
        "max": 10.0
    },
    {
        "reg": 1160,
        "key": "disinfection_setpoint",
        "name": "[Disinf] Target - G01 Disinfection Setpoint",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:water-thermometer",
        "min": 60.0,
        "max": 70.0
    },
    {
        "reg": 1161,
        "key": "time_of_duration",
        "name": "[Disinf] Schedule - G02 Time of Duration",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "min",
        "icon": "mdi:timer-sand",
        "min": 0,
        "max": 60
    },
    {
        "reg": 1162,
        "key": "start_time",
        "name": "[Disinf] Schedule - G03 Start Time",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "h",
        "icon": "mdi:clock-outline",
        "min": 0,
        "max": 23
    },
    {
        "reg": 1163,
        "key": "work_cycle",
        "name": "[Disinf] Schedule - G04 Work Cycle",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "Days",
        "icon": "mdi:calendar-range",
        "min": 1,
        "max": 30
    },
    {
        "reg": 1170,
        "key": "pump_advanced_start_time",
        "name": "[Pump] Timing - P04 Pump Advanced Start Time",
        "entityCategory": "config",
        "block": 2,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "min",
        "icon": "mdi:timer-sand",
        "min": 0,
        "max": 30
    },
    {
        "reg": 1171,
        "key": "pump_manual_control",
        "name": "[Pump] Manual - P05 Pump Manual-control",
        "entityCategory": "config",
        "block": 2,
        "component": "switch",
        "icon": "mdi:toggle-switch"
    },
    {
        "reg": 1194,
        "key": "power_on_return_diff",
        "name": "[Temp] Diff - R04 Power-on Return Diff",
        "entityCategory": "config",
        "block": 3,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:thermometer-lines",
        "min": 0.0,
        "max": 10.0
    },
    {
        "reg": 1195,
        "key": "standby_temp_diff",
        "name": "[Temp] Diff - R05 Standby Temp Diff",
        "entityCategory": "config",
        "block": 3,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:thermometer-lines",
        "min": 0.0,
        "max": 10.0
    },
    {
        "reg": 1196,
        "key": "min_hot_water_setpoint",
        "name": "[Temp] Limit - R06 Min Hot Water Setpoint",
        "entityCategory": "config",
        "block": 3,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:thermometer-chevron-down",
        "min": 40.0,
        "max": 65.0
    },
    {
        "reg": 1197,
        "key": "max_hot_water_setpoint",
        "name": "[Temp] Limit - R07 Max Hot Water Setpoint",
        "entityCategory": "config",
        "block": 3,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:thermometer-chevron-up",
        "min": 6.0,
        "max": 65.0
    },
    {
        "reg": 1198,
        "key": "min_heating_setpoint",
        "name": "[Temp] Limit - R08 Min Heating Setpoint",
        "entityCategory": "config",
        "block": 3,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:thermometer-chevron-down",
        "min": 20.0,
        "max": 30.0
    },
    {
        "reg": 1199,
        "key": "max_heating_setpoint",
        "name": "[Temp] Limit - R09 Max Heating Setpoint",
        "entityCategory": "config",
        "block": 3,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:thermometer-chevron-up",
        "min": 30.0,
        "max": 60.0
    },
    {
        "reg": 1200,
        "key": "min_cooling_setpoint",
        "name": "[Temp] Limit - R10 Min Cooling Setpoint",
        "entityCategory": "config",
        "block": 3,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:thermometer-chevron-down",
        "min": 8.0,
        "max": 20.0
    },
    {
        "reg": 1201,
        "key": "max_cooling_setpoint",
        "name": "[Temp] Limit - R11 Max Cooling Setpoint",
        "entityCategory": "config",
        "block": 3,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:thermometer-chevron-up",
        "min": 20.0,
        "max": 30.0
    },
    {
        "reg": 1202,
        "key": "electric_heating_mode",
        "name": "[Temp] Heater - R12 Electric Heating Mode",
        "entityCategory": "config",
        "block": 3,
        "component": "select",
        "options": [
            "Not used",
            "Waterline",
            "Water tank"
        ],
        "icon": "mdi:form-dropdown"
    },
    {
        "reg": 1203,
        "key": "electric_heater_start_diff",
        "name": "[Temp] Heater - R13 Electric-heater Start Diff",
        "entityCategory": "config",
        "block": 3,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:heating-coil",
        "min": 0.0,
        "max": 10.0
    },
    {
        "reg": 1204,
        "key": "electric_heater_start_at",
        "name": "[Temp] Heater - R14 Electric-heater Start AT",
        "entityCategory": "config",
        "block": 3,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:thermometer-low",
        "min": -10.0,
        "max": 30.0
    },
    {
        "reg": 1205,
        "key": "delay_of_electric_heater",
        "name": "[Temp] Heater - R15 Delay of Electric-heater",
        "entityCategory": "config",
        "block": 3,
        "component": "number",
        "mode": "box",
        "scale": 1,
        "step": 1,
        "unit": "min",
        "icon": "mdi:timer-sand",
        "min": 0,
        "max": 60
    },
    {
        "reg": 1206,
        "key": "electric_heater_instant_start_at",
        "name": "[Temp] Heater - R16 Electric-heater Instant Start AT",
        "entityCategory": "config",
        "block": 3,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:thermometer-alert",
        "min": -30.0,
        "max": 20.0
    },
    {
        "reg": 1207,
        "key": "compensation_on_low_at",
        "name": "[Temp] Curve - R17 Compensation-ON Low AT",
        "entityCategory": "config",
        "block": 3,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:weather-snowy",
        "min": 18.0,
        "max": 0.0
    },
    {
        "reg": 1208,
        "key": "compensation_off_low_at",
        "name": "[Temp] Curve - R18 Compensation-OFF Low AT",
        "entityCategory": "config",
        "block": 3,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:thermometer-low",
        "min": -30.0,
        "max": 60.0
    },
    {
        "reg": 1209,
        "key": "low_at_max_compensation_target",
        "name": "[Temp] Curve - R19 Low-AT Max-Compensation Target",
        "entityCategory": "config",
        "block": 3,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:chart-bell-curve",
        "min": 20.0,
        "max": 60.0
    },
    {
        "reg": 1210,
        "key": "compensation_on_high_at",
        "name": "[Temp] Curve - R20 Compensation-ON High AT",
        "entityCategory": "config",
        "block": 3,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:weather-sunny",
        "min": -30.0,
        "max": 60.0
    },
    {
        "reg": 1211,
        "key": "compensation_off_high_at",
        "name": "[Temp] Curve - R21 Compensation-OFF High AT",
        "entityCategory": "config",
        "block": 3,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:thermometer-high",
        "min": 20.0,
        "max": 60.0
    },
    {
        "reg": 1212,
        "key": "high_at_max_compensation_target",
        "name": "[Temp] Curve - R22 High-AT Max-Compensation Target",
        "entityCategory": "config",
        "block": 3,
        "component": "number",
        "mode": "box",
        "scale": 0.1,
        "step": 0.1,
        "unit": "°C",
        "devClass": "temperature",
        "icon": "mdi:chart-bell-curve",
        "min": 20.0,
        "max": 60.0
    }
]

# Lookup map by register number
CONFIG_REGISTERS_BY_REG: dict[int, dict[str, Any]] = {
    item["reg"]: item for item in CONFIG_REGISTERS
}

# Lookup map by key
CONFIG_REGISTERS_BY_KEY: dict[str, dict[str, Any]] = {
    item["key"]: item for item in CONFIG_REGISTERS
}
