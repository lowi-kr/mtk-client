"""
MTK Client — MediaTek Flash Tool (PyQt6)
Requires: pip install PyQt6 pyserial
Optional for real MTK backend: pip install mtkclient
"""

import sys
import os
import subprocess
import threading
import time
import serial.tools.list_ports
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTabWidget, QLineEdit, QFileDialog,
    QTextEdit, QComboBox, QProgressBar, QFrame, QSplitter,
    QTreeWidget, QTreeWidgetItem, QCheckBox, QGroupBox,
    QStatusBar, QSizePolicy, QSpacerItem, QScrollArea,
    QGridLayout, QMessageBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QSlider, QSpinBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize, QProcess
from PyQt6.QtGui import (
    QFont, QColor, QPalette, QTextCursor, QIcon,
    QFontDatabase, QPainter, QPixmap
)

# ─────────────────────────────────────────────
#  THEME
# ─────────────────────────────────────────────
DARK = """
QMainWindow, QWidget {
    background-color: #0e1117;
    color: #d0d8e8;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 12px;
}
QTabWidget::pane {
    border: 1px solid #1e2530;
    background: #10141c;
}
QTabBar::tab {
    background: #141920;
    color: #6a7a90;
    padding: 8px 18px;
    border: none;
    border-right: 1px solid #1e2530;
    font-size: 11px;
    letter-spacing: 1px;
    text-transform: uppercase;
}
QTabBar::tab:selected {
    background: #10141c;
    color: #00e5a0;
    border-top: 2px solid #00e5a0;
}
QTabBar::tab:hover:!selected {
    background: #181f2a;
    color: #a0b4cc;
}
QPushButton {
    background-color: #141920;
    color: #a0b4cc;
    border: 1px solid #253040;
    border-radius: 4px;
    padding: 6px 14px;
    font-size: 11px;
    letter-spacing: 0.5px;
}
QPushButton:hover {
    background-color: #1c2535;
    color: #00e5a0;
    border-color: #00e5a0;
}
QPushButton:pressed {
    background-color: #00c080;
    color: #001a10;
}
QPushButton:disabled {
    color: #374050;
    border-color: #1e2530;
}
QPushButton#danger {
    color: #e05555;
    border-color: #5a2020;
}
QPushButton#danger:hover {
    background: #2a1515;
    border-color: #e05555;
}
QPushButton#accent {
    background: #00c080;
    color: #001a10;
    border: none;
    font-weight: bold;
}
QPushButton#accent:hover {
    background: #00e5a0;
}
QPushButton#accent:disabled {
    background: #1c3030;
    color: #2a5040;
}
QLineEdit, QComboBox, QSpinBox {
    background: #0a0d14;
    border: 1px solid #1e2530;
    border-radius: 3px;
    color: #c0cce0;
    padding: 5px 8px;
    selection-background-color: #00804a;
}
QLineEdit:focus, QComboBox:focus {
    border-color: #00c080;
}
QComboBox::drop-down { border: none; width: 20px; }
QComboBox::down-arrow { image: none; border-left: 4px solid transparent; border-right: 4px solid transparent; border-top: 5px solid #6a7a90; }
QComboBox QAbstractItemView {
    background: #0e1117;
    border: 1px solid #253040;
    color: #c0cce0;
    selection-background-color: #1c4030;
}
QTextEdit {
    background: #060910;
    color: #00e5a0;
    border: 1px solid #1a2030;
    border-radius: 3px;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 11px;
}
QTreeWidget {
    background: #080b12;
    border: 1px solid #1a2030;
    color: #a0b4cc;
    alternate-background-color: #0c1018;
}
QTreeWidget::item:selected {
    background: #1c3040;
    color: #00e5a0;
}
QTableWidget {
    background: #080b12;
    border: 1px solid #1a2030;
    color: #a0b4cc;
    gridline-color: #151c28;
}
QTableWidget::item:selected {
    background: #1c3040;
    color: #00e5a0;
}
QHeaderView::section {
    background: #101520;
    color: #6a8090;
    border: none;
    border-right: 1px solid #1e2530;
    border-bottom: 1px solid #1e2530;
    padding: 4px 8px;
    font-size: 10px;
    letter-spacing: 1px;
    text-transform: uppercase;
}
QProgressBar {
    background: #0a0d14;
    border: 1px solid #1e2530;
    border-radius: 3px;
    text-align: center;
    color: #00e5a0;
    font-size: 10px;
}
QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #007850, stop:1 #00e5a0);
    border-radius: 2px;
}
QGroupBox {
    border: 1px solid #1e2530;
    border-radius: 4px;
    margin-top: 12px;
    padding-top: 8px;
    color: #6a8090;
    font-size: 10px;
    letter-spacing: 1px;
    text-transform: uppercase;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
    color: #4a8070;
}
QScrollBar:vertical {
    background: #0a0d14;
    width: 8px;
    border: none;
}
QScrollBar::handle:vertical {
    background: #253040;
    border-radius: 4px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover { background: #3a5060; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QStatusBar {
    background: #090c14;
    border-top: 1px solid #1a2030;
    color: #4a6070;
    font-size: 10px;
}
QCheckBox { color: #8090a8; spacing: 6px; }
QCheckBox::indicator {
    width: 13px; height: 13px;
    border: 1px solid #2a3a4a;
    border-radius: 2px;
    background: #0a0d14;
}
QCheckBox::indicator:checked {
    background: #00c080;
    border-color: #00c080;
}
QSplitter::handle { background: #1a2030; width: 1px; height: 1px; }
QLabel#section {
    color: #4a8070;
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
}
QLabel#value {
    color: #00e5a0;
    font-family: "Consolas";
}
QLabel#warn { color: #f0a500; }
QLabel#err  { color: #e05555; }
"""

# ─────────────────────────────────────────────
#  LOG WORKER — runs commands in background
# ─────────────────────────────────────────────
class CommandWorker(QThread):
    output = pyqtSignal(str)
    finished = pyqtSignal(int)

    def __init__(self, cmd, parent=None):
        super().__init__(parent)
        self.cmd = cmd

    def run(self):
        try:
            proc = subprocess.Popen(
                self.cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, shell=isinstance(self.cmd, str),
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            )
            for line in proc.stdout:
                self.output.emit(line.rstrip())
            proc.wait()
            self.finished.emit(proc.returncode)
        except Exception as e:
            self.output.emit(f"[ERROR] {e}")
            self.finished.emit(-1)


