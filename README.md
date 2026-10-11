**Languages / Jazyky:** [English](README.md) | [Čeština](README.cz.md)

---

# Nordline Air-to-Water Heat Pump (N8A) - Modbus & Home Assistant Integration

Bidirectional monitoring, telemetry, and full configuration control integration for the **Nordline N8A Air-to-Water Heat Pump** (equipped with the **PC8002 PCB Controller** and **Slave 1 LCD Wall Unit**).

This project integrates the heat pump with **Home Assistant** via **RS-485 Modbus RTU**, **Node-RED**, and **MQTT**, featuring:
- **Live Telemetry & Diagnostics**: 42 status sensors (temperatures, refrigerant pressures, compressor inverter frequency, electrical parameters, EEV position, fan speed, relay outputs, and alarms).
- **Full Configuration & Control**: 109 registers (21 primary dashboard controls such as heating/DHW setpoints, operational modes, scheduled mute timers, and pump modes + 88 advanced engineering parameters).
- **Coexistence & Dynamic Failover (10-Second Watchdog)**: Smart arbitration between the physical wall LCD unit and Node-RED's LCD emulator to prevent RS-485 bus packet collisions.
- **Automatic Home Assistant MQTT Discovery**: Instantly auto-creates all devices, controls, numbers, switches, selects, and telemetry sensors with structured grouping.

