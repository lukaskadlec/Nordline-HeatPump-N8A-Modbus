**Languages / Jazyky:** [English](README.md) | [Čeština](README.cz.md)

---

# Nordline Air-to-Water Heat Pump (N8A) - Modbus & Home Assistant Integration

Bidirectional monitoring, telemetry, and full configuration control integration for the **Nordline N8A Air-to-Water Heat Pump** (OEM model **PHNIX Hero H8A**, equipped with the **PC8002 PCB Controller** and **Slave 1 LCD Wall Unit**).

This project offers two implementation paths:
1. **Native Home Assistant Custom Integration (HACS) [Recommended]**: Direct local serial port connection (`/dev/ttyUSB*`), zero Node-RED or MQTT dependencies, UI Config Flow, 42 telemetry sensors, 21 primary controls, 88 configuration registers, built-in 10-second silence watchdog.
2. **Node-RED & MQTT Alternative**: Streamlined production flow ([`flows.json`](flows.json)) with all debugging and scratch file-logging removed, communicating via MQTT Discovery.

---

> [!WARNING]
> ### ⚠️ IMPORTANT WARNING: Heat Pump Lifespan & EEPROM Write Endurance
> **Recommended safe daily limit: maximum ~10 writes per day per parameter!**
> 
> The main microcontroller on the **PC8002 PCB** stores all configuration parameter changes (target heating, cooling, and hot water setpoints, operating modes, timers, and service registers) directly into non-volatile **EEPROM** memory. EEPROM chips have a physically finite endurance cycle (typically 100,000 to 1,000,000 write operations per cell before irreversible hardware failure occurs).
> 
> - **Hardware Protection**: Keeping parameter changes under **~10 writes/day per parameter** guarantees decades of safe operational lifespan.
> - **Warning for Automations**: **Never create high-frequency automation loops** in Home Assistant (e.g., dynamically updating target temperatures every minute based on spot electricity prices, minor room thermostat fluctuations, or outdoor temperature drift).
> - **Best Practices**: Use hysteresis, batch parameter adjustments, and alter setpoints only during major schedule shifts (e.g., eco/comfort transitions 2–4 times a day).

