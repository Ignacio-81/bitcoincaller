import smtplib
import comm
from getpass import getpass

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail():
    try:
        #The mail addresses and password
        #print("Please enter your gmail account: ")
        sender_address = input(prompt= '\nPlease enter your gmail account:', )
        sender_address += '@gmail.com'
        #print("\nPlease enter your password: ")
        sender_pass = getpass('\nPlease enter your password:')
        print("\nPlease enter destination email: ")
        receiver_address = input(prompt='\nPlease enter destination email: ')
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Bitcoin Notification...'   #The subject line
        #The body and the attachments for the mail
        stat, data = comm.get_btdata('USD')
        mail_content = """Hello,
        Please find information for BitCoin:
        
        Bitcoin value is: {0:,.2f} USD
        Last 24hs variation is: {1:.2%} 
        Last 7days variation is: {2:.2%}%

        Information update -> {3}
        
        Have a nice day!
        """.format(data['price'], data['percent_change_24h']/100, data['percent_change_7d']/100, data['last_updated'])
        
        message.attach(MIMEText(mail_content, 'plain'))
        print('Remember to enable inside Google configuration option -> "Control access to less secure apps"')
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
 