---

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Hardware Requirements](#hardware-requirements)
3. [Wiring & Custom Power Switch](#wiring--custom-power-switch)
4. [Software & Prerequisites](#software--prerequisites)
5. [Node-RED Plugins & Nodes](#node-red-plugins--nodes)
6. [Serial Port Settings](#serial-port-settings)
7. [Installation & Setup](#installation--setup)
8. [Home Assistant Integration & UI](#home-assistant-integration--ui)
9. [Safety & Fail-Safe Mechanisms](#safety--fail-safe-mechanisms)
10. [Reference Documentation](#reference-documentation)

---

## System Architecture

```text
+-----------------------+                    +---------------------------+
| Physical LCD Wall Unit|                    | USB-to-RS485 Dongle       |
| (Slave ID 1)          |<---+          +--->| (e.g. /dev/ttyUSB-TC)     |
+-----------------------+    |          |    +---------------------------+
                             |  RS-485  |                  |
+-----------------------+    |  2-Wire  |                  v
| Heat Pump Master Board|----+-- Bus ---+            +------------+
| (PC8002 PCB)          |                            |  Node-RED  |
+-----------------------+                            +------------+
                                                           |  MQTT
                                                           v
                                                     +------------+
                                                     | Home Asst. |
                                                     +------------+
```

1. **Master Controller (PC8002 PCB)** cyclically broadcasts status frames (`00, 16, 07` and `00, 16, 08`) and polls the LCD display (`01, 03, 0B, B9, 00, 15`) every second.
2. **Node-RED** connects to the bus via an isolated USB-to-RS485 transceiver.
3. When the physical LCD is active, Node-RED sniffs all frames passively (read-only telemetry).
4. When the physical LCD is disconnected or turned off via the custom power switch for >10 seconds, Node-RED's LCD Emulator takes over answering polls and synchronizing parameter adjustments from Home Assistant.
5. All telemetry metrics and configuration states are published over **MQTT** with Home Assistant auto-discovery.

---

## Hardware Requirements

To replicate this setup, you need:
1. **Nordline N8A Heat Pump** (or compatible unit using PC8002 PCB controller).
2. **USB-to-RS485 Adapter**:
   - An isolated FTDI, CH340, or CP2102-based USB-to-RS485 transceiver is recommended to protect your host from ground loops and electrical noise.
3. **Shielded Twisted Pair Cable**:
   - 2-wire or 3-wire cable connecting `A (Data+)`, `B (Data-)`, and `G (GND)` on the RS-485 bus.
4. **Custom Rocker Power Switch (Optional but Recommended)**:
   - A sub-miniature toggle or rocker switch installed on the wall LCD unit's housing to break the `V (VCC)` power line.
   - Allows switching between the physical wall display and the Node-RED emulator on demand.
5. **Home Server / SBC**:
   - Raspberry Pi, Intel NUC, Home Assistant Yellow/Green, or Linux VM running Home Assistant, an MQTT broker (Mosquitto), and Node-RED.

---

## Wiring & Custom Power Switch

### 1. Terminal Block Connections
Inside the LCD wall controller, you will find a 6-position terminal block:

| Terminal Pin | Function | Wiring Connection |
|:------------:|:---------|:-------------------|
| **G** | Ground (GND) | Shared ground with RS-485 adapter / heat pump |
| **B** | RS-485 Data - | Connected to RS-485 **B / D-** line |
| **A** | RS-485 Data + | Connected to RS-485 **A / D+** line |
| **T** | TX (Internal) | Unconnected |
| **R** | RX (Internal) | Unconnected |
| **V** | Power (+12V/+24V) | Connected through the **Custom Power Switch** |

![Cable Connection](assets/cable_connection.JPEG)

### 2. Custom Power Switch Installation
Because RS-485 is a single-master shared bus, having two devices respond to Slave 1 queries simultaneously causes electrical collisions and framing errors.

To cleanly switch between physical control and Node-RED automation, a red rocker power switch was wired in-line with terminal **V**:

![Custom Power Switch](assets/custom_power_switch.JPEG)

- **Switch ON**: The physical LCD powers on and responds to Master queries. Node-RED automatically detects `01, 03, 42 Display Reply` packets and disables its internal emulator, operating in passive sniffing mode.
- **Switch OFF**: The physical LCD is depowered. After 10 seconds of silence, Node-RED's 10-second watchdog expires, and Node-RED's LCD Emulator automatically takes over answering Master queries and processing Home Assistant commands.

---

## Software & Prerequisites

1. **Home Assistant**: Core 2023.x or newer with the native **MQTT Integration** enabled.
2. **MQTT Broker**: **Mosquitto Broker** (add-on in Home Assistant OS or standalone container).
3. **Node-RED**: Version 2.x, 3.x, or 4.x running as a Home Assistant add-on or Docker container.

---

## Node-RED Plugins & Nodes

The provided flow (`flows.json`) requires the following palette node packages:

### Required Packages:
1. **`node-red-contrib-buffer-parser`**:
   - Parses complex binary Modbus frames into numbers, booleans, and bitfields.
2. **`node-red-node-serialport`**:
   - Interfaces directly with the USB-RS485 adapter on Linux or Windows.

### Installation via Node-RED Palette Manager:
1. Open Node-RED menu -> **Manage palette** -> **Install** tab.
2. Search for and install:
   - `node-red-contrib-buffer-parser`
   - `node-red-node-serialport`

*(All other nodes—`mqtt in`, `mqtt out`, `function`, `delay`, `file`, `inject`, and `debug`—are built into Node-RED core).*

---

## Serial Port Settings

Configure the `serial-port` configuration node in Node-RED with the following parameters:

| Property | Value | Description |
|:---|:---|:---|
| **Serial Port** | `/dev/ttyUSB-TC` *(or your port path / COM port)* | Linux device path or symlink |
| **Baud Rate** | `9600` | Heat pump Modbus baud rate |
| **Data Bits** | `8` | Standard Modbus RTU |
| **Parity** | `None` | No parity bit |
| **Stop Bits** | `1` | 1 stop bit |
| **Flow Control** | DTR: auto, RTS: auto, CTS: auto, DSR: auto | No hardware handshaking |
| **Split Input** | After a silence of **`40 ms`** | Delivers complete frames |
| **Deliver** | `binary buffers` | Raw binary Buffer objects |
| **Response Timeout** | `1000 ms` | 1 second default timeout |

![Serial Port Configuration](assets/serial_port_setting.png)

---

## Installation & Setup

1. **Import the Flow**:
   - In Node-RED, open the top-right hamburger menu -> **Import**.
   - Select and import [`flows.json`](flows.json).
2. **Configure MQTT Broker Node**:
   - Double-click the `mqtt` broker configuration node.
   - Set the server IP (e.g. `127.0.0.1` or Home Assistant IP), port `1883`, and MQTT credentials.
3. **Configure Serial Port**:
   - Double-click the `/dev/ttyUSB-TC` node and verify your serial port path.
4. **Deploy**:
   - Click **Deploy** in Node-RED.
   - At startup, the flow runs an automatic 10-second silence grace period, initializes telemetry, and transmits MQTT discovery payloads to Home Assistant.

![Node-RED Flow Screenshot](assets/Node_Red_screen.png)

---

## Home Assistant Integration & UI

Once deployed, the `Create HA mqtt device` node publishes MQTT Discovery messages under `homeassistant/#`. The heat pump appears as a single unified device named **Heat Pump**:

![Home Assistant UI Screenshot](assets/HA_screen.png)

### Logical Sorting & Taxonomy:
Entities are structured so they sort logically on Home Assistant device cards:
- **Controls (21 Primary Controls)**: Clean friendly names for quick interaction:
  - `Power State` (`switch.hp_power_state`)
  - `Operating Mode` (`select.hp_operating_mode`)
  - `Heating Setpoint`, `Hot Water Setpoint`, `Cooling Setpoint`
  - `Fast Mute`, `Mute Timer Enable / Start / End`
  - `Electric Heater`, `Daily Timer 1 & 2 Schedules`
  - `Pump Running Mode / Interval / Duration`
- **Configuration (88 Advanced Registers)**: Grouped with category prefixes:
  - `[System]`, `[Protect]`, `[Fan]`, `[Defrost]`, `[EEV]`, `[Disinf]`, `[Pump]`, `[Temp]`
- **Sensors & Diagnostics (42 Live Telemetry Sensors)**:
  - `[Temp]`: Water (Inlet, Outlet, Boiler), Refrigerant (Suction, Discharge, Evaporator, Superheats), System (Ambient, Inverter, Module Protection)
  - `[Pressure]`: Suction LP Transducer, Discharge HP Transducer
  - `[Electrical]`: AC Voltage, Current, DC Bus Voltage, Compressor Phase Current
  - `[Fan]`: Fan Speed, Fan Speed Set
  - `[EEV]`: Electronic Expansion Valve Steps
  - `[System]`: Freq Set, Freq Actual, Power ON/OFF, Status
  - `[Output]`: Digital Relays O01 .. O13
  - `[Alarm]`: S01 .. S07 Safety Switches & Active Numerical Alarm Code

---

## Safety & Fail-Safe Mechanisms

1. **Dual-Guard 10-Second LCD Silence Watchdog**:
   - **Immediate Disable**: Any incoming `01, 03, 42 Display Reply` packet from the physical LCD instantly disables emulation (`flow.set("lcd_emulator_enabled", false)`).
   - **10s Silence Trigger**: Node-RED's LCD emulator only answers Master periodic polls when no physical LCD reply has been detected for at least 10 seconds.
   - **Reconnection Protection**: If the physical switch is toggled ON, the first packet immediately halts Node-RED's emulator to prevent electrical collisions.
2. **Flag 128 (0x8000) Startup Full-Sync Guard**:
   - When Node-RED starts up or assumes emulation, it queues Flag 128 to request all 270 configuration registers from the Master board.
   - Bidirectional writes from Home Assistant are **blocked** until all registers are populated in memory, preventing accidental overwrite of parameters with zeroed defaults.
3. **Checksum & Framing Validation**:
   - Every received frame is verified with Modbus CRC-16 before decoding or routing.

---

## Reference Documentation

- [`heatpump_configuration_registers.txt`](heatpump_configuration_registers.txt) / [Česká verze (`heatpump_configuration_registers.cz.txt`)](heatpump_configuration_registers.cz.txt): Complete 270-register engineering map, parameter ranges, scalings, and manufacturer codes.
- [`heatpump_rs485_protocol_spec.txt`](heatpump_rs485_protocol_spec.txt) / [Česká verze (`heatpump_rs485_protocol_spec.cz.txt`)](heatpump_rs485_protocol_spec.cz.txt): In-depth Modbus protocol reverse-engineering specification, frame timings, and state machines.
- [`Nordline_N8A_Manual.pdf`](Nordline_N8A_Manual.pdf): Official manufacturer manual for PC8002 PCB controller and hardware wiring diagrams.