import json
from urllib.request import Request, urlopen

from common.tools import cprint
# Timeout
from wrapt_timeout_decorator import timeout

API_BASE_URL = f'https://snapeda-eeintech.herokuapp.com/snapeda?q='
SNAPEDA_URL = 'https://www.snapeda.com'

@timeout(dec_timeout=20)
def fetch_snapeda_part_info(part_number: str) -> dict:
	''' Fetch SnapEDA part data from API '''

	data = {}
	api_url = API_BASE_URL + part_number
	request = Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})

	with urlopen(request) as response:
		data = json.load(response)

	return data

def test_snapeda_api_connect() -> bool:
	''' Test method for SnapEDA API '''

	test_part = fetch_snapeda_part_info('SN74LV4T125PWR')
	if test_part:
		return True

	return False

def parse_snapeda_response(response: dict) -> dict:
	''' Return only relevant information from SnapEDA API response '''

	data = {}

	# data = {
	# 	'has_symbol': False,
	# 	'has_footprint': False,
	# 	'symbol_image': None,
	# 	'footprint_image': None,
	# 	'package': None,
	# 	'part_url': 'https://www.snapeda.com',
	# }

	number_results = int(response.get('hits', 0))

	# Check for single result
	if number_results != 1:
		pass
	else:
		try:
			data['has_symbol'] = response['results'][0].get('has_symbol', False)
			data['has_footprint'] = response['results'][0].get('has_footprint', False)
			data['symbol_image'] = response['results'][0]['models'][0]['symbol_medium'].get('url', None)
			data['footprint_image'] = response['results'][0]['models'][0]['package_medium'].get('url', None)
			data['package'] = response['results'][0]['package'].get('name', None)
			data['part_url'] = SNAPEDA_URL + response['results'][0]['_links']['self'].get('href', '')
		except KeyError:
			pass

	return data
