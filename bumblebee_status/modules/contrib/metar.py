# pylint: disable=C0111,R0903

import re
import requests

import core.module
import core.widget
import core.input
import core.decorators


def fetch(url):
    try:
        return requests.get(url).text

    except:
        return None


class Module(core.module.Module):
    @core.decorators.every(minutes=5)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.output))

        self.provider = self.parameter("provider")

        self.airports = self.parameter("airports").split(",")
        self.airports_index = 0

        core.input.register(
            self, button=core.input.LEFT_MOUSE, cmd=self.next_airport
        )

    def next_airport(self, event):
        self.airports_index += 1

        if self.airports_index == len(self.airports):
            self.airports_index = 0

    def update(self):
        metar = fetch(self.provider + "/" + self.airports[self.airports_index])

        if metar is None:
            self.data = ""
        else:
            self.data = metar

    def output(self, widget):
        return self.data

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
