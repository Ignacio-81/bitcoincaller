""" This module will be running to get information and launching events in the background
set time as parameter
"""
import time
import comm
import threading
#import datetime

class watchbot(object):
    
    def __init__(self, interval=5.0, p_var=5.0, mvar = 100000):
        self._running = True
        self.interval = interval
        self.p_var = p_var
        self.mvar = mvar

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()
    
    def terminate(self): 
        self._running = False
    
    def run(self):
        while self._running:
            
            stat, data = comm.get_btdata('USD')
            if stat == False : break
            comm.post_IFTTT_event('bitcoin_USD_price', data)
            
            if self.interval >= 3600 : time.sleep(3600) 
            else: time.sleep(self.interval)

            if abs(data['percent_change_1h']) >= float(self.p_var) or data['price'] < float(self.mvar) :
                    data ['percent_change_24h'] = data ['percent_change_1h']
                    comm.post_IFTTT_event('bitcoin_alert', data)
            
            if self.interval >= 3600 : time.sleep (self.interval - 3600)           

            