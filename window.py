# gobject fullscreen browser window 
import pathlib
import gi
gi.require_version('Gdk', '3.0')
gi.require_version('WebKit2', '4.0')
gi.require_version('Gtk', '3.0')
from urllib.parse import urlparse
import logging
import re
import signal
import argparse

#webkit2
from gi.repository import Gdk, Gtk, WebKit2


class FullScreenBrowser(Gtk.Window):
    def __init__(self, url=None, isDeveloper=False, closeKey=None):
        self.closeKey = closeKey
        Gtk.Window.__init__(self)
        self.set_default_size(800, 600)
        self.set_title("Fullscreen Browser")
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("destroy", Gtk.main_quit)
        self.connect("key-press-event", self.on_key_press)
        self.connect("button-press-event", self.on_button_press)
        self.connect("realize", self.on_realize)
        self.connect("unrealize", self.on_unrealize)
        # self.connect("screen-changed", self.on_screen_changed)
        # self.connect("window-state-event", self.on_window_state_event)
        # self.connect("motion-notify-event", self.on_motion_notify_event)
        # webkit 
        self.webkit = WebKit2.WebView()
        self.webkit.connect("load-changed", self.on_load_changed)
        self.webkit.connect("load-failed", self.on_load_failed)
        self.webkit.connect("resource-load-started", self.on_resource_load_started)
        self.webkit.connect("create", self.on_create)
        self.webkit.connect("context-menu", self.on_context_menu)
        self.webkit.connect("notify::title", self.on_title_changed)
        self.webkit.connect("notify::uri", self.on_uri_changed)
        self.webkit.connect("notify::estimated-load-progress", self.on_estimated_load_progress_changed)
        if url:
            self.webkit.load_uri(url)
        else:
            index_html = """<html><head><title>Hello World</title></head><body>Hello World</body></html>"""
            self.webkit.load_html(index_html, "file:///")
        # call destroy when SIGINT is received
        signal.signal(signal.SIGINT, self.close)
        # close on esc
        self.add_events(Gdk.EventMask.KEY_PRESS_MASK)
        self.connect("key-press-event", self.on_key_press)

        self.add(self.webkit)
        self.show_all()
        self.fullscreen()
        self.webkit.grab_focus()
        self.webkit.set_zoom_level(1.0)
        self.webkit.set_settings(self.webkit.get_settings())
        webkitSettings = self.webkit.get_settings()
        webkitSettings.set_enable_developer_extras(isDeveloper)
        webkitSettings.set_enable_dns_prefetching(True)
        webkitSettings.set_enable_frame_flattening(True)
        webkitSettings.set_enable_fullscreen(True)
        webkitSettings.set_enable_html5_database(True)
        webkitSettings.set_enable_html5_local_storage(True)
        webkitSettings.set_enable_hyperlink_auditing(True)
        webkitSettings.set_enable_java(False)
        webkitSettings.set_enable_javascript(True)
        webkitSettings.set_enable_mediasource(True)
        webkitSettings.set_enable_media_stream(True)
        webkitSettings.set_enable_offline_web_application_cache(True)
        webkitSettings.set_enable_page_cache(False)
        webkitSettings.set_enable_resizable_text_areas(True)
        webkitSettings.set_enable_site_specific_quirks(True)
        webkitSettings.set_enable_smooth_scrolling(True)
        webkitSettings.set_enable_spatial_navigation(True)
        webkitSettings.set_enable_webaudio(True)
        webkitSettings.set_enable_webgl(True)
        webkitSettings.set_enable_write_console_messages_to_stdout(True)
        webkitSettings.set_enable_xss_auditor(True)

        # disable right click menu
        settings = self.webkit.get_settings()
    def close(self):
        logging.info("closing.")
        self.destroy()
    def on_realize(self, widget):
        logging.info("on_realize")
    def on_unrealize(self, widget):
        logging.info("on_unrealize")
    def on_key_press(self, widget, event):
        logging.info("on_key_press")
        if event.keyval == self.closeKey:
            self.destroy()
    def on_button_press(self, widget, event):
        logging.info("on_button_press")
    def on_create(self, webview):
        logging.info("on_create")
    def on_context_menu(self, webview, context_menu, event, hit_test_result):
        logging.info("on_context_menu")
    def on_resource_load_started(self, webview, resource, request):
        logging.info("on_resource_load_started")
    def on_resource_load_finished(self, webview, resource, request):
        logging.info("on_resource_load_finished")
    def on_resource_load_failed(self, webview, resource, request, error):
        logging.info("on_resource_load_failed")
    def on_resource_response_received(self, webview, resource, response):
        logging.info("on_resource_response_received")
    def on_load_changed(self, webview, load_event):
        logging.info("on_load_changed")
    def on_load_failed(self, webview, load_event, failing_uri, error):
        logging.info("on_load_failed")
    def on_title_changed(self, webview, title):
        logging.info("on_title_changed")
    def on_uri_changed(self, webview, uri):
        logging.info("on_uri_changed")
    def on_estimated_load_progress_changed(self, webview, progress):
        logging.info("on_estimated_load_progress_changed")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='WebKit2 kiosk')
    # optional url
    parser.add_argument('--url', help='url to load', default=None)
    # optional developer mode
    parser.add_argument('--developer', help='developer mode', action='store_true')
    args = parser.parse_args()
    # create window
    if args.url:
        # prepend http:// if not present
        if not urlparse(args.url).scheme:
            # check if url is a file and it exists
            path = pathlib.Path(args.url)
            if path.is_file():
                # make file into a url
                args.url = f"file://{path.absolute()}"
                logging.info(f"url: {args.url}")
            else:
                logging.info("no scheme present, prepending http://")
                args.url = "http://" + args.url
    browser = FullScreenBrowser(url=args.url, isDeveloper=args.developer, closeKey=Gdk.KEY_Escape)
    # run minimized
    Gtk.main()
