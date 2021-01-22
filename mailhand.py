import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail():
    mail_content = """Hello,
    This is a simple mail. There is only text, no attachments are there The mail is sent using Python SMTP library.
    Thank You
    """
    #The mail addresses and password
    print("Please enter your gmail account: ")
    sender_address = input()
    sender_address += '@gmail.com'
    print("\nPlease enter your password: ")
    sender_pass = input()
    print("\nPlease enter destination email: ")
    receiver_address = input()
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Informe Bitcoin by Nacho.'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    try: 
        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        print('Mail Sent')
        answer = True   
    except smtplib.SMTPException as e:
        print('Error while sending mail:'+e)
        answer = False
    
    finally:
        session.quit()
        del message, sender_address, sender_pass
        return answer
 