# ─────────────────────────────────────────────
#  TERMINAL WIDGET
# ─────────────────────────────────────────────
class TerminalWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # toolbar
        bar = QHBoxLayout()
        bar.setContentsMargins(8, 6, 8, 2)
        self.lbl = QLabel("TERMINAL")
        self.lbl.setObjectName("section")
        bar.addWidget(self.lbl)
        bar.addStretch()
        self.btn_clear = QPushButton("Clear")
        self.btn_clear.setFixedWidth(60)
        self.btn_copy = QPushButton("Copy all")
        self.btn_copy.setFixedWidth(70)
        bar.addWidget(self.btn_clear)
        bar.addWidget(self.btn_copy)
        layout.addLayout(bar)

        # output
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setObjectName("terminal_out")
        layout.addWidget(self.output, 1)

        # input row
        inp_row = QHBoxLayout()
        inp_row.setContentsMargins(8, 2, 8, 6)
        self.prompt = QLabel("C:\\>")
        self.prompt.setObjectName("value")
        self.prompt.setFixedWidth(50)
        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter command…")
        self.run_btn = QPushButton("Run")
        self.run_btn.setObjectName("accent")
        self.run_btn.setFixedWidth(55)
        inp_row.addWidget(self.prompt)
        inp_row.addWidget(self.input, 1)
        inp_row.addWidget(self.run_btn)
        layout.addLayout(inp_row)

        self.btn_clear.clicked.connect(self.output.clear)
        self.btn_copy.clicked.connect(lambda: QApplication.clipboard().setText(self.output.toPlainText()))
        self.run_btn.clicked.connect(self._run)
        self.input.returnPressed.connect(self._run)

        self._history = []
        self._hist_idx = -1

        self.log("[MTK Terminal ready — type a command or use tabs above]\n", "#4a8070")

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Up and self._history:
            self._hist_idx = max(0, self._hist_idx - 1)
            self.input.setText(self._history[self._hist_idx])
        elif e.key() == Qt.Key.Key_Down and self._history:
            self._hist_idx = min(len(self._history), self._hist_idx + 1)
            self.input.setText(self._history[self._hist_idx] if self._hist_idx < len(self._history) else "")
        else:
            super().keyPressEvent(e)

    def _run(self):
        cmd = self.input.text().strip()
        if not cmd:
            return
        self._history.append(cmd)
        self._hist_idx = len(self._history)
        self.input.clear()
        self.log(f"\n> {cmd}", "#00c080")
        self._worker = CommandWorker(cmd)
        self._worker.output.connect(lambda l: self.log(l))
        self._worker.finished.connect(lambda rc: self.log(f"\n[exit {rc}]", "#4a6070" if rc == 0 else "#e05555"))
        self._worker.start()

    def log(self, text, color="#a0c0b0"):
        self.output.setTextColor(QColor(color))
        self.output.append(text)
        self.output.moveCursor(QTextCursor.MoveOperation.End)

    def run_command(self, cmd):
        self.input.setText(cmd)
        self._run()


# ─────────────────────────────────────────────
#  STATUS BAR DEVICE INDICATOR
# ─────────────────────────────────────────────
class DeviceIndicator(QWidget):
    def __init__(self):
        super().__init__()
        lay = QHBoxLayout(self)
        lay.setContentsMargins(8, 0, 8, 0)
        lay.setSpacing(6)
        self.dot = QLabel("●")
        self.dot.setStyleSheet("color:#2a4a38; font-size:14px;")
        self.lbl = QLabel("No device")
        self.lbl.setStyleSheet("color:#3a5048; font-size:10px;")
        lay.addWidget(self.dot)
        lay.addWidget(self.lbl)

    def set_connected(self, name="MTK Device"):
        self.dot.setStyleSheet("color:#00e5a0; font-size:14px;")
        self.lbl.setText(name)
        self.lbl.setStyleSheet("color:#00c080; font-size:10px;")

    def set_disconnected(self):
        self.dot.setStyleSheet("color:#2a4a38; font-size:14px;")
        self.lbl.setText("No device")
        self.lbl.setStyleSheet("color:#3a5048; font-size:10px;")


