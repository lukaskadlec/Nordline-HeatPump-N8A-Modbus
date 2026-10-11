**Languages / Jazyky:** [English](README.md) | [Čeština](README.cz.md)

---

# Tepelné čerpadlo vzduch-voda Nordline (N8A) – Integrace Modbus a Home Assistant

Obousměrné monitorování, telemetrie a plné konfigurační řízení pro tepelné čerpadlo **Nordline N8A vzduch-voda** (vybavené řídicí deskou **PC8002 PCB** a nástěnnou LCD jednotkou **Slave 1**).

Tento projekt nabízí dvě cesty nasazení:
1. **Nativní integrace pro Home Assistant (HACS) [Doporučeno]**: Přímé připojení přes lokální sériový port USB (`/dev/ttyUSB*`), nulová závislost na Node-RED či MQTT brokeru, grafická konfigurace (UI Config Flow), nativní termostatová entita `climate`, 42 telemetrických senzorů, 21 primárních ovládacích prvků, 88 konfiguračních registrů, vestavěný 10sekundový watchdog ticha fyzického LCD a automatická denní ochrana paměti EEPROM!
2. **Alternativa přes Node-RED a MQTT**: Odladěný produkční tok ([`flows.json`](flows.json)) s odstraněným laděním a pomocnými zápisy do souborů, komunikující přes MQTT Discovery.

---

---

