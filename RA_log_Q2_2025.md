# Raspberry Pi Sensor & Connectivity Setup – RA Log Q2 2025

## Quick-Guide Takeaways (from Steve Teoh's Guides)

| Area | What I set up & verified | Why it matters |
|------|-------------------------|----------------|
| **Raspberry Pi 3 B+ & OS** | • Flashed SD XC with Raspberry Pi Imager; preset user =`user`, enabled SSH/VNC/SPI/I²C/UART; left Windows “Format?” prompt **untouched**.  • Turned on GL Full KMS to avoid camera glitches. | Baseline image reproducible by any team-mate; graphics stack ready for camera preview. |
| **Arducam IMX219 (8 MP)** | • Disabled `camera_auto_detect`, added `dtoverlay=imx219,vcm`.  • Tested with `libcamera-vid`.  • Wrote `picamera2_continuous.py` + `record.sh` → one-minute, timestamped H.264 clips auto-rotate in `/Video/`. | Gives continuous, filename-stamped evidence for the Naturalistic Driving Study (NDS). |
| **MPU6050 (Accel + Gyro)** | • Wired SDA/SCL/VCC/GND (default addr 0x68).  • Enabled I²C via `raspi-config`.  • Installed `python3-smbus` / `mpu6050-raspberrypi`.  • Python loop prints g-forces + °/s each second. | Real-time motion features ready for “risky-behaviour” scoring pipeline. |
| **UART housekeeping** | • Installed `pyserial` + `minicom`.  • Stopped `serial-getty@ttyS0`, stripped `console=serial0,115200` from `/boot/cmdline.txt`.  • Optional: reclaimed high-precision `/dev/ttyAMA0` with `dtoverlay=pi3-miniuart-bt`. | Prevents login console from hijacking GPS/LTE modules; frees the good UART. |
| **SIM7000E NB-IoT HAT** | • Correct HAT orientation (antenna away from USB/LAN).  • Minicom on `/dev/ttyAMA0`; ran key AT chain: `AT+CNMP`, `AT+CMNB`, `AT+CSQ`, MQTT connect/pub/sub, `AT+CNACT` etc. | Verified NB-IoT attach and end-to-end MQTT; template for automated Python dial-up. |
| **SIM A7670SA 4G LTE** | • Wired 5 V, GND, TXD0→R, RXD0→T; seated IPX antennas carefully.  • Identity, signal & network cmds (`AT+CGMI`, `AT+CSQ`, `AT+CREG?`, `AT+CPING="www.google.com"`). | LTE fallback path operational; groundwork for dual-stack NB-IoT + LTE data uplink. |

## Practical Lessons & Next Steps

1. **Serial vs. I²C conflicts** – Free the UART early; mind MPU6050 address pin (0x68 → 0x69) to avoid bus clashes.  
2. **File integrity** – Keep `/boot/cmdline.txt` a **single line**; extra line breaks brick the boot.  
3. **Hardware safety** – Double-check 40-pin alignment and IPX snaps; mistakes are permanent.  
4. **Automation roadmap**  
   - Merge sensor readings into the Picamera overlay.  
   - Wrap AT command flow in a Python class (pyserial) + systemd service.  
   - Push scripts + service files to the repo with Markdown HOW-TO.

> _Based on Quick Guide Part 1, 2, 3 by Steve Teoh (2025)._
