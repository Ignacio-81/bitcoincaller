""" Menu del programa """

import comm
import mailhand
import resident
import os
import platform

def clear():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def loop():

    while True:

        clear()

        print("========================")
        print("    Bitcoin Manager     ")
        print("========================")
        print("[1] Ask bitcoin info USD")
        print("[2] Ask bitcoin info ARS")
        print("[3] Send BT to Mobile   ")
        print("[4] Mobile Notification ")
        print("[5] E-Mail Notification ")
        print("[6] Exit                ")
        print("========================")

        option = input("> ")

        clear()

        if option == '1':
            print("Retrieving Bitcoin USD Information...\n")
            stat, data = comm.get_btdata('USD')
            if stat: 
                #print('Answer OK from server') 
                print("Bitcoin value is: {0:,.2f} ".format(data['price']) + 'USD')
                print("Last 24hs variation is: {0:.2%}".format(data['percent_change_24h']/100))
                print("Last 7days variation is: {0:.2%}".format(data['percent_change_7d']/100))
            else: 
                print('Error while requesting info: {}'.format(data))
        
        if option == '2':
            print("RetrievingBitcoin ARS Information...\n")
            stat, data = comm.get_btdata('ARS')
            if stat: 
                print("Bitcoin value is: {0:,.2f} ".format(data['price']) + 'ARS')
                print("Last 24hs variation is: {0:.2%}".format(data['percent_change_24h']/100))
                print("Last 7days variation is: {0:.2%}".format(data['percent_change_7d']/100))
            else: 
                print('Error while requesting info: {}'.format(data))
        
        if option == '3':
            print("Select the currency -> 1.USD / 2.ARS")
            opt2 = input("> ")
            print("Sending BC information to Mobile...\n")
            if opt2 == '1':
                stat, data = comm.get_btdata('USD')
                comm.post_IFTTT_event('bitcoin_USD_price', data)
            if opt2 == '2':
                stat, data = comm.get_btdata('ARS')
                comm.post_IFTTT_event('bitcoin_ARS_price', data)    
            
            
        if option == '4':
            print("Please select to 1-RUN or 2-STOP background notification process:")
            opt2 = input("> ")
            if opt2 == '1':
                print("Please enter notification time in HS...\n")
                time = (float(input("> ")) * 3600)
                print("Please enter BC threshold '%' change in the last hour ...\n")
                p_val = input("> ")
                print("Please enter BC minimum Threshold Value in USD...\n")
                mval = input("> ")
                print("Running notification process...\n")
                
                bot = resident.watchbot(time,p_val,mval)
            
            if opt2 == '2':
                print("Stopping notification process...\n")
                bot.terminate()

        if option == '5':
            print("Empty...\n")
            
        if option == '6':
            print("Closing app, Bye!...\n")
            break

        input("\nPress ENTER to continue...")