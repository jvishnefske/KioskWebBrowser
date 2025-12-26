# KioskWebBrowser Design Document

## Overview

KioskWebBrowser is a fullscreen web browser application designed for kiosk deployments where a locked-down, single-purpose browsing experience is required.

## MVP Functional Requirements

### Core Requirements

- [x] FR-001: Display web content in fullscreen mode
- [x] FR-002: Load URL from command line argument (--url)
- [x] FR-003: Load local HTML files when no URL scheme provided
- [x] FR-004: Exit application via Escape key
- [x] FR-005: Handle SIGINT signal for graceful shutdown
- [x] FR-006: Default to bundled demo page (kiosk.html) when no URL specified

### User Interface Requirements

- [x] FR-007: Window starts maximized/fullscreen
- [x] FR-008: No browser chrome (address bar, navigation buttons)
- [x] FR-009: Keyboard input handling for exit key

### Configuration Requirements

- [x] FR-010: Debug/developer mode flag for troubleshooting
- [x] FR-011: Automatic URL scheme detection and prepending

## Architecture

### Components

1. **qtwebwindow.py** - PySide2/QtWebEngine implementation
   - MyQtKiosk class extending QMainWindow
   - QWebEngineView for rendering
   - argparse for CLI argument handling

2. **window.py** - GTK3/WebKit2 implementation
   - FullScreenBrowser class extending Gtk.Window
   - WebKit2.WebView for rendering
   - Extended WebKit settings for kiosk use

3. **kiosk.html** - Demo page with clock and FPS counter

### Design Decisions

- Two backend implementations for flexibility across different Linux environments
- No dependency on complex configuration files
- Simple CLI interface for integration with startup scripts
- Escape key exit ensures physical access is required to close

## Non-Functional Requirements

- NFR-001: Minimal memory footprint suitable for embedded systems
- NFR-002: Fast startup time for kiosk boot scenarios
- NFR-003: Compatibility with OpenEmbedded/Yocto Linux distributions

## Future Considerations

- Configuration file support for persistent settings
- Remote management capabilities
- Multi-monitor support
- Input device filtering/restriction
