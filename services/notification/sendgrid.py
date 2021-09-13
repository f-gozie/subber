from decouple import config
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

'''
from celery.decorators import task
from celery.utils.log import get_task_logger
'''

# logger = get_task_logger(__name__)

# @task(name='send_mail')
def send_email(to, otp_code):
	data = Mail(
		from_email = 'fagozie43@gmail.com',
		to_emails = to,
		subject = 'OTP verification',
		html_content = f'<strong>Thank you for registering. Your OTP is {otp_code}. </strong>'
	)
	try:
		sg = SendGridAPIClient(config('SENDGRID_API_KEY'))
		resp = sg.send(data)
		# logger.info("Sent OTP email")
		return "Success"
	except Exception as e:
		# logger.error(f'{e}')
		return 'Failed'
