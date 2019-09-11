#!/usr/bin/env python3

import os
import signal
import time
import threading
import random

import click
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk, AppIndicator3, GObject, GLib



class NightscoutSystray():

    ASSETS_DIR = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "assets",
        )
    )
    APP_NAME = "nightscout-systray"
    REFRESH_INTERVAL = 2

    def __init__(
        self,
        *,
        api_url,
        api_token,
    ):

        self.api_url = api_url
        self.api_token = api_token

        iconpath = os.path.join(
            self.ASSETS_DIR,
            "tint.png"
        )

        self.indicator = AppIndicator3.Indicator.new(
            self.APP_NAME,
            iconpath,
            AppIndicator3.IndicatorCategory.OTHER,
        )

        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())
        breakpoint()
        self.indicator.set_label(label="hello", guide='')

        self.update_thread = threading.Thread(target=self.update_loop)
        self.update_thread.setDaemon(True)
        self.update_thread.start()

    def update_loop(self):

        while True:
            time.sleep(self.REFRESH_INTERVAL)

            new_text = "{number} mmol/L".format(
                number=random.randrange(4, 7)
            )

            GLib.idle_add(
                self.indicator.set_label,
                new_text,
                self.APP_NAME,
                priority=GLib.PRIORITY_DEFAULT,
            )

    def create_menu(self):
        menu = Gtk.Menu()

        item_quit = Gtk.MenuItem(label='Quit')
        item_quit.connect('activate', self.stop)
        menu.append(item_quit)

        menu.show_all()

        return menu

    def stop(self, source):
        Gtk.main_quit()

@click.command()
@click.option(
    '--api_url',
    required=True,
    default=lambda: os.environ.get("NIGHTSCOUT_API_URL", None),
)
@click.option(
    '--api_token',
    required=True,
    default=lambda: os.environ.get("NIGHTSCOUT_API_TOKEN", None),
)
def main(*, api_url, api_token):
    nightscout_systray = NightscoutSystray(
        api_url=api_url,
        api_token=api_token,
    )
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()


if __name__ == "__main__":
    main()
