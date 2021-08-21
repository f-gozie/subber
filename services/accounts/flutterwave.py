import requests
from decouple import config


BASE_URL = config('FLUTTERWAVE_BASE_URL')
FLUTTERWAVE_SECRET_KEY = config('FLUTTERWAVE_SECRET_KEY')
header = {
	'Authorization': f'Bearer {FLUTTERWAVE_SECRET_KEY}'
}


class FlutterwaveService:

	def get_banks(self):
		'''
			Description: Get list of all banks
			Accepts: No input
			Request Type: GET
			Returns: List of banks with their codes
		'''
		response = requests.get(
								f'{BASE_URL}/banks/NG',
								data={},
								headers=header
								).json()
		return response



x = FlutterwaveService()
print(x.get_banks())