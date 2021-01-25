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

def loop():
    
    bot = resident.watchbot(_running = False)
    while True:
        try: 
            clear()

            print("========================")
            print("    Bitcoin Manager     ")
            print("========================")
            print("[1] Ask bitcoin info USD")
            print("[2] Ask bitcoin info ARS")
            print("[3] Send BT to Mobile   ")
            print("[4] Notification process")
            print("[5] Empty               ")
            print("[6] Exit                ")
            print("========================")

            option = input("> ")

            clear()

            if option == '1':
                print("Retrieving Bitcoin USD Information...\n")
                stat, data = comm.get_btdata('USD')
                show_bc_screen(stat,data, cur='USD')
            
            if option == '2':
                print("RetrievingBitcoin ARS Information...\n")
                stat, data = comm.get_btdata('ARS')
                show_bc_screen(stat, data, cur='ARS')
            
            if option == '3':
                print("Select the currency -> 1.USD / 2.ARS")
                opt2 = input("> ")
                print("Sending BC information to Mobile...\n")
                if opt2 == '1':
                    cur = 'USD'
                    
                if opt2 == '2':
                    cur = 'ARS'    
                
                stat, data = comm.get_btdata(cur)
                if stat :
                    stat, data = comm.post_IFTTT_event('bitcoin_'+cur+'_price', data)
                show_bc_screen (stat, data)

            if option == '4':
                print("Please select to 1-RUN or 2-STOP background notification process:")
                opt2 = input("> ")
                if opt2 == '1':
                        if not bot._running : 
                            print("\nPlease enter notification time in HS:")
                            time = (float(input("> ")) * 3600)
                            print("\nPlease enter BC threshold '%' change in the last hour ...")
                            p_val = input("> ")
                            print("\nPlease enter BC minimum Threshold Value in USD...")
                            mval = input("> ")
                            print("Running notification process...\n")  
                            bot = resident.watchbot(True, time, p_val, mval)
                        else:
                            print("The Notification process is already running, please stop it first...") 

                if opt2 == '2':
                    if bot._running  : 
                        print("Stopping notification process...\n")
                        bot.terminate()
                    else:
                        print("Notification process was not running...\n")


            if option == '5':
                print("Empty...\n")
                
            if option == '6':
                print("Closing app, Bye!...\n")
                break
        
        except ConnectionError as err:
            print('Communication Error: ', err)            
        
        finally :     
            input("\nPress ENTER to continue...")

    
