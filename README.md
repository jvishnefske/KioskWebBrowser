# KioskWebBrowser

A lightweight, fullscreen web browser for kiosk deployments. Built with Python and Qt5/WebKit, it provides a locked-down browsing experience suitable for information displays, digital signage, and interactive kiosks.

## Features

- Fullscreen mode for immersive kiosk displays
- URL loading from command line or local HTML files
- Escape key to exit (configurable)
- Two backend options: PySide2/QtWebEngine or GTK3/WebKit2
- Developer mode for debugging (GTK version)

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run with default demo page
python qtwebwindow.py

# Run with custom URL
python qtwebwindow.py --url https://example.com
```

## Requirements

- Python 3.6+
- PySide2 with QtWebEngine (for qtwebwindow.py)
- PyGObject with WebKit2 (for window.py)

## Usage

### Qt/PySide2 Version (qtwebwindow.py)

```bash
python qtwebwindow.py [--url URL] [--debug]
```

### GTK/WebKit2 Version (window.py)

```bash
python window.py [--url URL] [--developer]
```

## License

See fonts/OFL.txt for B612 font license.
