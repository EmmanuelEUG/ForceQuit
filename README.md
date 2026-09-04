# ForceQuit (Hyprland)

ForceQuit is a lightweight, efficient utility designed specifically for Hyprland users to quickly identify and terminate unresponsive or unwanted applications.

## Features

- **Hyprland Integration**: Uses `hyprctl` to accurately list all active window clients.
- **Smart Killing**: Leverages `psutil` to terminate processes along with their entire child process tree, ensuring no "zombie" processes are left behind.
- **Clean Interface**: A simple and intuitive UI built with PyQt6 that matches modern Linux aesthetics.
- **PID Tracking**: Displays PIDs for each application for precise process management.

## Installation

### Prerequisites

Ensure you have Python 3 installed and are running a Hyprland session.

### Dependencies

Install the required Python libraries:
```bash
pip install PyQt6 psutil
```

## Usage

Run the application using Python:
```bash
python main.py
```

Click "Refresh List" to update the current active windows and use the "Force Quit" button to terminate any application.

## Requirements

- **Python**: 3.x
- **Environment**: Hyprland
- **Tools**: `hyprctl` (part of Hyprland)

---
Simple, fast, and effective.
