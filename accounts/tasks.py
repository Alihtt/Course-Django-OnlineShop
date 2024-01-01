from utilts import send_otp_code
from celery import shared_task
from accounts.models import OtpCode
from datetime import datetime, timedelta
import pytz


@shared_task
def send_otp_code_task(phone_number, code):
    send_otp_code(phone_number, code)


@shared_task
def delete_expired_otp_codes():
    time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=2)
    OtpCode.objects.filter(created__lt=time).delete()
