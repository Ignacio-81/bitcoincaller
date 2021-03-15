"""
This module has auxiliary function for the program.
"""

def show_bc_screen (stat, data, **args):
    if stat: 
        if data == 'IFTTT': 
            print('IFTTT Request Sended OK...')    
        else: 
            #print('Answer OK from server') 
            print("Bitcoin value is: {0:,.2f} ".format(data['price']) + args['cur'])
            print("Last 24hs variation is: {0:.2%}".format(data['percent_change_24h']/100))
            print("Last 7days variation is: {0:.2%}".format(data['percent_change_7d']/100))
    else: 
        if data == 'IFTTT':
            print('Error while sending IFTTT request: {}'.format(data))
        else:    
            print('Error while requesting info to BC URL:', data)
