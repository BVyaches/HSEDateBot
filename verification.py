import random
import smtplib
import re
import asyncio

async def SendVerificationCode(toAddrs):
    email = 'hseloveperm.bot@yandex.ru'
    verCode = str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(
        random.randint(0, 9))

    subject = '❕Ваш код для входа и создания анкеты❕'
    message = 'Ваш код для входа и регистрации: ' + verCode

    msg = 'From: {}\r\nTo: {}\r\nSubject: {}\n\n{}'.format(
        email, toAddrs, subject, message
    )

    server = smtplib.SMTP('smtp.yandex.ru')
    server.starttls()
    server.login(email, 'phoenix14bot')
    server.sendmail(email, toAddrs, msg.encode('utf8'))
    server.quit()

    return verCode


async def check_hse_mail(email):
    pattern = r'\w+@(edu\.)?hse\.ru'
    print(re.fullmatch(pattern, email) is None)
    return re.fullmatch(pattern, email)

asyncio.run(check_hse_mail('vsbolshagin@edu.hse..ru'))
