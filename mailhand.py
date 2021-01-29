import smtplib
import comm
from getpass import getpass
from menu import show_bc_screen

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail():
    session = None
    try:
        #The mail addresses and password
        stat, data = comm.get_btdata('USD')
        if stat == False : 
            show_bc_screen(stat, data)
            return False
        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        sender_address = input('\nPlease enter your gmail account: ')
        sender_address += '@gmail.com'
        sender_pass = getpass('\nPlease enter your password:')
        receiver_address = input('\nPlease enter destination email: ')
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
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
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
      
    except smtplib.SMTPAuthenticationError :
        print("\nThe username and/or password you entered is incorrect")

    except smtplib.SMTPConnectError as err:
        print('SMTP Connection error while sending mail:'+err)
        #raise ConnectionError ('\nSMTP error while sending mail:'+err) from err  
    
    except smtplib.SMTPServerDisconnected as err:
        print('Server Connection error while sending mail:'+err)

    except ConnectionError:
        raise
    
    except Exception as inst:
        raise Exception ("Connection Error while sending Mail", inst)

    finally:
        if session is not None:
            session.quit()
            del sender_address, sender_pass
            return True    
 