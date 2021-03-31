""" FIchero principal del programa """

#TO USE FOR COMMAND LINE VERSION:
#import textmenu

#TO USE FOR WINDOWS VERSION:
import wx
import wmenu


def main():
    #COde to RUN on windows interface

    frame = wx.App()
    wmenu.MainWindow(None, 'BitCoin Caller')
    frame.MainLoop()

    #Line to RUN on Command line Menu
    #textmenu.loop()
    
if __name__ == "__main__":

    main()