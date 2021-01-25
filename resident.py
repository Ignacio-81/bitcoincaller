""" This module will be running to get information and launching events in the background.
send flag to stop thread from running.
set time interval to send notifications.
set absolute percentage (in 1 hour) modification threshold to send alarm
set minimum value to send alarm
"""
import time
import comm
import threading

class watchbot(object):
    
    def __init__(self, _running = True, interval=5.0, p_var=5.0, mvar = 100000):
        self._running = _running
        if self._running :
            self.interval = interval
            self.p_var = p_var
            self.mvar = mvar

            thread = threading.Thread(target=self.run, args=())
            thread.daemon = True #Running as daemon in order to kill qhen program exists
            thread.start()

    def terminate (self):
        self._running = False
    
    def run(self):
        while True: #This flag will end thread run.
            if not self._running : break
            stat, bc_data = comm.get_btdata('USD')
            if stat == False : break #This error getting data  will end thread run.
            stat, data = comm.post_IFTTT_event('bitcoin_USD_price', bc_data)
            if stat == False : break #This error getting data  will end thread run.
            if self.interval >= 3600 : time.sleep(3600) 
            else: time.sleep(self.interval)

            if abs(bc_data['percent_change_1h']) >= float(self.p_var) or bc_data['price'] < float(self.mvar) :
                    bc_data ['percent_change_24h'] = bc_data ['percent_change_1h']
                    comm.post_IFTTT_event('bitcoin_alert', bc_data)
                    if stat == False : break #This error getting data  will end thread run.
            
            if self.interval >= 3600 : time.sleep (self.interval - 3600)
                       

            