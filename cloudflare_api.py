#!/usr/bin/env python3

import os
import requests
import logzero
import logging
from datetime import datetime
import json
from pprint import pprint
from urllib.parse import urlencode

import env
# import env_dev as env


class CloudflareApi:
    base_url = 'https://api.cloudflare.com/client/v4'

    # Headers to go with API requests
    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Key': env.api_key,
        'X-Auth-Email': env.api_email,
    }

    def __init__(self, logger=None):
        if logger:
            self.logger = logger
        else:
            self.logger = logzero.logger
            if os.environ.get('PRODUCTION', 0):
                logzero.loglevel(logging.INFO)
            else:
                logzero.loglevel(logging.DEBUG)

    # def get_telegram_updates(self):
    #     url = env.bot_url + '/getUpdates'
    #     print requests.get(url).text

    def update_dns(self, _zone_id, _dns_id):
        current_ip = requests.get('http://ip.42.pl/raw').text
        now = (str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        # Find current configured url from DNS
        url = '{}/zones/{}/dns_records/{}'.format(self.base_url, _zone_id, _dns_id)

        req = requests.get(url, headers=self.headers).json()['result']
        self.logger.debug(req)

        old_ip = {
            'content': req['content'],
            'type': req['type'],
            'name': req['name'],
        }

        # Check if ip has changed, update if so
        if old_ip['content'] != current_ip:
            self.logger.debug("Old IP: {} - Current IP: {}".format(old_ip['content'], current_ip))

            payload = {
                'content': current_ip,
                'type': old_ip['type'],
                'name': old_ip['name']
            }

            req = requests.put(url, data=json.dumps(payload), headers=self.headers)

            output = "{}: {}".format(now, 'Public IP change detected, DNS updated automatically to {}, with response {}'.format(
                current_ip,
                req.status_code))
            return output

        else:
            return None

    def find_dns_id(self, _zone_id, record_name):
        self.logger.debug("== Find DNS ID ==")

        url = '{}/zones/{}/dns_records/'.format(self.base_url, _zone_id)

        req = requests.get(url, headers=self.headers).json()['result']
        # pprint(req)

        # self.logger.debug(req)

        _dns_id = None
        for content in req:
            if content['name'] == record_name:
                _dns_id = content['id']

        # print("DNS ID for {}: {}".format(record_name, _dns_id))

        return _dns_id

    def find_zone_id(self, zone_name):
        get_vars = {'status': 'active', 'account.id': env.account_id, 'match': 'all'}
        url = '{}/zones?'.format(self.base_url)

        url += urlencode(get_vars)
        req = requests.get(url, headers=self.headers).json()['result']

        # pprint(req)

        _zone_id = None
        for content in req:
            if content['name'] == zone_name:
                _zone_id = content['id']

        # print(zone_id)

        return _zone_id


if __name__ == '__main__':
    app = CloudflareApi()

    zone_id = app.find_zone_id('hjb.io')
    dns_id = app.find_dns_id(zone_id, 'home.hjb.io')