## Obsah
1. [Architektura systému](#architektura-systému)
2. [Požadavky na hardware](#požadavky-na-hardware)
3. [Zapojení a přídavný vypínač napájení](#zapojení-a-přídavný-vypínač-napájení)
4. [Metoda A: Nativní HACS integrace (Doporučeno)](#metoda-a-nativní-hacs-integrace-doporučeno)
5. [Metoda B: Alternativa přes Node-RED a MQTT](#metoda-b-alternativa-přes-node-red-a-mqtt)
6. [Nastavení sériového portu](#nastavení-sériového-portu)
7. [Integrace do Home Assistant a uživatelské rozhraní](#integrace-do-home-assistant-a-uživatelské-rozhraní)
8. [Bezpečnostní a ochranné mechanismy](#bezpečnostní-a-ochranné-mechanismy)
9. [Referenční dokumentace](#referenční-dokumentace)

---

## Architektura systému

```text
+-----------------------+                    +---------------------------+
| Fyzický nástěnný LCD  |                    | USB-RS485 převodník       |
| ovladač (Slave ID 1)  |<---+          +--->| (např. /dev/ttyUSB-TC)    |
+-----------------------+    |          |    +---------------------------+
                             |  RS-485  |                  |
+-----------------------+    | dvoudrát |                  v
| Řídicí deska čerpadla |----+ sběrnice +    +---------------------------+
| (PC8002 PCB)          |                    |  Home Assistant           |
+-----------------------+                    |  - HACS integrace (Přímo) |
                                             |  NEBO Node-RED -> MQTT    |
                                             +---------------------------+
```

1. **Hlavní řídicí deska (PC8002 PCB - Master)** cyklicky každou sekundu vysílá broadcasty se stavem (`00, 16, 07` a `00, 16, 08`) a dotazuje se LCD displeje (`01, 03, 0B, B9, 00, 15`).
2. **Přímé sériové připojení**: Hostitelský systém je ke sběrnici připojen prostřednictvím galvanicky odděleného USB-RS485 převodníku.
3. **Pasivní odposlech**: Pokud je fyzický LCD ovladač aktivní, Home Assistant nebo Node-RED pouze pasivně naslouchá živé telemetrii na sběrnici.
4. **Koexistence a watchdog (10s)**: Pokud je fyzický LCD ovladač odpojen nebo vypnut přídavným vypínačem po dobu delší než 10 sekund, softwarový emulátor LCD automaticky převezme odpovídání na dotazy Masteru a synchronizaci parametrů z Home Assistant.

---

## Požadavky na hardware

Pro zprovoznění tohoto řešení budete potřebovat:
1. **Tepelné čerpadlo Nordline N8A** (nebo kompatibilní jednotku s řídicí deskou PC8002 PCB).
2. **USB-RS485 adaptér**:
   - Důrazně doporučujeme galvanicky oddělený USB-RS485 převodník na bázi FTDI, CH340 nebo CP2102, který ochrání váš hostitelský systém před zemními smyčkami a přepětím.
3. **Stíněný kroucený kabel**:
   - Dvoudrátový nebo třídrátový kabel pro propojení signálů `A (Data+)`, `B (Data-)` a volitelně `G (GND)` sběrnice RS-485.
4. **Přídavný kolébkový vypínač napájení (volitelný, ale doporučený)**:
   - Malý přepínač instalovaný do krytu nástěnné LCD jednotky přerušující napájecí vodič `V (VCC)`.
   - Umožňuje okamžité a bezpečné přepínání mezi fyzickým nástěnným panelem a emulací.
5. **Domácí server pro Home Assistant**:
   - Raspberry Pi, Intel NUC, Home Assistant Yellow/Green nebo virtuální stroj s Home Assistant OS / Supervised.

---

## Zapojení a přídavný vypínač napájení

### 1. Zapojení svorkovnice
Uvnitř nástěnného LCD ovladače se nachází 6pólová svorkovnice:

| Svorka | Funkce | Zapojení vodiče |
|:------:|:-------|:----------------|
| **G** | Zem (GND) | Společná zem s adaptérem RS-485 / tepelným čerpadlem |
| **B** | RS-485 Data - | Připojeno k lince RS-485 **B / D-** |
| **A** | RS-485 Data + | Připojeno k lince RS-485 **A / D+** |
| **T** | TX (Interní) | Nezapojeno |
| **R** | RX (Interní) | Nezapojeno |
| **V** | Napájení (+12V/+24V) | Připojeno přes **přídavný vypínač napájení** |

![Zapojení kabelu](assets/cable_connection.JPEG)

### 2. Instalace přídavného vypínače napájení
Jelikož je RS-485 sběrnice s jedním Masterem, současné odpovídání dvou zařízení na adresu Slave 1 způsobuje elektrické kolize a chyby rámců (framing/CRC errors).

Pro čisté přepínání mezi fyzickým ovládáním a automatizací byl do série s napájecí svorkou **V** zapojen červený kolébkový vypínač:

![Přídavný vypínač](assets/custom_power_switch.JPEG)

- **Vypínač ZAPNUT (ON)**: Fyzický LCD displej je napájen a odpovídá na dotazy řídicí desky (Master). Softwarová emulace se automaticky vypne a systém přechází do čistě pasivního režimu odposlechu.
- **Vypínač VYPNUT (OFF)**: Fyzický LCD displej je bez napájení. Po 10 sekundách ticha na sběrnici vyprší 10sekundový watchdog a softwarový emulátor LCD automaticky převezme odpovídání na dotazy Masteru i zpracování příkazů z Home Assistant.

---

## Metoda A: Nativní HACS integrace (Doporučeno)

Nativní uživatelská komponenta (`custom_components/nordline_heatpump`) komunikuje přímo s převodníkem USB-RS485 a nevyžaduje Node-RED ani MQTT broker.

### Vlastnosti:
- **Nativní termostat**: Sjednocená entita `climate` (`Termostat`) s režimy Topení, Chlazení a Vypnuto + posuvníkem žádané teploty.
- **Všech 109 registrů a 42 telemetrických senzorů**: Automaticky vytvoří přehledné entity pro veškeré parametry.
- **Vestavěný 10sekundový watchdog**: Automaticky detekuje ticho fyzického LCD panelu a hladce převezme řízení.
- **Ochrana životnosti EEPROM**: Integrovaný denní čítač a omezovač zápisů vynucující bezpečný strop **20 zápisů za den**.

### Instalace přes HACS (Doporučeno):
1. V Home Assistant otevřete **HACS** -> **Integrace**.
2. Klikněte na tři tečky (⋮) v pravém horním rohu a vyberte **Vlastní repozitáře** (Custom repositories).
3. Vyplňte údaje o repozitáři:
   - **Repozitář**: `https://github.com/lukaskadlec/Nordline-HeatPump-N8A-Modbus`
   - **Typ / Kategorie**: `Integrace` (Integration)
4. Klikněte na **Přidat** (Add).
5. V HACS vyhledejte **Nordline Heat Pump N8A Modbus** a klikněte na **Stáhnout** (Download).
6. Restartujte Home Assistant.
7. V Home Assistant přejděte do **Nastavení** -> **Zařízení a služby** -> **Přidat integraci**.
8. Vyhledejte **Nordline Heat Pump N8A Modbus**.
9. Zvolte váš sériový port (např. `/dev/ttyUSB-TC` nebo `/dev/serial/by-id/...`), přenosovou rychlost (`9600`) a potvrďte tlačítkem **Odeslat**.
10. Zařízení tepelného čerpadla se okamžitě zobrazí se všemi ovládacími prvky, termostatem, senzory a konfiguračními přepínači!

### Manuální instalace (Alternativa):
1. Zkopírujte složku `custom_components/nordline_heatpump` do vašeho adresáře `/config/custom_components/` v Home Assistant:
   ```bash
   cp -r custom_components/nordline_heatpump /config/custom_components/
   ```
2. Restartujte Home Assistant a postupujte podle kroků 7–10 výše.

---

## Metoda B: Alternativa přes Node-RED a MQTT

Pro instalace, které již provozují Node-RED, je k dispozici odladěný produkční tok (`flows.json`) s odstraněným laděním a pomocnými soubory.

### Požadavky:
1. **Home Assistant**: s aktivovanou integrací **MQTT**.
2. **Mosquitto Broker**: nainstalovaný a spuštěný.
3. **Node-RED**: s balíčky palety `node-red-contrib-buffer-parser` a `node-red-node-serialport`.

### Nastavení:
1. V Node-RED otevřete nabídku vpravo nahoře -> **Importovat**.
2. Vyberte a importujte soubor [`flows.json`](flows.json).
3. Nakonfigurujte uzel `mqtt` broker (IP adresa a přihlašovací údaje).
4. Zkontrolujte cestu k sériovému portu v uzlu `/dev/ttyUSB-TC`.
5. Klikněte na **Nasadit** (Deploy). Telemetrie a zprávy MQTT Discovery se odešlou automaticky.

![Snímek toku v Node-RED](assets/Node_Red_screen.png)

---

## Nastavení sériového portu

V konfiguračním uzlu `serial-port` v Node-RED (nebo konfiguraci HACS integrace) se používají tyto parametry sběrnice:

| Vlastnost | Hodnota | Popis |
|:---|:---|:---|
| **Sériový port** | `/dev/ttyUSB-TC` *(nebo váš port / COM)* | Cesta k zařízení v Linuxu nebo symlink |
| **Přenosová rychlost** | `9600` | Rychlost Modbus sběrnice tepelného čerpadla |
| **Datové bity** | `8` | Standardní Modbus RTU |
| **Parita** | `Žádná` (None) | Bez paritního bitu |
| **Stop bity** | `1` | 1 stop bit |
| **Řízení toku** | DTR: auto, RTS: auto, CTS: auto, DSR: auto | Bez hardwarového handshakingu |
| **Rozdělení vstupu** | Po odmlce trvající **`40 ms`** | Zajišťuje doručení celistvých rámců |
| **Doručovat jako** | `binární buffery` (binary buffers) | Nativní objekty typu Buffer |
| **Časový limit odezvy**| `1000 ms` | Výchozí limit 1 sekunda |
![Nastavení sériového portu](assets/serial_port_setting.png)

---

## Integrace do Home Assistant a uživatelské rozhraní

Po nasazení toku uzel `Create HA mqtt device` publikuje konfigurační zprávy MQTT Discovery do tématu `homeassistant/#`. Tepelné čerpadlo se v Home Assistant zobrazí jako jedno ucelené zařízení s názvem **Heat Pump**:

![Uživatelské rozhraní Home Assistant](assets/HA_screen.png)

### Logické řazení a taxonomie entit:
Entity jsou strukturovány tak, aby se na kartách zařízení Home Assistant přirozeně a logicky řadily:
- **Ovládací prvky (21 hlavních prvků v kartě Ovládání)**: Přehledné názvy bez závorek pro rychlé ovládání:
  - `Power State` (Vypínač: `switch.hp_power_state`)
  - `Operating Mode` (Provozní režim: `select.hp_operating_mode`)
  - `Heating Setpoint`, `Hot Water Setpoint`, `Cooling Setpoint` (Požadovaná teplota topení, TUV, chlazení)
  - `Fast Mute`, `Mute Timer Enable / Start / End` (Rychlý tichý režim, plánovač tichého režimu)
  - `Electric Heater`, `Daily Timer 1 & 2 Schedules` (Záložní elektrokotel, denní časovače 1 a 2)
  - `Pump Running Mode / Interval / Duration` (Režim, interval a doba běhu čerpadla)
- **Konfigurace (88 pokročilých servisních registrů)**: Seskupeno podle kategorií s jednotnou předponou:
  - `[System]`, `[Protect]`, `[Fan]`, `[Defrost]`, `[EEV]`, `[Disinf]`, `[Pump]`, `[Temp]`
- **Senzory a diagnostika (42 telemetrických senzorů)**:
  - `[Temp]`: Teploty vody (Vstupní, Výstupní, Bojler TUV), Chladivo (Sání, Výtlak, Výparník, Přehřátí), Systém (Venkovní okolí, Invertor, Ochrana modulu)
  - `[Pressure]`: Tlakový snímač sání LP, Tlakový snímač výtlaku HP
  - `[Electrical]`: Napětí sítě AC, Proud sítě AC, Napětí DC sběrnice, Fázový proud kompresoru
  - `[Fan]`: Otáčky ventilátoru, Požadované otáčky
  - `[EEV]`: Kroky elektronického expanzního ventilu
  - `[System]`: Požadovaná frekvence, Aktuální frekvence, Stav napájení ON/OFF, Status
  - `[Output]`: Výstupní relé O01 až O13
  - `[Alarm]`: Bezpečnostní spínače S01 až S07 a aktivní číselný kód chyby

---

## Bezpečnostní a ochranné mechanismy

1. **Dvoustupňový 10sekundový watchdog ticha LCD ovladače**:
   - **Okamžité vypnutí emulace**: Jakýkoliv příchozí paket `01, 03, 42 Display Reply` z fyzického LCD ovladače okamžitě deaktivuje emulaci v paměti (`flow.set("lcd_emulator_enabled", false)`).
   - **Aktivace po 10 sekundách ticha**: Emulátor LCD v Node-RED začne odpovídat na dotazy Masteru teprve tehdy, pokud po dobu nejméně 10 sekund nebyl zachycen žádný paket od fyzického LCD panelu.
   - **Ochrana při opětovném zapnutí**: Pokud je fyzický vypínač zapnut, hned první přijatý paket okamžitě odpojí emulátor Node-RED, čímž je zaručena nulová kolize na lince RS-485.
2. **Ochrana proti neúplné synchronizaci při startu (Flag 128 / 0x8000)**:
   - Při startu toku Node-RED nebo převzetí emulace zařadí do fronty příznak Flag 128, kterým si od řídicí desky vyžádá vyčtení všech 270 konfiguračních registrů.
   - Zápisy parametrů z Home Assistant jsou **zablokovány**, dokud nejsou všechny registry načteny v paměti, což brání nechtěnému přepsání parametrů výchozími nulami.
3. **Validace kontrolních součtů CRC-16 a rámců**:
   - Každý přijatý rámec je před dekódováním nebo přeposláním ověřen pomocí algoritmu Modbus CRC-16.

---

## Referenční dokumentace

- [`heatpump_configuration_registers.cz.txt`](heatpump_configuration_registers.cz.txt) / [Anglická verze (`heatpump_configuration_registers.txt`)](heatpump_configuration_registers.txt): Kompletní servisní mapa 270 registrů, rozsahy parametrů, přepočty a tovární kódy.
- [`heatpump_rs485_protocol_spec.cz.txt`](heatpump_rs485_protocol_spec.cz.txt) / [Anglická verze (`heatpump_rs485_protocol_spec.txt`)](heatpump_rs485_protocol_spec.txt): Podrobná specifikace reverzního inženýrství protokolu Modbus, časování rámců a stavové automaty.
- [`Nordline_N8A_Manual.pdf`](Nordline_N8A_Manual.pdf): Oficiální servisní manuál výrobce k desce PC8002 PCB a schémata elektrického zapojení.
