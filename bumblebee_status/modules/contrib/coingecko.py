# pylint: disable=C0111,R0903

import decimal
import requests

import core.module
import core.widget
import core.input
import core.decorators


def fetch_prices(coins, currency):
    try:
        return (
            requests
                .get("https://api.coingecko.com/api/v3/simple/price?ids=" + ",".join(coins) + "&include_24hr_change=true&vs_currencies=" + currency)
                .json()
        )
    except:
        return None

def get_price_from_response(response, coin, currency):
    try:
        return (
            decimal.Decimal(response[coin][currency]),
            decimal.Decimal(response[coin][currency + "_24h_change"])
        )
    except:
        return (None, 0)


class Module(core.module.Module):
    @core.decorators.every(minutes=1)
    def __init__(self, config, theme):
        super().__init__(config, theme, [])

        self.coins = self.parameter("coins", "bitcoin,ethereum").split(",")
        self.currency = "usd"

        self.format = self.parameter("format", "{coin} ${price} ({price_24hr_change}%)")

        for coin in self.coins:
            widget = self.add_widget(full_text=self.price_output, name=coin)

        self.price = {}
        self.price_24hr_change = {}

        self.update_prices()

    def state(self, widget):
        coin = widget.name
        coin_price_24hr_change = self.price_24hr_change[coin]

        # no change
        if coin_price_24hr_change == 0:
            return []

        if coin_price_24hr_change < 0:
            return ["down"]

        return ["up"]

    def update(self):
        self.update_prices()

    def update_prices(self):
        response = fetch_prices(self.coins, self.currency)

        for coin in self.coins:
            price, price_24hr_change = get_price_from_response(response, coin, self.currency)

            self.price[coin] = price
            self.price_24hr_change[coin] = price_24hr_change

    def price_output(self, widget):
        coin = widget.name

        if self.price[coin] is None:
            return (
                "{coin} ?"
                    .replace("{coin}", coin)
            )

        sign = "+" if self.price_24hr_change[coin] > 0 else ""

        return (
            self.format
                .replace("{coin}", coin)
                .replace("{price}", "{:,.2f}".format(self.price[coin]))
                .replace("{price_24hr_change}", sign + "{:,.2f}".format(self.price_24hr_change[coin]))
        )

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
