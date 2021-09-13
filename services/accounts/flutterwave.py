import requests
from decouple import config

from rave_python import Rave


BASE_URL = config('FLUTTERWAVE_BASE_URL')

RAVE_SECRET_KEY = config('RAVE_SECRET_KEY')
RAVE_PUBLIC_KEY = config('RAVE_PUBLIC_KEY')

header = {
	'Authorization': f'Bearer {RAVE_SECRET_KEY}'
}

rave = Rave(secretKey=RAVE_SECRET_KEY, publicKey=RAVE_PUBLIC_KEY, usingEnv=False)

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


	def create_virtual_card(self):
		'''
			Description: Create virtual card
			Accepts: {
				'currency': 'NGN',
				'amount': '10',
				'billing_name': 'Test Case',
			}
			Request Type: POST
			Returns: Status code with accompanying data
		'''
		data = {
		    "currency": "USD",
		    "amount": 5000,
		    "billing_name": "Jermaine Graham",
		    "billing_address": "333 fremont road",
		    "billing_city": "San Francisco",
		    "billing_state": "CA",
		    "billing_postal_code": "984105",
		    "billing_country": "US",
		    "callback_url": "https://your-callback-url.com/"
		}
		response = requests.post(
			f'{BASE_URL}/virtual-cards',
			data=data,
			headers=header
		).json()
		return response



# x = FlutterwaveService()
# # print(x.get_banks())
# print(x.create_virtual_card())

res = rave.VirtualCard.create(
	{
		"currency": "NGN",
	    "amount": "100",
	    "billing_name": "Corvus james",
	    "billing_address": "8, Providence Street",
	    "billing_city": "Lekki",
	    "billing_state": "Lagos",
	    "billing_postal_code": "100001",
	    "billing_country": "NG",
	}
)
print(res)