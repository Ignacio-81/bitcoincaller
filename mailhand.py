"""
Mail sender using Google mail system.
Input Parameters -> gmail user , password, destination
"""

import smtplib
import comm
from getpass import getpass
from helpers import show_bc_screen

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail(add, pas, des):
    session = None
    
    #Request BC information and give erro message.
    stat, data = comm.get_btdata('USD')
    if stat == False : 
        show_bc_screen(stat, data)
        return False
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    add += '@gmail.com'

    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = add
    message['To'] = des
    message['Subject'] = 'Bitcoin Notification...'   #The subject line
    #The body and the attachments for the mail
    mail_content = """Hello,
    Please find information for BitCoin:
    
    Bitcoin value is: {0:,.2f} USD
    Last 24hs variation is: {1:.2%} 
    Last 7days variation is: {2:.2%}%

    Information update -> {3}
    
    Have a nice day!
    """.format(data['price'], data['percent_change_24h']/100, data['percent_change_7d']/100, data['last_updated'])
    
    message.attach(MIMEText(mail_content, 'plain'))
    try:   
        session.login(add, pas) #login with mail_id and password
        text = message.as_string()
        session.sendmail(add, des, text)
        return True 
    
    except smtplib.SMTPAuthenticationError :
        raise  ConnectionError ("The username and/or password you entered is incorrect")

    except smtplib.SMTPConnectError as err:
        raise ConnectionError ('SMTP Connection error while sending mail:')
    
    except smtplib.SMTPServerDisconnected as err:
        raise ConnectionError ('Server Connection error while sending mail:')

    except ConnectionError:
        raise
    
    except Exception as inst:
        raise Exception ("Error while sending Mail", inst)

    finally:
        if session is not None:
            session.quit()
            del add, pas   
 