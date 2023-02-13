import random
import smtplib
import re
import aiosmtplib
from email.message import EmailMessage
import asyncio

async def SendVerificationCode(email_to_send):
    message = EmailMessage()
    verCode = str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(
        random.randint(0, 9))
    message["From"] = "hseloveperm.bot@yandex.ru"
    message["To"] = email_to_send
    message["Subject"] = "❕Ваш код для входа и создания анкеты❕"
    message.set_content('Ваш код для входа и регистрации: ' + verCode)

    await aiosmtplib.send(message, hostname="smtp.yandex.ru", port=25, password='phoenix14bot',
                          username="hseloveperm.bot@yandex.ru")
    return verCode


async def check_hse_mail(email):
    pattern = r'\w+@(edu\.)?hse\.ru'
    return re.fullmatch(pattern, email)
