import sys
import requests
import subprocess
from datetime import datetime
import json

from secrets import *

# Headers to go with API requests
headers = {
	'Content-Type': 'application/json',
	'X-Auth-Key': api_key,
	'X-Auth-Email': api_email,
}

def get_telegram_updates():
	url = bot_url + '/getUpdates'
	print requests.get(url).text


def update_dns():
	current_ip = requests.get('http://ip.42.pl/raw').text
	output = str(datetime.now()) + ': '

	# Find current configured url from DNS
	url = '{}/zones/{}/dns_records/{}'.format(base_url, zone_id, dns_id)

	req = requests.get(url, headers=headers).json()['result']

	old_ip = {
		'content': req['content'],
		'type': req['type'],
		'name': req['name'],
	} 

	# Check if ip has changed, update if so
	if old_ip['content'] != current_ip:

		payload = {
			'content': current_ip,
			'type': old_ip['type'],
			'name': old_ip['name']
		}

		req = requests.put(url, data=json.dumps(payload), headers=headers)

		output += 'Public IP change detected, DNS updated automatically to {}, with response {}'.format(current_ip, req.status_code)

		url = bot_url + '/sendMessage?chat_id={}&text={}'.format(chat_id, output)
		requests.get(url)

	else:
		output += 'No change detected'

	cmd = 'echo {} >> /var/log/cron.log 2>&1'.format(output)
	subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)


def list_dns():
	url = '{}/zones/{}/dns_records/'.format(base_url, zone_id)

	req = requests.get(url, headers=headers).json()['result']
	pprint(req)


def detail_dns():
	url = '{}/zones/{}/dns_records/{}'.format(base_url, zone_id, dns_id)

	req = requests.get(url, headers=headers).json()['result']
	pprint(req)


if __name__ == '__main__':
	if len(sys.argv) > 1 and ('-l' in sys.argv):
		list_dns()

	if len(sys.argv) > 1 and ('-u' in sys.argv):
		update_dns()

	if len(sys.argv) > 1 and ('-d' in sys.argv):
		detail_dns()

	if len(sys.argv) > 1 and ('-t' in sys.argv):
		get_telegram_updates()