---

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Hardware Requirements](#hardware-requirements)
3. [Hardware Compatibility & OEM Rebadges](#hardware-compatibility--oem-rebadges)
4. [Wiring & Custom Power Switch](#wiring--custom-power-switch)
5. [Method A: Native HACS Integration (Recommended)](#method-a-native-hacs-integration-recommended)
6. [Method B: Node-RED & MQTT Alternative](#method-b-node-red--mqtt-alternative)
7. [Serial Port Settings](#serial-port-settings)
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
+-----------------------+    |  2-Wire  |                  |
| Heat Pump Master Board|----+-- Bus ---+                  v
| (PC8002 PCB)          |                    +---------------------------+
+-----------------------+                    |  Home Assistant           |
                                             |  - HACS Integration (Direct)|
                                             |  OR Node-RED -> MQTT      |
                                             +---------------------------+

```

1. **Master Controller (PC8002 PCB)** cyclically broadcasts status frames (`00, 16, 07` and `00, 16, 08`) and polls the LCD display (`01, 03, 0B, B9, 00, 15`) every second.
2. **Direct Serial Access**: The host connects to the bus via an isolated USB-to-RS485 transceiver.
3. **Passive Sniffing**: While the physical LCD is active, Home Assistant or Node-RED passively reads live telemetry frames.
4. **Coexistence & Watchdog (10s)**: When the physical LCD is disconnected or turned off via the rocker power switch for >10 seconds, the LCD Emulator seamlessly answers Master polls and synchronizes settings adjustments from Home Assistant.

---

## Hardware Requirements

To replicate this setup, you need:
1. **Nordline N8A Heat Pump** (or compatible unit using PC8002 PCB controller — see [Hardware Compatibility & OEM Rebadges](#hardware-compatibility--oem-rebadges)).
2. **USB-to-RS485 Adapter**:
   - An isolated FTDI, CH340, or CP2102-based USB-to-RS485 transceiver is recommended to protect your host from ground loops and electrical noise.
3. **Shielded Twisted Pair Cable**:
   - 2-wire or 3-wire cable connecting `A (Data+)`, `B (Data-)`, and `G (GND)` on the RS-485 bus.
4. **Custom Rocker Power Switch (Optional but Recommended)**:
   - A sub-miniature toggle or rocker switch installed on the wall LCD unit's housing to break the `V (VCC)` power line.
   - Allows switching between the physical wall display and software emulation on demand.
5. **Home Assistant Host**:
   - Home Assistant OS / Supervised on Raspberry Pi, Intel NUC, Home Assistant Yellow/Green, or Linux VM.

---

## Hardware Compatibility & OEM Rebadges

The **NORDline N8A** is based on the **PHNIX Hero Series**, specifically the OEM model designation **H8A** (also listed in some catalogs simply as **H8**), manufactured by **Guangdong PHNIX Eco-Energy Solution Ltd.**

### Other Commercial Rebadges of the H8A
Because PHNIX acts as an ODM/OEM supplier globally, the identical platform was distributed under various brand names:
- **ECON / Clima Control** (Southern Europe): Sold directly as the **ECON Hero H8A**.
- **EvoHeat** (Australia/Oceania): Sold under the **Evo Flex** inverter series.
- **Automatic Heating** (International): Marketed under the **AHGR410AW** monobloc inverter series.

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

To cleanly switch between physical control and automation, a red rocker power switch was wired in-line with terminal **V**:

![Custom Power Switch](assets/custom_power_switch.JPEG)

- **Switch ON**: The physical LCD powers on and responds to Master queries. Software emulation is automatically disabled, operating in passive sniffing mode.
- **Switch OFF**: The physical LCD is depowered. After 10 seconds of silence, the 10-second watchdog expires, and software emulation automatically takes over answering Master queries and processing Home Assistant commands.

---

## Method A: Native HACS Integration (Recommended)

The native custom component (`custom_components/nordline_heatpump`) connects directly to the USB serial adapter without requiring Node-RED or an MQTT broker.

### Features:
- **All 109 Registers & 42 Telemetry Sensors**: Automatically creates entities for all parameters.
- **Built-in 10-Second Watchdog**: Auto-detects physical LCD silence and seamlessly takes over.
- **Daily EEPROM Writes Tracking**: Real-time diagnostic sensor monitoring non-volatile memory write operations.

### Installation via HACS (Recommended):
1. In Home Assistant, open **HACS** -> **Integrations**.
2. Click the three dots (⋮) in the top right corner and select **Custom repositories**.
3. Fill in the repository details:
   - **Repository**: `https://github.com/lukaskadlec/Nordline-HeatPump-N8A-Modbus`
   - **Type / Category**: `Integration`
4. Click **Add**.
5. Find **Nordline Heat Pump N8A Modbus** in HACS and click **Download**.
6. Restart Home Assistant.
7. Go to **Settings** -> **Devices & Services** -> **Add Integration**.
8. Search for **Nordline Heat Pump N8A Modbus**.
9. Select your serial port (e.g. `/dev/ttyUSB-TC` or `/dev/serial/by-id/...`) and baud rate (`9600`), then click **Submit**.
10. The heat pump device will appear immediately with all sensors, controls, and configuration switches!

### Manual Installation (Alternative):
1. Copy the `custom_components/nordline_heatpump` directory into your Home Assistant `/config/custom_components/` folder:
   ```bash
   cp -r custom_components/nordline_heatpump /config/custom_components/
   ```
2. Restart Home Assistant and follow steps 7–10 above.

### Docker Configuration (Home Assistant Container):
If you are running Home Assistant Container (Docker / Docker Compose), configure your `docker-compose.yml` to grant access to the USB serial adapter and enable hardware auto-discovery:

```yaml
services:
  homeassistant:
    image: ghcr.io/home-assistant/home-assistant:stable
    # ...
    volumes:
      # ...
      - /dev:/dev             # Exposes device nodes for hot-plugging
      - /run/udev:/run/udev:ro # Enables Home Assistant hardware auto-discovery
    device_cgroup_rules:
      - 'c 188:* rmw'         # USB-to-serial (/dev/ttyUSB*)
      - 'c 166:* rmw'         # CDC-ACM devices (/dev/ttyACM*)
    group_add:
      - "20"                  # Debian/Ubuntu dialout group
```

> [!TIP]
> This configuration allows Home Assistant to detect and communicate with `/dev/ttyUSB*` devices dynamically without running the container in insecure `privileged` mode, retaining device permissions even across hot-plugging or host reboots.

---

## Method B: Node-RED & MQTT Alternative

For setups already running Node-RED, a streamlined production flow (`flows.json`) is provided with all debugging and scratch file-logging removed.

### Prerequisites:
1. **Home Assistant**: with native **MQTT Integration** enabled.
2. **Mosquitto Broker**: installed and running.
3. **Node-RED**: with palette packages `node-red-contrib-buffer-parser` and `node-red-node-serialport`.

### Setup:
1. In Node-RED, open the top-right hamburger menu -> **Import**.
2. Select and import [`flows.json`](flows.json).
3. Configure the `mqtt` broker node with your server IP and credentials.
4. Verify the serial port path in `/dev/ttyUSB-TC`.
5. Click **Deploy**. Telemetry and MQTT Discovery payloads will be transmitted automatically.

![Node-RED Flow Screenshot](assets/Node_Red_screen.png)

---

## Serial Port Settings

The RS-485 bus operates with the following physical serial parameters (configured in the HACS setup dialog or the Node-RED `serial-port` node):

| Parameter | Value | Description |
|:---|:---|:---|
| **Serial Port** | `/dev/ttyUSB-TC` *(or `/dev/serial/by-id/...`)* | Linux device node or persistent symlink |
| **Baud Rate** | `9600` | Heat pump Modbus RTU communication rate |
| **Data Bits** | `8` | Standard Modbus RTU framing |
| **Parity** | `None` | No parity |
| **Stop Bits** | `1` | 1 stop bit |
| **Flow Control** | DTR: auto, RTS: auto, CTS: auto, DSR: auto | No hardware handshaking |
| **Split Input / Timeout** | After a silence of **`40 ms`** | Guarantees complete Modbus frame delivery |
| **Delivery Mode** | `binary buffers` | Raw binary Buffer objects |
| **Response Timeout** | `1000 ms` | 1-second timeout |

![Serial Port Settings](assets/serial_port_setting.png)

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
  - `Fast Mute (8h)`, `Mute Timer Enable / Start / End`
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
  - `[Output]`: Digital Relays (1) .. (13)
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
4. **Configuration Register Write Limits & EEPROM Protection**:
   > [!WARNING]
   > **Recommended daily ceiling: maximum ~10 writes per day per parameter**
   > 
   > The PC8002 PCB microcontroller writes all settings changes directly to internal non-volatile **EEPROM**. Because EEPROM cells endure a limited number of write cycles (typically 100,000 to 1,000,000 writes per memory cell):
   > 
   > - **Lifespan Protection**: Restricting daily adjustments to approximately 10 writes per parameter ensures decades of reliable hardware service.
   > - **Automation Caution**: Do not bind heat pump setpoints directly to real-time spot electricity price feeds or aggressive PID controllers that push changes every few seconds or minutes.
   > - **Recommended Usage**: Utilize built-in schedules, apply temperature hysteresis, and group setting updates into daily mode transitions (e.g., night setback vs daytime comfort 2–4 times a day).

---

## Reference Documentation

- [`heatpump_configuration_registers.txt`](heatpump_configuration_registers.txt) / [Česká verze (`heatpump_configuration_registers.cz.txt`)](heatpump_configuration_registers.cz.txt): Complete 270-register engineering map, parameter ranges, scalings, and manufacturer codes.
- [`heatpump_rs485_protocol_spec.txt`](heatpump_rs485_protocol_spec.txt) / [Česká verze (`heatpump_rs485_protocol_spec.cz.txt`)](heatpump_rs485_protocol_spec.cz.txt): In-depth Modbus protocol reverse-engineering specification, frame timings, and state machines.
- [`Nordline_N8A_Manual.pdf`](doc/Nordline_N8A_Manual.pdf): Official manufacturer manual for PC8002 PCB controller and hardware wiring diagrams.