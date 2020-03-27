#!/usr/bin/env python3

import os
import requests
from datetime import datetime
import logzero
import logging

import env
# import env_dev as env

from cloudflare_api import CloudflareApi


class UpdateDns:
    zone_name = 'hjb.io'
    record_name = 'home.hjb.io'

    last_check_date = None
    zone_id = None
    dns_id = None

    api = None

    bot_url = "https://api.telegram.org/bot{}".format(env.bot_key)

    logger = None

    def __init__(self):
        self.logger = logzero.logger
        if os.environ.get('PRODUCTION', 0):
            logzero.loglevel(logging.INFO)
        else:
            logzero.loglevel(logging.DEBUG)

        self.api = CloudflareApi(self.logger)

    def send_telegram_message(self, message):

        url = self.bot_url + '/sendMessage?chat_id={}&text={}'.format(env.chat_id, message)
        requests.get(url)

    def on_execute(self):
        now = (str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.logger.info("Update started on: {}".format(now))

        if not self.last_check_date or self.last_check_date != datetime.now().date():
            self.logger.debug("Updating DNS and Zone IDs")
            self.last_check_date = datetime.now().date()

            # Find zone id
            self.zone_id = self.api.find_zone_id(self.zone_name)
            self.logger.debug("Zone ID: {}".format(self.zone_id))

            # Find DNS id
            self.dns_id = self.api.find_dns_id(self.zone_id, self.record_name)
            self.logger.debug("DNS ID: {}".format(self.dns_id))

        message = self.api.update_dns(self.zone_id, self.dns_id)
        self.logger.debug("Message: {}".format(message))

        if message:
            self.send_telegram_message(message)


if __name__ == '__main__':
    app = UpdateDns()
    app.on_execute()
