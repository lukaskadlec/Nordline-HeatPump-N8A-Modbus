"""Core RS-485 Modbus RTU communication hub for Nordline Heat Pump N8A."""

from __future__ import annotations

import asyncio
from datetime import datetime, date
import logging
import struct
import time
from typing import Any, Callable

from .const import (
    CONFIG_REGISTERS,
    CONFIG_REGISTERS_BY_KEY,
    CONFIG_REGISTERS_BY_REG,
    DOMAIN,
    TELEMETRY_DECODER_ITEMS,
    TELEMETRY_SENSORS_META,
)

_LOGGER = logging.getLogger(__name__)


def calculate_crc16(data: bytes | bytearray) -> int:
    """Calculate Modbus RTU CRC-16 (Polynomial 0xA001, Init 0xFFFF)."""
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc


def verify_crc16(frame: bytes | bytearray) -> bool:
    """Verify Modbus RTU CRC-16 of a frame."""
    if len(frame) < 3:
        return False
    expected = calculate_crc16(frame[:-2])
    actual = frame[-2] | (frame[-1] << 8)
    return expected == actual


def append_crc16(frame: bytearray) -> bytes:
    """Calculate and append 2-byte CRC16 (Low byte, High byte)."""
    crc = calculate_crc16(frame)
    frame.append(crc & 0xFF)
    frame.append((crc >> 8) & 0xFF)
    return bytes(frame)


