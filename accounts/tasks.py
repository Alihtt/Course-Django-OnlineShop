from utilts import send_otp_code
from celery import shared_task


@shared_task
def send_otp_code_task(phone_number, code):
    send_otp_code(phone_number, code)
