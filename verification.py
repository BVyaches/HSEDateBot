import random
import smtplib

def SendVerificationCode(toAddrs):
    
    email = 'hseloveperm.bot@yandex.ru'
    verCode = str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))

    subject = 'Верификация'
    message = 'placeholder ' + verCode + ' placeholder'
    
    msg = 'From: {}\r\nTo: {}\r\nSubject: {}\n\n{}'.format(
       email, toAddrs, subject, message
    )
 
    server = smtplib.SMTP('smtp.yandex.ru')
    server.starttls()
    server.login(email, 'phoenix14bot')
    server.sendmail(email, toAddrs, msg.encode('utf8'))
    server.quit()
	
    return verCode