class NordlineHeatPumpHub:
    """Handles RS-485 Modbus serial communication, passive sniffing, and LCD emulation."""

    def __init__(self, hass, serial_port: str, baudrate: int = 9600) -> None:
        """Initialize the hub."""
        self.hass = hass
        self.serial_port = serial_port
        self.baudrate = baudrate

        # Telemetry & Config State
        self.telemetry_data: dict[str, Any] = {}
        self.config_data: dict[str, Any] = {}
        self.config_raw: dict[int, int] = {}

        # 90-register data blocks (180 bytes each)
        self.config_block1 = bytearray(180)
        self.config_block2 = bytearray(180)
        self.config_block3 = bytearray(180)

        # Operational state flags
        self.config_initialized = False
        self.lcd_emulator_enabled = False
        self.last_lcd_reply_time = time.time()  # Start with 10s grace period
        self.pending_event_flag = 0x8000  # Queue Flag 128 on startup

        # Diagnostic: EEPROM daily write endurance counter
        self.daily_write_count = 0
        self.daily_write_date = date.today().isoformat()

        # Callbacks & async tasks
        self._callbacks: set[Callable[[], None]] = set()
        self._running = False
        self._loop_task: asyncio.Task | None = None
        self._transport = None
        self._protocol = None

        # Writer reference for serial output
        self._writer: asyncio.StreamWriter | None = None

    @property
    def is_connected(self) -> bool:
        """Return True if serial communication is active."""
        return self._running and self._writer is not None

    def register_callback(self, callback: Callable[[], None]) -> Callable[[], None]:
        """Register a callback to be called when data updates."""
        self._callbacks.add(callback)

        def remove_callback():
            self._callbacks.discard(callback)

        return remove_callback

    def _notify_callbacks(self) -> None:
        """Notify all registered entity callbacks in the event loop."""
        for callback in list(self._callbacks):
            try:
                callback()
            except Exception as err:
                _LOGGER.error("Error in entity update callback: %s", err)

    async def async_start(self) -> None:
        """Start the background serial communication loop."""
        self._running = True
        self._loop_task = asyncio.create_task(self._serial_worker())

    async def async_stop(self) -> None:
        """Stop serial communication and close port."""
        self._running = False
        if self._writer:
            try:
                self._writer.close()
                await self._writer.wait_closed()
            except Exception:
                pass
            self._writer = None

        if self._loop_task and not self._loop_task.done():
            self._loop_task.cancel()
            try:
                await self._loop_task
            except asyncio.CancelledError:
                pass

    async def _serial_worker(self) -> None:
        """Asynchronous serial connection loop with auto-reconnect."""
        while self._running:
            try:
                _LOGGER.info("Opening serial port %s at %d baud...", self.serial_port, self.baudrate)

                # Attempt using serial_asyncio_fast, fallback to serial_asyncio
                try:
                    import serial_asyncio_fast as serial_asyncio
                except ImportError:
                    import serial_asyncio

                reader, writer = await serial_asyncio.open_serial_connection(
                    url=self.serial_port,
                    baudrate=self.baudrate,
                    bytesize=8,
                    parity='N',
                    stopbits=1,
                    timeout=0.04  # 40ms silence detection
                )
                self._writer = writer
                _LOGGER.info("Serial connection established successfully on %s", self.serial_port)
                self._notify_callbacks()

                # Reset 10s grace period on connection
                self.last_lcd_reply_time = time.time()
                self.lcd_emulator_enabled = False

                buffer = bytearray()
                while self._running:
                    # Read incoming data chunks
                    try:
                        chunk = await asyncio.wait_for(reader.read(1024), timeout=0.04)
                        if chunk:
                            buffer.extend(chunk)
                    except asyncio.TimeoutError:
                        # 40ms inter-frame silence detected: process frame if buffer has content
                        if len(buffer) >= 4:
                            self._process_frame(bytes(buffer))
                        buffer.clear()
                    except Exception as err:
                        _LOGGER.warning("Serial read error: %s", err)
                        break

            except asyncio.CancelledError:
                break
            except Exception as err:
                _LOGGER.error("Failed to connect or maintain serial connection on %s: %s. Reconnecting in 5s...", self.serial_port, err)
                await asyncio.sleep(5)
            finally:
                if self._writer:
                    try:
                        self._writer.close()
                    except Exception:
                        pass
                    self._writer = None
                    self._notify_callbacks()

    def _process_frame(self, frame: bytes) -> None:
        """Process and route received Modbus RTU frames with stream-slicing fallback."""
        if verify_crc16(frame):
            self._route_frame(frame)
            return

        # Slicer fallback: scan for valid CRC frames in buffer (handles noise or concatenated frames)
        if len(frame) >= 5:
            offset = 0
            while offset <= len(frame) - 5:
                matched = False
                for length in (189, 47, 8, 11, 5):
                    if offset + length <= len(frame):
                        candidate = frame[offset:offset + length]
                        if verify_crc16(candidate):
                            self._route_frame(candidate)
                            offset += length
                            matched = True
                            break
                if not matched:
                    offset += 1

    def _route_frame(self, frame: bytes) -> None:
        """Route verified Modbus frame by header and length."""
        # 1. Master Broadcast Part A (00 16 07 D1 ... 180 bytes telemetry)
        if len(frame) == 189 and frame[0] == 0x00 and frame[1] == 0x10 and frame[2] == 0x07 and frame[3] == 0xD1:
            self._decode_telemetry_part_a(frame)
            return

        # 2. Master Broadcast Part B (00 16 08 2B)
        if frame[0] == 0x00 and frame[1] == 0x10 and frame[2] == 0x08:
            return

        # 3. Physical LCD Display Reply (01 03 2A ...)
        if frame[0] == 0x01 and frame[1] == 0x03 and frame[2] == 0x2A and len(frame) == 47:
            self.last_lcd_reply_time = time.time()
            if self.lcd_emulator_enabled:
                _LOGGER.info("Physical LCD traffic detected! Disabling internal LCD emulator immediately.")
                self.lcd_emulator_enabled = False
            return

        # 4. Master Periodic Poll for LCD Display (01 03 0B B9 00 15 57 C4)
        if len(frame) == 8 and frame[:6] == b"\x01\x03\x0B\xB9\x00\x15":
            self._handle_master_lcd_poll()
            return

        # 5. Master Write Block 1 Request (01 10 03 E9 00 5A B4 ...)
        if len(frame) >= 189 and frame[:6] == b"\x01\x10\x03\xE9\x00\x5A":
            self._handle_master_write_block(1, 1001, frame[7:187])
            return

        # 6. Master Write Block 2 Request (01 10 04 43 00 5A B4 ...)
        if len(frame) >= 189 and frame[:6] == b"\x01\x10\x04\x43\x00\x5A":
            self._handle_master_write_block(2, 1091, frame[7:187])
            return

        # 7. Master Write Block 3 Request (01 10 04 9D 00 5A B4 ...)
        if len(frame) >= 189 and frame[:6] == b"\x01\x10\x04\x9D\x00\x5A":
            self._handle_master_write_block(3, 1181, frame[7:187])
            return

        # 8. Master Clear Reg 3011 Request (01 10 0B C3 00 01 02 00 00 ...)
        if len(frame) >= 11 and frame[:7] == b"\x01\x10\x0B\xC3\x00\x01\x02":
            self._handle_master_clear_reg3011()
            return

        # 9. Master Read Block Request (FC 03 Read 90 regs)
        if len(frame) == 8 and frame[0] == 0x01 and frame[1] == 0x03 and frame[4] == 0x00 and frame[5] == 0x5A:
            start_reg = (frame[2] << 8) | frame[3]
            self._handle_master_read_block(start_reg)
            return

    def _decode_telemetry_part_a(self, frame: bytes) -> None:
        """Decode live operational metrics from Master Broadcast Part A."""
        updated = False

        for item in TELEMETRY_DECODER_ITEMS:
            name = item["name"]
            offset = item["offset"]
            itype = item["type"]
            scale = item.get("scale", "")

            try:
                if itype == "int16be":
                    val = struct.unpack_from(">h", frame, offset)[0]
                    if scale == "/10":
                        val = round(val / 10.0, 1)
                elif itype == "uint16be":
                    val = struct.unpack_from(">H", frame, offset)[0]
                    if scale == "/10":
                        val = round(val / 10.0, 1)
                elif itype in ("bool", "bit"):
                    byte_val = frame[offset]
                    if "offsetbit" in item:
                        bit = item["offsetbit"]
                        val = 1 if ((byte_val >> bit) & 1) != 0 else 0
                    else:
                        mask = item.get("mask", 1)
                        val = 1 if (byte_val & mask) != 0 else 0
                elif itype == "int8":
                    val = struct.unpack_from(">b", frame, offset)[0]
                elif itype == "uint8":
                    val = struct.unpack_from(">B", frame, offset)[0]
                else:
                    continue

                if self.telemetry_data.get(name) != val:
                    self.telemetry_data[name] = val
                    updated = True
            except Exception as err:
                _LOGGER.debug("Error decoding telemetry item %s at offset %d: %s", name, offset, err)

        if updated:
            self._notify_callbacks()

    def _handle_master_lcd_poll(self) -> None:
        """Evaluate 10s watchdog and answer poll if emulation is active."""
        silence_duration = time.time() - self.last_lcd_reply_time

        if silence_duration >= 10.0:
            if not self.lcd_emulator_enabled:
                _LOGGER.info("No physical LCD replies for %.1fs. Assuming Slave 1 LCD emulation.", silence_duration)
                self.lcd_emulator_enabled = True

        if not self.lcd_emulator_enabled:
            # Bus silence: physical LCD will answer or we are in grace period
            return

        # Build 42-byte data response (Total 47 bytes with header & CRC)
        resp = bytearray(45)
        resp[0] = 0x01
        resp[1] = 0x03
        resp[2] = 0x2A  # 42 data bytes

        # Reg 3011 at Offset 23-24 (Big-Endian word)
        flag = self.pending_event_flag
        resp[23] = (flag >> 8) & 0xFF
        resp[24] = flag & 0xFF

        # RTC at Offset 35-44 (Current Local Time)
        now = datetime.now()
        struct.pack_into(">H", resp, 35, now.year % 100)
        struct.pack_into(">H", resp, 37, now.month)
        struct.pack_into(">H", resp, 39, now.day)
        struct.pack_into(">H", resp, 41, now.hour)
        struct.pack_into(">H", resp, 43, now.minute)

        # Transmit frame with CRC
        packet = append_crc16(resp)
        self._send_raw(packet)

    def _handle_master_write_block(self, block_num: int, start_reg: int, data_bytes: bytes) -> None:
        """Store synchronized configuration registers and send FC 16 confirmation echo."""
        if block_num == 1:
            self.config_block1[:] = data_bytes
        elif block_num == 2:
            self.config_block2[:] = data_bytes
        elif block_num == 3:
            self.config_block3[:] = data_bytes

        # Unpack 90 registers
        for i in range(90):
            reg = start_reg + i
            raw_val = struct.unpack_from(">H", data_bytes, i * 2)[0]
            self.config_raw[reg] = raw_val

            # If this register is in our config definition map, update friendly config_data
            if reg in CONFIG_REGISTERS_BY_REG:
                meta = CONFIG_REGISTERS_BY_REG[reg]
                key = meta["key"]
                scale = meta.get("scale", 1)
                component = meta.get("component")

                if component == "switch":
                    self.config_data[key] = (raw_val == 1)
                elif component == "select":
                    options = meta.get("options", [])
                    if 0 <= raw_val < len(options):
                        self.config_data[key] = options[raw_val]
                    else:
                        self.config_data[key] = str(raw_val)
                else:  # number
                    if scale == 0.1:
                        # Signed 16-bit for temperatures that can be negative
                        signed_val = struct.unpack_from(">h", data_bytes, i * 2)[0]
                        self.config_data[key] = round(signed_val * 0.1, 1)
                    else:
                        self.config_data[key] = raw_val
                self.config_data[str(reg)] = self.config_data[key]

        _LOGGER.debug("Synchronized Block %d (Reg %d..%d) into memory.", block_num, start_reg, start_reg + 89)

        # Send FC 16 confirmation echo
        echo = bytearray([0x01, 0x10, (start_reg >> 8) & 0xFF, start_reg & 0xFF, 0x00, 0x5A])
        self._send_raw(append_crc16(echo))
        self._notify_callbacks()

    def _handle_master_clear_reg3011(self) -> None:
        """Acknowledge Master's clear of Register 3011 and finalize handshake."""
        prev_flag = self.pending_event_flag
        if prev_flag == 0x8000:
            self.config_initialized = True
            _LOGGER.info("Full Flag 128 initialization handshake complete! All 270 registers synchronized.")
        elif prev_flag != 0:
            _LOGGER.info("Single block settings synchronization acknowledged (Flag %d).", prev_flag)

        self.pending_event_flag = 0

        # Send FC 16 Echo
        echo = bytearray([0x01, 0x10, 0x0B, 0xC3, 0x00, 0x01])
        self._send_raw(append_crc16(echo))
        self._notify_callbacks()

    def _handle_master_read_block(self, start_reg: int) -> None:
        """Answer Master FC 03 read request with the requested 180-byte block."""
        if start_reg == 1001:
            data = self.config_block1
        elif start_reg == 1091:
            data = self.config_block2
        elif start_reg == 1181:
            data = self.config_block3
        else:
            return

        resp = bytearray([0x01, 0x03, 0xB4]) + data
        self._send_raw(append_crc16(resp))

    def _send_raw(self, packet: bytes) -> None:
        """Transmit raw bytes over serial connection."""
        if self._writer and not self._writer.is_closing():
            try:
                self._writer.write(packet)
            except Exception as err:
                _LOGGER.error("Serial write error: %s", err)

    def write_parameter(self, reg: int, value: Any) -> bool:
        """Update a configuration register in memory and queue Modbus synchronization to Master."""
        if not self.config_initialized:
            _LOGGER.warning("Cannot write register %d: Configuration not yet initialized from heat pump (Flag 128 pending).", reg)
            return False

        if reg not in CONFIG_REGISTERS_BY_REG:
            _LOGGER.error("Register %d is not defined in configuration specification.", reg)
            return False

        # --- EEPROM DAILY WRITE TRACKER ---
        today = date.today().isoformat()
        if self.daily_write_date != today:
            self.daily_write_date = today
            self.daily_write_count = 0

        meta = CONFIG_REGISTERS_BY_REG[reg]
        key = meta["key"]
        component = meta.get("component")
        scale = meta.get("scale", 1)

        # Convert friendly value to raw uint16
        raw_val = 0
        if component == "switch":
            raw_val = 1 if bool(value) else 0
        elif component == "select":
            options = meta.get("options", [])
            if str(value) in options:
                raw_val = options.index(str(value))
            else:
                try:
                    raw_val = int(value)
                except ValueError:
                    return False
        else:  # number
            if scale == 0.1:
                # Raw value = float / 0.1
                raw_int = int(round(float(value) * 10))
                raw_val = raw_int & 0xFFFF  # two's complement uint16
            else:
                raw_val = int(value)

        # Increment daily write counter
        self.daily_write_count += 1
        _LOGGER.info(
            "Writing Register %d (%s) -> Raw: %d (Friendly: %s). Daily write count: %d.",
            reg, meta["name"], raw_val, value, self.daily_write_count
        )
        self._notify_callbacks()

        # Update in-memory 180-byte block and queue synchronization flag
        if 1001 <= reg <= 1090:
            offset = (reg - 1001) * 2
            struct.pack_into(">H", self.config_block1, offset, raw_val)
            self.pending_event_flag = 0x0002
        elif 1091 <= reg <= 1180:
            offset = (reg - 1091) * 2
            struct.pack_into(">H", self.config_block2, offset, raw_val)
            self.pending_event_flag = 0x0004
        elif 1181 <= reg <= 1270:
            offset = (reg - 1181) * 2
            struct.pack_into(">H", self.config_block3, offset, raw_val)
            self.pending_event_flag = 0x0008

        # Update local states
        self.config_raw[reg] = raw_val
        self.config_data[key] = value
        self.config_data[str(reg)] = value

        self._notify_callbacks()
        return True
