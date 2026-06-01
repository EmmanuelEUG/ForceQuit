#!/usr/bin/python3
import sys
import json
import subprocess
import psutil
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QListWidget, QListWidgetItem, 
                             QPushButton, QLabel, QFrame)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon

class AppItemWidget(QWidget):
    def __init__(self, app_name, pid, on_kill_callback, parent=None):
        super().__init__(parent)
        self.pid = pid
        self.on_kill = on_kill_callback
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # App Info
        info_layout = QVBoxLayout()
        self.name_label = QLabel(app_name)
        self.name_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff;")
        self.pid_label = QLabel(f"PID: {pid}")
        self.pid_label.setStyleSheet("color: #aaaaaa; font-size: 11px;")
        
        info_layout.addWidget(self.name_label)
        info_layout.addWidget(self.pid_label)
        layout.addLayout(info_layout)
        
        layout.addStretch()
        
        # Kill Button
        self.kill_btn = QPushButton("Forzar Cierre")
        self.kill_btn.setFixedSize(120, 35)
        self.kill_btn.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: white;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f44336;
            }
            QPushButton:pressed {
                background-color: #b71c1c;
            }
        """)
        self.kill_btn.clicked.connect(self.handle_kill)
        layout.addWidget(self.kill_btn)

    def handle_kill(self):
        self.on_kill(self.pid)

class ForceQuitApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Force Quit - Hyprland")
        self.setMinimumSize(500, 600)
        self.setStyleSheet("background-color: #1e1e2e; color: #cdd6f4;")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        
        # Header
        header = QLabel("Aplicaciones Abiertas")
        header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header.setStyleSheet("margin: 10px; color: #89b4fa;")
        self.main_layout.addWidget(header)
        
        # Refresh Button
        self.refresh_btn = QPushButton("Actualizar Lista")
        self.refresh_btn.setFixedHeight(40)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #45475a;
                color: #cdd6f4;
                border-radius: 5px;
                margin: 0 10px 10px 10px;
            }
            QPushButton:hover {
                background-color: #585b70;
            }
        """)
        self.refresh_btn.clicked.connect(self.refresh_apps)
        self.main_layout.addWidget(self.refresh_btn)
        
        # App List
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListWidget {
                border: none;
                background-color: #181825;
                outline: none;
            }
            QListWidget::item {
                border-bottom: 1px solid #313244;
            }
            QListWidget::item:selected {
                background-color: #313244;
            }
        """)
        self.main_layout.addWidget(self.list_widget)
        
        self.refresh_apps()

    def get_hyprland_clients(self):
        try:
            result = subprocess.run(['hyprctl', 'clients', '-j'], capture_output=True, text=True)
            return json.loads(result.stdout)
        except Exception as e:
            print(f"Error getting clients: {e}")
            return []

    def refresh_apps(self):
        self.list_widget.clear()
        clients = self.get_hyprland_clients()
        
        # Group by PID to avoid duplicates
        apps = {}
        for client in clients:
            pid = client.get('pid')
            # Filter out entries without valid PIDs or empty classes
            if pid and pid > 0 and client.get('class'):
                if pid not in apps:
                    # Clean up the name
                    name = client.get('class', 'Unknown')
                    if not name or name == "":
                        name = client.get('title', 'Unknown Application')
                    apps[pid] = name

        for pid, name in apps.items():
            item = QListWidgetItem(self.list_widget)
            item_widget = AppItemWidget(name, pid, self.kill_process)
            item.setSizeHint(item_widget.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, item_widget)

    def kill_process(self, pid):
        try:
            process = psutil.Process(pid)
            # Kill children first
            for child in process.children(recursive=True):
                child.kill()
            process.kill()
            self.refresh_apps()
        except Exception as e:
            print(f"Failed to kill process {pid}: {e}")
            # Fallback to shell if psutil fails
            subprocess.run(['kill', '-9', str(pid)])
            self.refresh_apps()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ForceQuitApp()
    window.show()
    sys.exit(app.exec())
