<p align="center">
  <h1 align="center">🔧 MTK Client</h1>
  <p align="center">A full-featured MediaTek flash & repair desktop tool built with Python and PyQt6</p>
  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white"/>
    <img src="https://img.shields.io/badge/PyQt6-6.4+-41CD52?style=flat-square&logo=qt&logoColor=white"/>
    <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=flat-square&logo=windows&logoColor=white"/>
    <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square"/>
    <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square"/>
  </p>
</p>

---

## Overview

**MTK Client** is an open-source desktop GUI for flashing, repairing, and managing MediaTek (MTK) Android devices on Windows. It provides a clean dark-themed interface covering everything from low-level BROM communication to IMEI management — with a built-in terminal for operations that go beyond what a GUI can cover.

Built as a Python/PyQt6 desktop app, it wraps the [mtkclient](https://github.com/bkerler/mtkclient) library with a user-friendly interface suitable for both beginners and experienced technicians.

---

## Features

### 📡 Connection
- Auto-scan COM/USB ports with live refresh
- Connect in **BROM**, **Preloader**, or **Download Agent (DA)** mode
- Load custom DA binary and scatter files
- Live device info panel: Chip ID, HW code, HW version, secure boot state, serial number, battery voltage

### ⚡ Flash
- Load scatter file or firmware ZIP to populate partition table
- Per-partition selection with checkboxes
- Options: format before flash, verify after write, auto-reset, erase userdata
- Live progress bar with write speed indicator

### 💾 Read / Backup
- Quick presets: Full backup, Boot, Recovery, NVRAM, Persist
- Custom address range reads (hex start + length)
- Named partition reads
- Checksum verification on read

### 🗑️ Erase
- Targeted erase: userdata, cache, NVRAM, persist, or full chip
- Custom partition or raw address range
- Confirmation dialog before any destructive operation

### 📁 File Manager
- Split-pane browser: device filesystem ↔ local PC
- Mount/unmount device filesystem
- Push files to device, pull files to PC
- Local directory browser

### 🔐 Security
- Auth bypass methods: **Kamakiri**, DA auth skip, SLA auth skip
- Bootloader unlock / lock
- FRP lock removal
- Secure boot state check
- RSA key read

### 📟 NVRAM / EFS
- Read and write **IMEI 1 & 2**
- Full NVRAM backup, restore, repair, reset
- EFS / modem partition backup and restore
- Modem NV read

### 🖥️ Terminal
- Full interactive shell embedded in the app
- Runs any system command as a real subprocess
- Command history (↑ / ↓ arrow keys)
- Color-coded output, clear, copy-all
- Ideal for direct `mtkclient` CLI commands and advanced operations

---

## Getting Started

### Prerequisites
- Windows 10 or 11
- Python 3.10 or newer → [python.org](https://python.org)
- MediaTek USB VCOM driver (install from your device vendor or use [Zadig](https://zadig.akeo.ie/))

### Installation

**Option 1 — Batch launcher (easiest)**
```
Double-click launch_mtk.bat
```
It installs all dependencies automatically and launches the app.

**Option 2 — Manual**
```bash
git clone https://github.com/yourusername/mtk-client.git
cd mtk-client
pip install -r requirements.txt
python mtk_client.py
```

### Optional: real device backend
```bash
pip install mtkclient
```
Without this, the GUI runs in simulation mode (useful for UI testing without a device).

---

## Usage

### Connecting a device
1. Put your MTK device in **BROM mode**: power off → hold Vol Down → plug USB
2. Open the **Connection** tab
3. Click **↺ Refresh** to scan ports
4. Select the correct COM port and click **Connect Device**

### Flashing firmware
1. Connect the device first
2. Go to the **Flash** tab
3. Click **Load Scatter…** and select your `MT6xxx_Android_scatter.txt`
4. Check the partitions you want to flash
5. Click **Flash Selected**

### Using the terminal for advanced ops
The **Terminal** tab gives you a direct shell. Examples using mtkclient CLI:
```bash
# Auth bypass
python -m mtkclient.mtk payload

# Read boot partition
python -m mtkclient.mtk r boot boot.bin

# Write boot partition
python -m mtkclient.mtk w boot boot.bin

# Read full flash
python -m mtkclient.mtk rf full_backup.bin

# Unlock bootloader
python -m mtkclient.mtk da seccfg unlock
```

---

## Project Structure

```
mtk-client/
├── mtk_client.py      # Main application (all tabs, theme, logic)
├── launch_mtk.bat     # Windows one-click launcher
├── requirements.txt   # Python dependencies
├── .gitignore
└── README.md
```

---

## Roadmap

- [ ] Real mtkclient backend integration (replace simulation stubs)
- [ ] Linux & macOS support
- [ ] Scatter file parser with auto partition detection
- [ ] Firmware OTA ZIP unpacker
- [ ] TWRP / Magisk auto-installer
- [ ] Theme switcher (light / dark)
- [ ] Session logging to file
- [ ] Drag-and-drop firmware loading
- [ ] Multi-device support

---

## Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to change.

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

---

## Disclaimer

This tool is intended for **device repair, development, and educational purposes only**. Use it only on devices you own or have explicit permission to work on. The author is not responsible for bricked devices, voided warranties, or any other damage.

---

## License

[MIT](LICENSE) © 2025

---

<p align="center">Made with Python + PyQt6</p>