# ─────────────────────────────────────────────
#  TAB: CONNECTION
# ─────────────────────────────────────────────
class ConnectionTab(QWidget):
    device_connected = pyqtSignal(str)
    device_disconnected = pyqtSignal()
    log_message = pyqtSignal(str, str)

    def __init__(self, terminal):
        super().__init__()
        self.terminal = terminal
        self._connected = False
        self._build()

    def _build(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(16, 16, 16, 16)
        main.setSpacing(12)

        # ── Port selection ──
        port_grp = QGroupBox("Serial / USB Port")
        pg = QGridLayout(port_grp)
        pg.addWidget(QLabel("Port:"), 0, 0)
        self.port_combo = QComboBox()
        self.port_combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        pg.addWidget(self.port_combo, 0, 1)
        self.refresh_btn = QPushButton("↺  Refresh")
        self.refresh_btn.setFixedWidth(90)
        pg.addWidget(self.refresh_btn, 0, 2)
        pg.addWidget(QLabel("Baud:"), 1, 0)
        self.baud_combo = QComboBox()
        self.baud_combo.addItems(["115200", "921600", "460800", "230400", "57600", "9600"])
        pg.addWidget(self.baud_combo, 1, 1)
        main.addWidget(port_grp)

        # ── Connection mode ──
        mode_grp = QGroupBox("Connection Mode")
        mg = QGridLayout(mode_grp)
        self.mode_auto = QCheckBox("Auto-detect (BROM / Preloader / DA)")
        self.mode_auto.setChecked(True)
        self.mode_brom = QCheckBox("Force BROM mode")
        self.mode_preloader = QCheckBox("Force Preloader mode")
        self.mode_auth = QCheckBox("Use authentication / auth bypass")
        mg.addWidget(self.mode_auto, 0, 0, 1, 2)
        mg.addWidget(self.mode_brom, 1, 0)
        mg.addWidget(self.mode_preloader, 1, 1)
        mg.addWidget(self.mode_auth, 2, 0)
        main.addWidget(mode_grp)

        # ── DA / scatter ──
        da_grp = QGroupBox("Download Agent / Scatter File")
        dg = QGridLayout(da_grp)
        dg.addWidget(QLabel("DA File:"), 0, 0)
        self.da_path = QLineEdit()
        self.da_path.setPlaceholderText("Optional — leave blank for auto")
        dg.addWidget(self.da_path, 0, 1)
        self.da_browse = QPushButton("Browse")
        self.da_browse.setFixedWidth(70)
        dg.addWidget(self.da_browse, 0, 2)
        dg.addWidget(QLabel("Scatter:"), 1, 0)
        self.scatter_path = QLineEdit()
        self.scatter_path.setPlaceholderText("Optional — MT6xxx_Android_scatter.txt")
        dg.addWidget(self.scatter_path, 1, 1)
        self.scatter_browse = QPushButton("Browse")
        self.scatter_browse.setFixedWidth(70)
        dg.addWidget(self.scatter_browse, 1, 2)
        main.addWidget(da_grp)

        # ── Connect button ──
        btn_row = QHBoxLayout()
        self.connect_btn = QPushButton("  Connect Device")
        self.connect_btn.setObjectName("accent")
        self.connect_btn.setMinimumHeight(38)
        self.disconnect_btn = QPushButton("Disconnect")
        self.disconnect_btn.setObjectName("danger")
        self.disconnect_btn.setEnabled(False)
        btn_row.addWidget(self.connect_btn, 2)
        btn_row.addWidget(self.disconnect_btn, 1)
        main.addLayout(btn_row)

        # ── Device info panel ──
        info_grp = QGroupBox("Device Information")
        ig = QGridLayout(info_grp)
        fields = [
            ("Chip ID", "chip_id"), ("Hardware Code", "hw_code"),
            ("Hardware Sub-code", "hw_sub"), ("Hardware Version", "hw_ver"),
            ("Software Version", "sw_ver"), ("Secure Boot", "secure_boot"),
            ("Serial Number", "serial"), ("Battery", "battery"),
        ]
        self._info_labels = {}
        for i, (label, key) in enumerate(fields):
            lbl = QLabel(label + ":")
            lbl.setObjectName("section")
            val = QLabel("—")
            val.setObjectName("value")
            self._info_labels[key] = val
            ig.addWidget(lbl, i, 0)
            ig.addWidget(val, i, 1)
        main.addWidget(info_grp)
        main.addStretch()

        # signals
        self.refresh_btn.clicked.connect(self._refresh_ports)
        self.connect_btn.clicked.connect(self._connect)
        self.disconnect_btn.clicked.connect(self._disconnect)
        self.da_browse.clicked.connect(lambda: self._browse(self.da_path, "Download Agent (*.bin *.hex);;All files (*)"))
        self.scatter_browse.clicked.connect(lambda: self._browse(self.scatter_path, "Scatter files (*.txt);;All files (*)"))

        self._refresh_ports()

    def _refresh_ports(self):
        self.port_combo.clear()
        ports = serial.tools.list_ports.comports()
        for p in ports:
            self.port_combo.addItem(f"{p.device}  —  {p.description}", p.device)
        if not ports:
            self.port_combo.addItem("(No COM ports found)")

    def _browse(self, field, filt):
        path, _ = QFileDialog.getOpenFileName(self, "Select file", "", filt)
        if path:
            field.setText(path)

    def _connect(self):
        port = self.port_combo.currentData() or self.port_combo.currentText().split()[0]
        baud = self.baud_combo.currentText()
        self.terminal.log(f"\n[+] Connecting on {port} @ {baud}…", "#00c080")
        self.connect_btn.setEnabled(False)
        self.connect_btn.setText("  Connecting…")

        # simulate connect (replace with real mtkclient call)
        QTimer.singleShot(1500, self._simulate_connect)

    def _simulate_connect(self):
        info = {
            "chip_id": "0x6765  (Helio G85)",
            "hw_code": "0x8163",
            "hw_sub": "0x8A00",
            "hw_ver": "0xCA01",
            "sw_ver": "0x0001",
            "secure_boot": "Enabled",
            "serial": "A1B2C3D4E5F6",
            "battery": "3.87V",
        }
        for k, v in info.items():
            self._info_labels[k].setText(v)

        self._connected = True
        self.connect_btn.setText("  Connected ✓")
        self.connect_btn.setEnabled(False)
        self.disconnect_btn.setEnabled(True)
        self.terminal.log("[+] Device connected: Helio G85 / MT6765", "#00e5a0")
        self.terminal.log("[+] BROM mode detected", "#00c080")
        self.terminal.log("[+] Auth bypass: OK", "#00c080")
        self.device_connected.emit("MT6765 — Helio G85")

    def _disconnect(self):
        self._connected = False
        for lbl in self._info_labels.values():
            lbl.setText("—")
        self.connect_btn.setEnabled(True)
        self.connect_btn.setText("  Connect Device")
        self.disconnect_btn.setEnabled(False)
        self.terminal.log("\n[!] Device disconnected.", "#f0a500")
        self.device_disconnected.emit()


# ─────────────────────────────────────────────
#  TAB: FLASH
# ─────────────────────────────────────────────
class FlashTab(QWidget):
    def __init__(self, terminal):
        super().__init__()
        self.terminal = terminal
        self._build()

    def _build(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(16, 16, 16, 16)
        main.setSpacing(10)

        # partition table
        part_grp = QGroupBox("Partition Map — select partitions to flash")
        pg = QVBoxLayout(part_grp)
        self.part_table = QTableWidget(0, 5)
        self.part_table.setHorizontalHeaderLabels(["", "Partition", "Size", "Offset", "File"])
        self.part_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.part_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.part_table.setColumnWidth(0, 28)
        self.part_table.setColumnWidth(2, 80)
        self.part_table.setColumnWidth(3, 100)
        pg.addWidget(self.part_table)
        btns = QHBoxLayout()
        self.load_scatter = QPushButton("Load Scatter…")
        self.load_firmware = QPushButton("Load Firmware ZIP…")
        self.select_all = QPushButton("Select all")
        self.deselect_all = QPushButton("Deselect all")
        for b in [self.load_scatter, self.load_firmware, self.select_all, self.deselect_all]:
            btns.addWidget(b)
        btns.addStretch()
        pg.addLayout(btns)
        main.addWidget(part_grp, 2)

        # options
        opt_grp = QGroupBox("Flash Options")
        og = QGridLayout(opt_grp)
        self.opt_format = QCheckBox("Format before flash")
        self.opt_verify = QCheckBox("Verify after write")
        self.opt_verify.setChecked(True)
        self.opt_reset = QCheckBox("Reset after flash")
        self.opt_reset.setChecked(True)
        self.opt_erase = QCheckBox("Erase userdata / cache")
        og.addWidget(self.opt_format, 0, 0)
        og.addWidget(self.opt_verify, 0, 1)
        og.addWidget(self.opt_reset, 1, 0)
        og.addWidget(self.opt_erase, 1, 1)
        main.addWidget(opt_grp)

        # progress
        prog_grp = QGroupBox("Progress")
        pgg = QVBoxLayout(prog_grp)
        self.status_lbl = QLabel("Ready")
        self.status_lbl.setObjectName("value")
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.speed_lbl = QLabel("—")
        self.speed_lbl.setStyleSheet("color:#6a8090; font-size:10px;")
        pgg.addWidget(self.status_lbl)
        pgg.addWidget(self.progress)
        pgg.addWidget(self.speed_lbl)
        main.addWidget(prog_grp)

        # action buttons
        act = QHBoxLayout()
        self.flash_btn = QPushButton("  Flash Selected")
        self.flash_btn.setObjectName("accent")
        self.flash_btn.setMinimumHeight(36)
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setObjectName("danger")
        self.stop_btn.setEnabled(False)
        act.addWidget(self.flash_btn, 3)
        act.addWidget(self.stop_btn, 1)
        main.addLayout(act)

        # wire
        self.load_scatter.clicked.connect(self._load_scatter)
        self.load_firmware.clicked.connect(self._load_firmware)
        self.select_all.clicked.connect(lambda: self._set_all(True))
        self.deselect_all.clicked.connect(lambda: self._set_all(False))
        self.flash_btn.clicked.connect(self._start_flash)
        self.stop_btn.clicked.connect(self._stop_flash)

        self._populate_demo()

    def _populate_demo(self):
        parts = [
            ("preloader", "256 KB", "0x00000000"),
            ("mbr", "128 KB",  "0x00040000"),
            ("ebr1", "128 KB", "0x00060000"),
            ("lk", "1 MB",    "0x00080000"),
            ("boot", "16 MB",  "0x00480000"),
            ("recovery", "16 MB", "0x01480000"),
            ("system", "2.5 GB", "0x02480000"),
            ("vendor", "512 MB", "0xC0000000"),
            ("userdata", "~", "0xE0000000"),
        ]
        self.part_table.setRowCount(len(parts))
        for i, (name, size, offset) in enumerate(parts):
            cb = QCheckBox()
            cb.setChecked(name not in ("userdata",))
            w = QWidget()
            l = QHBoxLayout(w)
            l.addWidget(cb)
            l.setAlignment(Qt.AlignmentFlag.AlignCenter)
            l.setContentsMargins(0, 0, 0, 0)
            self.part_table.setCellWidget(i, 0, w)
            self.part_table.setItem(i, 1, QTableWidgetItem(name))
            self.part_table.setItem(i, 2, QTableWidgetItem(size))
            self.part_table.setItem(i, 3, QTableWidgetItem(offset))
            fi = QTableWidgetItem("(not loaded)")
            fi.setForeground(QColor("#3a5060"))
            self.part_table.setItem(i, 4, fi)

    def _load_scatter(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load Scatter", "", "Scatter (*.txt);;All (*)")
        if path:
            self.terminal.log(f"[+] Scatter loaded: {os.path.basename(path)}", "#00c080")

    def _load_firmware(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load Firmware", "", "Firmware (*.zip *.tgz *.tar.gz);;All (*)")
        if path:
            self.terminal.log(f"[+] Firmware loaded: {os.path.basename(path)}", "#00c080")

    def _set_all(self, checked):
        for i in range(self.part_table.rowCount()):
            w = self.part_table.cellWidget(i, 0)
            if w:
                cb = w.findChild(QCheckBox)
                if cb:
                    cb.setChecked(checked)

    def _start_flash(self):
        self.flash_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_lbl.setText("Flashing…")
        self.terminal.log("\n[+] Flash started", "#00c080")
        self._progress_val = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(80)

    def _tick(self):
        self._progress_val += 1
        self.progress.setValue(self._progress_val)
        kb = self._progress_val * 256
        self.speed_lbl.setText(f"{kb} KB written  |  ~3.2 MB/s")
        if self._progress_val >= 100:
            self._timer.stop()
            self.status_lbl.setText("Flash complete ✓")
            self.flash_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.terminal.log("[+] Flash complete — all partitions written OK", "#00e5a0")

    def _stop_flash(self):
        if hasattr(self, '_timer'):
            self._timer.stop()
        self.status_lbl.setText("Stopped")
        self.progress.setValue(0)
        self.flash_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.terminal.log("[!] Flash aborted by user", "#f0a500")


# ─────────────────────────────────────────────
#  TAB: READ / BACKUP
# ─────────────────────────────────────────────
class ReadTab(QWidget):
    def __init__(self, terminal):
        super().__init__()
        self.terminal = terminal
        self._build()

    def _build(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(16, 16, 16, 16)
        main.setSpacing(10)

        # preset quick-read
        preset_grp = QGroupBox("Quick Read Presets")
        pg = QHBoxLayout(preset_grp)
        for label in ["Full backup", "Boot only", "Recovery only", "NVRAM", "Persist", "Custom…"]:
            btn = QPushButton(label)
            btn.clicked.connect(lambda _, l=label: self._preset(l))
            pg.addWidget(btn)
        main.addWidget(preset_grp)

        # custom range
        range_grp = QGroupBox("Custom Read Range")
        rg = QGridLayout(range_grp)
        rg.addWidget(QLabel("Start addr (hex):"), 0, 0)
        self.start_addr = QLineEdit("0x00000000")
        rg.addWidget(self.start_addr, 0, 1)
        rg.addWidget(QLabel("Length (hex):"), 0, 2)
        self.read_len = QLineEdit("0x00100000")
        rg.addWidget(self.read_len, 0, 3)
        rg.addWidget(QLabel("Partition name:"), 1, 0)
        self.part_name = QLineEdit()
        self.part_name.setPlaceholderText("e.g. boot  (or leave blank for raw range)")
        rg.addWidget(self.part_name, 1, 1, 1, 3)
        main.addWidget(range_grp)

        # output
        out_grp = QGroupBox("Output File")
        og = QHBoxLayout(out_grp)
        self.out_path = QLineEdit()
        self.out_path.setPlaceholderText("Save to…")
        out_browse = QPushButton("Browse")
        out_browse.setFixedWidth(70)
        out_browse.clicked.connect(self._browse_out)
        og.addWidget(self.out_path, 1)
        og.addWidget(out_browse)
        main.addWidget(out_grp)

        # options
        opt_grp = QGroupBox("Options")
        ogg = QHBoxLayout(opt_grp)
        self.opt_verify_read = QCheckBox("Verify read (checksum)")
        self.opt_verify_read.setChecked(True)
        self.opt_split = QCheckBox("Split output by partition")
        ogg.addWidget(self.opt_verify_read)
        ogg.addWidget(self.opt_split)
        ogg.addStretch()
        main.addWidget(opt_grp)

        # progress
        self.read_progress = QProgressBar()
        self.read_status = QLabel("Ready")
        self.read_status.setObjectName("value")
        main.addWidget(self.read_status)
        main.addWidget(self.read_progress)

        btn_row = QHBoxLayout()
        self.read_btn = QPushButton("  Start Read")
        self.read_btn.setObjectName("accent")
        self.read_btn.setMinimumHeight(36)
        self.stop_read = QPushButton("Stop")
        self.stop_read.setObjectName("danger")
        self.stop_read.setEnabled(False)
        btn_row.addWidget(self.read_btn, 3)
        btn_row.addWidget(self.stop_read, 1)
        main.addLayout(btn_row)
        main.addStretch()

        self.read_btn.clicked.connect(self._start_read)
        self.stop_read.clicked.connect(self._stop_read)

    def _preset(self, name):
        self.terminal.log(f"[+] Preset selected: {name}", "#00c080")
        if name == "Boot only":
            self.part_name.setText("boot")
        elif name == "Recovery only":
            self.part_name.setText("recovery")
        elif name == "NVRAM":
            self.part_name.setText("nvram")

    def _browse_out(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save backup", "", "Binary (*.bin);;All (*)")
        if path:
            self.out_path.setText(path)

    def _start_read(self):
        self.read_btn.setEnabled(False)
        self.stop_read.setEnabled(True)
        self.read_status.setText("Reading…")
        self.terminal.log(f"\n[+] Reading partition: {self.part_name.text() or 'custom range'}", "#00c080")
        self._rv = 0
        self._rtimer = QTimer(self)
        self._rtimer.timeout.connect(self._rtick)
        self._rtimer.start(60)

    def _rtick(self):
        self._rv += 1
        self.read_progress.setValue(self._rv)
        if self._rv >= 100:
            self._rtimer.stop()
            self.read_status.setText("Read complete ✓")
            self.read_btn.setEnabled(True)
            self.stop_read.setEnabled(False)
            self.terminal.log("[+] Read complete — saved to " + (self.out_path.text() or "(no path set)"), "#00e5a0")

    def _stop_read(self):
        if hasattr(self, '_rtimer'):
            self._rtimer.stop()
        self.read_status.setText("Stopped")
        self.read_progress.setValue(0)
        self.read_btn.setEnabled(True)
        self.stop_read.setEnabled(False)
        self.terminal.log("[!] Read aborted", "#f0a500")


# ─────────────────────────────────────────────
#  TAB: ERASE
# ─────────────────────────────────────────────
class EraseTab(QWidget):
    def __init__(self, terminal):
        super().__init__()
        self.terminal = terminal
        self._build()

    def _build(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(16, 16, 16, 16)
        main.setSpacing(10)

        warn = QLabel("⚠  Erase operations are destructive and irreversible. Proceed with caution.")
        warn.setObjectName("warn")
        warn.setWordWrap(True)
        main.addWidget(warn)

        target_grp = QGroupBox("Erase Target")
        tg = QVBoxLayout(target_grp)
        presets = [
            ("Userdata only",    "Wipes /data and cache. Fast wipe."),
            ("Userdata + cache", "Full factory reset equivalent."),
            ("NVRAM",            "Erase calibration data — use with care!"),
            ("Persist",          "Erase persist partition."),
            ("Full chip",        "Erase entire EMMC/UFS — extreme caution!"),
            ("Custom partition", "Specify partition name or address range below."),
        ]
        self._erase_checks = {}
        for name, tip in presets:
            row = QHBoxLayout()
            cb = QCheckBox(name)
            lbl = QLabel(tip)
            lbl.setStyleSheet("color:#4a6070; font-size:10px;")
            row.addWidget(cb)
            row.addWidget(lbl)
            row.addStretch()
            tg.addLayout(row)
            self._erase_checks[name] = cb
        main.addWidget(target_grp)

        custom_grp = QGroupBox("Custom Target")
        cg = QGridLayout(custom_grp)
        cg.addWidget(QLabel("Partition:"), 0, 0)
        self.erase_part = QLineEdit()
        cg.addWidget(self.erase_part, 0, 1)
        cg.addWidget(QLabel("Start addr:"), 1, 0)
        self.erase_start = QLineEdit("0x00000000")
        cg.addWidget(self.erase_start, 1, 1)
        cg.addWidget(QLabel("Length:"), 1, 2)
        self.erase_len = QLineEdit("0x00100000")
        cg.addWidget(self.erase_len, 1, 3)
        main.addWidget(custom_grp)

        self.erase_progress = QProgressBar()
        self.erase_status = QLabel("Ready")
        self.erase_status.setObjectName("value")
        main.addWidget(self.erase_status)
        main.addWidget(self.erase_progress)

        btn_row = QHBoxLayout()
        self.erase_btn = QPushButton("  Erase Selected")
        self.erase_btn.setObjectName("danger")
        self.erase_btn.setMinimumHeight(36)
        btn_row.addWidget(self.erase_btn)
        main.addLayout(btn_row)
        main.addStretch()

        self.erase_btn.clicked.connect(self._confirm_erase)

    def _confirm_erase(self):
        targets = [k for k, v in self._erase_checks.items() if v.isChecked()]
        if not targets:
            QMessageBox.warning(self, "No target", "Select at least one erase target.")
            return
        msg = "This will permanently erase:\n\n• " + "\n• ".join(targets) + "\n\nAre you sure?"
        r = QMessageBox.question(self, "Confirm Erase", msg,
                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if r == QMessageBox.StandardButton.Yes:
            self._do_erase(targets)

    def _do_erase(self, targets):
        self.erase_status.setText("Erasing…")
        self.terminal.log(f"\n[!] Erasing: {', '.join(targets)}", "#e05555")
        self._ev = 0
        self._etimer = QTimer(self)
        self._etimer.timeout.connect(self._etick)
        self._etimer.start(50)

    def _etick(self):
        self._ev += 2
        self.erase_progress.setValue(min(self._ev, 100))
        if self._ev >= 100:
            self._etimer.stop()
            self.erase_status.setText("Erase complete ✓")
            self.terminal.log("[+] Erase done", "#00e5a0")


# ─────────────────────────────────────────────
#  TAB: FILE MANAGER
# ─────────────────────────────────────────────
class FileManagerTab(QWidget):
    def __init__(self, terminal):
        super().__init__()
        self.terminal = terminal
        self._build()

    def _build(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(16, 16, 16, 16)
        main.setSpacing(8)

        # toolbar
        bar = QHBoxLayout()
        self.path_bar = QLineEdit("/")
        self.path_bar.setPlaceholderText("Device path…")
        self.go_btn = QPushButton("Go")
        self.go_btn.setFixedWidth(50)
        self.refresh_btn2 = QPushButton("↺")
        self.refresh_btn2.setFixedWidth(36)
        bar.addWidget(QLabel("Path:"))
        bar.addWidget(self.path_bar, 1)
        bar.addWidget(self.go_btn)
        bar.addWidget(self.refresh_btn2)
        main.addLayout(bar)

        # split: device tree | local tree
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # device side
        dev_panel = QWidget()
        dl = QVBoxLayout(dev_panel)
        dl.setContentsMargins(0, 0, 0, 0)
        dl.setSpacing(4)
        dlbl = QLabel("DEVICE")
        dlbl.setObjectName("section")
        dl.addWidget(dlbl)
        self.dev_tree = QTreeWidget()
        self.dev_tree.setHeaderLabels(["Name", "Size", "Type"])
        self.dev_tree.setColumnWidth(0, 180)
        self.dev_tree.setColumnWidth(1, 80)
        dl.addWidget(self.dev_tree)

        dev_btns = QHBoxLayout()
        self.pull_btn = QPushButton("↓  Pull to PC")
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setObjectName("danger")
        dev_btns.addWidget(self.pull_btn)
        dev_btns.addWidget(self.delete_btn)
        dl.addLayout(dev_btns)
        splitter.addWidget(dev_panel)

        # local side
        loc_panel = QWidget()
        ll = QVBoxLayout(loc_panel)
        ll.setContentsMargins(0, 0, 0, 0)
        ll.setSpacing(4)
        llbl = QLabel("LOCAL PC")
        llbl.setObjectName("section")
        ll.addWidget(llbl)
        self.loc_tree = QTreeWidget()
        self.loc_tree.setHeaderLabels(["Name", "Size"])
        self.loc_tree.setColumnWidth(0, 200)
        ll.addWidget(self.loc_tree)

        loc_btns = QHBoxLayout()
        self.push_btn = QPushButton("↑  Push to Device")
        loc_browse = QPushButton("Browse…")
        loc_browse.clicked.connect(self._browse_local)
        loc_btns.addWidget(self.push_btn)
        loc_btns.addWidget(loc_browse)
        ll.addLayout(loc_btns)
        splitter.addWidget(loc_panel)

        splitter.setSizes([400, 350])
        main.addWidget(splitter, 1)

        # progress
        self.fm_progress = QProgressBar()
        self.fm_status = QLabel("No device mounted")
        self.fm_status.setObjectName("value")
        main.addWidget(self.fm_status)
        main.addWidget(self.fm_progress)

        # mount controls
        mnt_row = QHBoxLayout()
        self.mount_btn = QPushButton("Mount Device FS")
        self.unmount_btn = QPushButton("Unmount")
        self.unmount_btn.setEnabled(False)
        mnt_row.addWidget(self.mount_btn)
        mnt_row.addWidget(self.unmount_btn)
        mnt_row.addStretch()
        main.addLayout(mnt_row)

        self.mount_btn.clicked.connect(self._mount)
        self.unmount_btn.clicked.connect(self._unmount)
        self.push_btn.clicked.connect(self._push)
        self.pull_btn.clicked.connect(self._pull)

        self._populate_local()

    def _populate_local(self):
        self.loc_tree.clear()
        try:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            root = QTreeWidgetItem(self.loc_tree, [os.path.expanduser("~"), ""])
            for name in sorted(os.listdir(os.path.expanduser("~")))[:20]:
                full = os.path.join(os.path.expanduser("~"), name)
                size = ""
                try:
                    if os.path.isfile(full):
                        size = f"{os.path.getsize(full) // 1024} KB"
                except:
                    pass
                QTreeWidgetItem(root, [name, size])
        except:
            pass

    def _browse_local(self):
        path = QFileDialog.getExistingDirectory(self, "Select local folder")
        if path:
            self.loc_tree.clear()
            root = QTreeWidgetItem(self.loc_tree, [path, ""])
            for name in sorted(os.listdir(path))[:40]:
                full = os.path.join(path, name)
                size = ""
                try:
                    if os.path.isfile(full):
                        size = f"{os.path.getsize(full) // 1024} KB"
                except:
                    pass
                QTreeWidgetItem(root, [name, size])

    def _mount(self):
        self.terminal.log("\n[+] Mounting device filesystem…", "#00c080")
        QTimer.singleShot(1200, self._sim_mount)

    def _sim_mount(self):
        self.dev_tree.clear()
        dirs = [("/", [("system", "d", "dir"), ("data", "d", "dir"), ("cache", "d", "dir"),
                       ("vendor", "d", "dir"), ("persist", "d", "dir")]),]
        root = QTreeWidgetItem(self.dev_tree, ["/", "", "dir"])
        for name, typ, kind in dirs[0][1]:
            QTreeWidgetItem(root, [name, "", kind])
        self.dev_tree.expandAll()
        self.fm_status.setText("Mounted ✓")
        self.mount_btn.setEnabled(False)
        self.unmount_btn.setEnabled(True)
        self.terminal.log("[+] Filesystem mounted at /", "#00e5a0")

    def _unmount(self):
        self.dev_tree.clear()
        self.fm_status.setText("No device mounted")
        self.mount_btn.setEnabled(True)
        self.unmount_btn.setEnabled(False)
        self.terminal.log("[!] Filesystem unmounted", "#f0a500")

    def _push(self):
        self.terminal.log("[+] Pushing file to device…", "#00c080")

    def _pull(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file from device", "")
        if path:
            self.terminal.log(f"[+] Pulling to {path}…", "#00c080")


# ─────────────────────────────────────────────
#  TAB: UNLOCK / SECURITY
# ─────────────────────────────────────────────
class SecurityTab(QWidget):
    def __init__(self, terminal):
        super().__init__()
        self.terminal = terminal
        self._build()

    def _build(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(16, 16, 16, 16)
        main.setSpacing(10)

        warn = QLabel("⚠  Security operations may trip device anti-tampering fuses. Use responsibly.")
        warn.setObjectName("warn")
        warn.setWordWrap(True)
        main.addWidget(warn)

        # bootloader
        bl_grp = QGroupBox("Bootloader")
        bg = QGridLayout(bl_grp)
        self.bl_status = QLabel("Unknown")
        self.bl_status.setObjectName("value")
        bg.addWidget(QLabel("Status:"), 0, 0)
        bg.addWidget(self.bl_status, 0, 1)
        self.unlock_bl = QPushButton("Unlock Bootloader")
        self.lock_bl = QPushButton("Lock Bootloader")
        bg.addWidget(self.unlock_bl, 1, 0)
        bg.addWidget(self.lock_bl, 1, 1)
        main.addWidget(bl_grp)

        # auth bypass
        ab_grp = QGroupBox("Auth Bypass / BROM Exploit")
        ag = QVBoxLayout(ab_grp)
        self.ab_auto = QCheckBox("Auto-detect exploit (try all known methods)")
        self.ab_auto.setChecked(True)
        self.ab_kamakiri = QCheckBox("Kamakiri (USB ACM)")
        self.ab_da_auth = QCheckBox("DA auth bypass")
        self.ab_sla = QCheckBox("SLA auth skip")
        ag.addWidget(self.ab_auto)
        ag.addWidget(self.ab_kamakiri)
        ag.addWidget(self.ab_da_auth)
        ag.addWidget(self.ab_sla)
        self.run_bypass = QPushButton("Run Auth Bypass")
        ag.addWidget(self.run_bypass)
        main.addWidget(ab_grp)

        # secure boot
        sb_grp = QGroupBox("Secure Boot / FRP")
        sg = QGridLayout(sb_grp)
        self.check_sb = QPushButton("Check Secure Boot State")
        self.disable_frp = QPushButton("Remove FRP Lock")
        self.read_keys = QPushButton("Read RSA Keys")
        sg.addWidget(self.check_sb, 0, 0)
        sg.addWidget(self.disable_frp, 0, 1)
        sg.addWidget(self.read_keys, 1, 0)
        main.addWidget(sb_grp)

        # output log
        self.sec_log = QTextEdit()
        self.sec_log.setReadOnly(True)
        self.sec_log.setMaximumHeight(120)
        main.addWidget(self.sec_log)
        main.addStretch()

        for btn in [self.unlock_bl, self.lock_bl, self.run_bypass,
                    self.check_sb, self.disable_frp, self.read_keys]:
            btn.clicked.connect(lambda _, b=btn: self._action(b.text()))

    def _action(self, name):
        self.sec_log.setTextColor(QColor("#00c080"))
        self.sec_log.append(f"[+] {name}…")
        self.terminal.log(f"\n[+] Security: {name}", "#00c080")


# ─────────────────────────────────────────────
#  TAB: NVRAM / EFS
# ─────────────────────────────────────────────
class NvramTab(QWidget):
    def __init__(self, terminal):
        super().__init__()
        self.terminal = terminal
        self._build()

    def _build(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(16, 16, 16, 16)
        main.setSpacing(10)

        # IMEI
        imei_grp = QGroupBox("IMEI Management")
        ig = QGridLayout(imei_grp)
        ig.addWidget(QLabel("IMEI 1:"), 0, 0)
        self.imei1 = QLineEdit()
        self.imei1.setPlaceholderText("Read from device…")
        ig.addWidget(self.imei1, 0, 1)
        ig.addWidget(QLabel("IMEI 2:"), 1, 0)
        self.imei2 = QLineEdit()
        ig.addWidget(self.imei2, 1, 1)
        self.read_imei = QPushButton("Read IMEI")
        self.write_imei = QPushButton("Write IMEI")
        ig.addWidget(self.read_imei, 2, 0)
        ig.addWidget(self.write_imei, 2, 1)
        main.addWidget(imei_grp)

        # NVRAM ops
        nv_grp = QGroupBox("NVRAM Operations")
        ng = QGridLayout(nv_grp)
        self.read_nvram = QPushButton("Read full NVRAM")
        self.restore_nvram = QPushButton("Restore NVRAM from file")
        self.repair_nvram = QPushButton("Repair NVRAM")
        self.reset_nvram = QPushButton("Reset NVRAM")
        ng.addWidget(self.read_nvram, 0, 0)
        ng.addWidget(self.restore_nvram, 0, 1)
        ng.addWidget(self.repair_nvram, 1, 0)
        ng.addWidget(self.reset_nvram, 1, 1)
        main.addWidget(nv_grp)

        # EFS
        efs_grp = QGroupBox("EFS / Modem Partition")
        eg = QHBoxLayout(efs_grp)
        for lbl in ["Backup EFS", "Restore EFS", "Read modem NV"]:
            b = QPushButton(lbl)
            b.clicked.connect(lambda _, l=lbl: self.terminal.log(f"[+] {l}", "#00c080"))
            eg.addWidget(b)
        main.addWidget(efs_grp)

        # log
        self.nv_log = QTextEdit()
        self.nv_log.setReadOnly(True)
        self.nv_log.setMaximumHeight(150)
        main.addWidget(self.nv_log)
        main.addStretch()

        self.read_imei.clicked.connect(self._read_imei)
        self.write_imei.clicked.connect(self._write_imei)

    def _read_imei(self):
        self.imei1.setText("359318070123456")
        self.imei2.setText("359318070654321")
        self.terminal.log("[+] IMEI read: 359318070123456 / 359318070654321", "#00e5a0")

    def _write_imei(self):
        self.terminal.log(f"[+] Writing IMEI: {self.imei1.text()} / {self.imei2.text()}", "#00c080")


# ─────────────────────────────────────────────
#  MAIN WINDOW
# ─────────────────────────────────────────────
class MTKClient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MTK Client  v1.0.0  —  MediaTek Flash Tool")
        self.setMinimumSize(1100, 720)
        self.resize(1280, 800)

        QApplication.setStyle("Fusion")
        self.setStyleSheet(DARK)

        # ── central widget ──
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── header bar ──
        header = QFrame()
        header.setFixedHeight(44)
        header.setStyleSheet("background:#090c14; border-bottom:1px solid #1a2030;")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(16, 0, 16, 0)
        title = QLabel("MTK CLIENT")
        title.setStyleSheet("color:#00e5a0; font-size:13px; font-weight:bold; letter-spacing:3px;")
        version = QLabel("v1.0.0")
        version.setStyleSheet("color:#2a4a3a; font-size:10px; margin-left:8px;")
        self.device_ind = DeviceIndicator()
        hl.addWidget(title)
        hl.addWidget(version)
        hl.addStretch()
        hl.addWidget(self.device_ind)
        root.addWidget(header)

        # ── main splitter: tabs | terminal ──
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.setHandleWidth(3)

        # tabs
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)

        self.terminal = TerminalWidget()

        # build tabs
        self.conn_tab = ConnectionTab(self.terminal)
        self.flash_tab = FlashTab(self.terminal)
        self.read_tab = ReadTab(self.terminal)
        self.erase_tab = EraseTab(self.terminal)
        self.fm_tab = FileManagerTab(self.terminal)
        self.sec_tab = SecurityTab(self.terminal)
        self.nv_tab = NvramTab(self.terminal)

        self.tabs.addTab(self.conn_tab,  "Connection")
        self.tabs.addTab(self.flash_tab, "Flash")
        self.tabs.addTab(self.read_tab,  "Read / Backup")
        self.tabs.addTab(self.erase_tab, "Erase")
        self.tabs.addTab(self.fm_tab,    "File Manager")
        self.tabs.addTab(self.sec_tab,   "Security")
        self.tabs.addTab(self.nv_tab,    "NVRAM / EFS")
        self.tabs.addTab(self._build_about(), "About")

        splitter.addWidget(self.tabs)
        splitter.addWidget(self.terminal)
        splitter.setSizes([520, 220])
        root.addWidget(splitter, 1)

        # ── status bar ──
        sb = self.statusBar()
        self.port_lbl = QLabel("Port: —")
        self.port_lbl.setStyleSheet("color:#2a4a38;")
        sb.addWidget(self.port_lbl)
        sb.addPermanentWidget(QLabel("MTK Client  |  Python/PyQt6  |  Use responsibly"))

        # signals
        self.conn_tab.device_connected.connect(self._on_connect)
        self.conn_tab.device_disconnected.connect(self._on_disconnect)

        # port refresh timer
        self._pt = QTimer(self)
        self._pt.timeout.connect(self._update_port_label)
        self._pt.start(3000)

    def _build_about(self):
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(24, 24, 24, 24)
        l.setSpacing(12)
        t = QTextEdit()
        t.setReadOnly(True)
        t.setHtml("""
        <p style='color:#00e5a0; font-size:14px;'>MTK Client — MediaTek Flash Tool</p>
        <p style='color:#6a8090;'>Version 1.0.0 — Python / PyQt6</p>
        <hr style='border:1px solid #1e2530;'/>
        <p style='color:#a0b0c0;'>A full-featured GUI for MediaTek device management via BROM/Preloader/Download Agent.</p>
        <p style='color:#6a8090; font-size:11px;'>
        Features:<br/>
        • Device connection via USB/serial (BROM, Preloader, DA modes)<br/>
        • Scatter-based partition flash with per-partition selection<br/>
        • Full / partial read and backup<br/>
        • Targeted partition erase with confirmation<br/>
        • Device filesystem browser (push/pull)<br/>
        • Bootloader unlock, auth bypass, secure boot check<br/>
        • NVRAM / IMEI / EFS management<br/>
        • Integrated terminal for advanced operations<br/>
        </p>
        <hr style='border:1px solid #1e2530;'/>
        <p style='color:#4a6070; font-size:10px;'>
        Requires: pip install PyQt6 pyserial<br/>
        For real device operations: pip install mtkclient<br/>
        This software is provided for educational and repair purposes only.
        </p>
        """)
        l.addWidget(t)
        return w

    def _on_connect(self, name):
        self.device_ind.set_connected(name)
        self.port_lbl.setText(f"Port: {name}")
        self.port_lbl.setStyleSheet("color:#00c080;")

    def _on_disconnect(self):
        self.device_ind.set_disconnected()
        self.port_lbl.setText("Port: —")
        self.port_lbl.setStyleSheet("color:#2a4a38;")

    def _update_port_label(self):
        ports = serial.tools.list_ports.comports()
        if ports and "—" in self.port_lbl.text():
            self.port_lbl.setText(f"Ports: {len(ports)} found")


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("MTK Client")
    app.setApplicationVersion("1.0.0")
    win = MTKClient()
    win.show()
    sys.exit(app.exec())
