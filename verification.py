import random
import smtplib

def SendVerificationCode(toaddrs):
    
    email = 'hseloveperm.bot@yandex.ru'
    VerCode = str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))

    subject = 'Верификация'
    message = VerCode
    
    msg = 'From: {}\r\nTo: {}\r\nSubject: {}\n\n{}'.format(
       email, toaddrs, subject, message
    )
 
    server = smtplib.SMTP('smtp.yandex.ru')
    server.starttls()
    server.login(email, 'phoenix14bot')
    server.sendmail(email, toaddrs, msg.encode('utf8'))
    server.quit()
	
    return VerCode
