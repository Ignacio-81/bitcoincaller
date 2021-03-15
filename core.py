""" FIchero principal del programa """

import comm
import mailhand
import textmenu
import wmenu
import wx

def main():
    frame = wx.App()
    wmenu.MainWindow(None, 'BitCoin Caller')
    frame.MainLoop()
    #menu.loop()
    
if __name__ == "__main__":

    main()