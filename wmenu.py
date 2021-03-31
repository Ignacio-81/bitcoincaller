"""
This module handle windows menu
"""
import wx
import comm
import resident
import mailhand

import sys
import traceback
import wx.lib.agw.genericmessagedialog as GMD

class MainWindow (wx.Frame):
 
    def __init__(self, parent, title):
        super(MainWindow,self).__init__(parent, title=title, size=(400, 300))
        sys.excepthook = ExceptionHook
        self.Centre()
        self.bot = resident.watchbot(_running = False)
    
    #Setting Menus       
        mainmenu = wx.Menu()
        
        askbcinfomenu = wx.Menu()   
        bcinfousd = askbcinfomenu.Append(wx.ID_ANY , '&USD', 'Get Bitcoin information in USD') 
        bcinfoars = askbcinfomenu.Append(wx.ID_ANY, '&ARS', 'Get Bitcoin information in ARS')
        mainmenu.AppendMenu (wx.ID_ANY, '&Ask BitCoin Info', askbcinfomenu)

        notifymenu = wx.Menu()
        notMobile = notifymenu.Append(wx.ID_ANY, 'To Mobile', 'Send BC Values to Mobile')
        notMail = notifymenu.Append(wx.ID_ANY, 'By Mail', 'Send BC Values to Mail')
        mainmenu.AppendMenu (wx.ID_ANY, '&Send Notification', notifymenu)
        mainmenu.AppendSeparator()
        autoNotmobile = mainmenu.Append(wx.ID_ANY, '&BC Alert', 'Send BC Values and alert to Mobile')
        mainmenu.AppendSeparator()
        exitmenu = wx.MenuItem(mainmenu, wx.ID_ANY , '&Exit')
        mainmenu.AppendItem(exitmenu)

    #Setting MenuBar
        menubar = wx.MenuBar()
        menubar.Append(mainmenu, '&BitCoin Info')
        self.SetMenuBar(menubar)
        
        self.CreateStatusBar()

    #BC information Panel
        self.bcInfopanel = wx.Panel(self)
        panelsizer = wx.GridBagSizer(4,2)
        
        self.textC = wx.StaticText(self.bcInfopanel, label='USD Information:')
        panelsizer.Add(self.textC, pos=(0,0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        textV = wx.StaticText(self.bcInfopanel, label='BitCoin Value is:')
        panelsizer.Add(textV, pos=(1,0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        texto24 = wx.StaticText(self.bcInfopanel, label="Last 24hs variation is:")
        panelsizer.Add(texto24, pos=(2,0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        texto7d = wx.StaticText(self.bcInfopanel, label="Last 7days variation is:")
        panelsizer.Add(texto7d, pos=(3,0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        self.textoVV = wx.StaticText(self.bcInfopanel, label=' ')
        panelsizer.Add(self.textoVV, pos=(1,1), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        self.texto24V = wx.StaticText(self.bcInfopanel, label=' ')
        panelsizer.Add(self.texto24V, pos=(2,1), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        self.texto7dV = wx.StaticText(self.bcInfopanel, label=' ')
        panelsizer.Add(self.texto7dV, pos=(3,1), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        self.bcInfopanel.SetSizer(panelsizer)
        #self.panelsizer.Layout()
        self.bcInfopanel.Hide()

    #Send to Mobile Panel
        self.sendMpanel = wx.Panel(self)
        pbox = wx.BoxSizer(wx.VERTICAL)
        lblList = ['USD', 'ARS']     
        self.rbox = wx.RadioBox(self.sendMpanel,label = 'Please select Currency', pos = (80,10), choices = lblList , majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        pbox.Add(self.rbox,0,wx.ALL|wx.ALIGN_LEFT ,5) 
        bn01 = wx.Button(self.sendMpanel, label = "Send Info to Mobile (IFTT)", name='sendBCm') 
        pbox.Add(bn01,0, wx.EXPAND)
        self.sendMpanel.SetSizer(pbox)
        #self.pbox.Layout()
        self.sendMpanel.Hide()
    
    #BC E Mail notification Panel
        self.bcEmail = wx.Panel(self)
        panelsizer = wx.GridBagSizer(4,2)
        
        textGa = wx.StaticText(self.bcEmail, label='Enter google account:')
        panelsizer.Add(textGa, pos=(0,0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        textP = wx.StaticText(self.bcEmail, label="Enter your password:")
        panelsizer.Add(textP , pos=(1,0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        textDe = wx.StaticText(self.bcEmail, label="Destination mail:")
        panelsizer.Add(textDe, pos=(2,0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        
        self.textGu = wx.TextCtrl(self.bcEmail, size=(150,22))
        panelsizer.Add(self.textGu, pos=(0,1), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        self.textPa = wx.TextCtrl(self.bcEmail, size=(150,22),style=wx.TE_PASSWORD)
        panelsizer.Add(self.textPa, pos=(1,1), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        self.textDes = wx.TextCtrl(self.bcEmail, size=(150,22))
        panelsizer.Add(self.textDes, pos=(2,1), flag=wx.TOP | wx.LEFT | wx.BOTTOM | wx.EXPAND, border=5)
        
        self.bn04 = wx.Button(self.bcEmail, label = "Send mail", name='sendMail')         
        panelsizer.Add(self.bn04, pos=(3,0), flag=wx.EXPAND)

        self.bcEmail.SetSizer(panelsizer)
        self.bcEmail.Hide()

    #BC Automatic notification process Panel
        self.bcAutonot = wx.Panel(self)
        panelsizer = wx.GridBagSizer(5,2)
        
        textC = wx.StaticText(self.bcAutonot, label='Automatic Notification Status:')
        panelsizer.Add(textC, pos=(0,0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        textN = wx.StaticText(self.bcAutonot, label="Notification delay Time in HS:")
        panelsizer.Add(textN , pos=(1,0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        textT = wx.StaticText(self.bcAutonot, label="BC threshold '%' change in the last hour:")
        panelsizer.Add(textT, pos=(2,0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        textMt = wx.StaticText(self.bcAutonot, label="BC minimum Threshold Value in USD:")
        panelsizer.Add(textMt, pos=(3,0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        
        self.textSt = wx.StaticText(self.bcAutonot, label=' ')
        panelsizer.Add(self.textSt, pos=(0,1), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        self.textDT = wx.TextCtrl(self.bcAutonot)
        panelsizer.Add(self.textDT, pos=(1,1), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        self.textCh = wx.TextCtrl(self.bcAutonot)
        panelsizer.Add(self.textCh, pos=(2,1), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        self.textTh = wx.TextCtrl(self.bcAutonot)
        panelsizer.Add(self.textTh, pos=(3,1), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        
        self.bn02 = wx.Button(self.bcAutonot, label = "Start Robot", name='startrob')         
        panelsizer.Add(self.bn02, pos=(4,0), flag=wx.EXPAND)
        self.bn03 = wx.Button(self.bcAutonot, label = "Stop Robot", name='stoprob')         
        panelsizer.Add(self.bn03, pos=(4,1), flag=wx.EXPAND)
        self.bcAutonot.SetSizer(panelsizer)
        self.bcAutonot.Hide()

    #Events
        self.Bind(wx.EVT_MENU, lambda e: self.sendNot (e, 'USD'), bcinfousd )
        self.Bind(wx.EVT_MENU, lambda e: self.sendNot (e, 'ARS'), bcinfoars )
        self.Bind(wx.EVT_MENU, lambda e: self.sendNot (e, 'notMobile'), notMobile)
        self.Bind(wx.EVT_MENU, lambda e: self.sendNot (e, 'notMail'), notMail)       
        self.Bind(wx.EVT_MENU, lambda e: self.sendNot (e, 'autoNotmobile'), autoNotmobile)
        self.Bind(wx.EVT_BUTTON, self.onButton, bn01)
        self.Bind(wx.EVT_BUTTON, self.onButton, self.bn02)
        self.Bind(wx.EVT_BUTTON, self.onButton, self.bn03)
        self.Bind(wx.EVT_BUTTON, self.onButton, self.bn04)
        self.Bind(wx.EVT_MENU, self.Onquit, exitmenu)
    
    #LayOut
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.bcInfopanel, 1, wx.EXPAND)
        self.sizer.Add(self.sendMpanel, 1, wx.EXPAND)
        self.sizer.Add(self.bcEmail, 1, wx.EXPAND)
        self.sizer.Add(self.bcAutonot, 1, wx.EXPAND)
        #self.sizer.SetSizeHints(self.sizer)
        self.SetSizer(self.sizer)     
        self.Show(True)

    """
    def Onaskbcinfo (self, e, cur):
        obj = e.GetEventObject()
        if self.sendMpanel.IsShown : self.sendMpanel.Hide()
        stat, data = comm.get_btdata(cur) 
    
        if cur == 'USD':
            self.textC.Label = 'USD Information:'
        else:
            self.textC.Label = 'ARS Information:'

        self.textoVV.Label = '{0:,.2f}'.format(data['price'])
        self.texto24V.Label = '{0:.2%}'.format(data['percent_change_24h']/100)
        self.texto7dV.Label = '{0:.2%}'.format(data['percent_change_7d']/100)
     
        self.bcInfopanel.Show()
        self.Layout()
    """
    def sendNot (self, e, op):
        obj = e.GetEventObject()
        self.bcInfopanel.Hide()
        self.sendMpanel.Hide()
        self.bcEmail.Hide()
        self.bcAutonot.Hide()
            #if self.bcInfopanel.IsShown : self.bcInfopanel.Hide()

        if op == 'USD' or op == 'ARS':
            stat, data = comm.get_btdata(op) 
            if op == 'USD':
                self.textC.Label = 'USD Information:'
            else:
                self.textC.Label = 'ARS Information:'
    
            self.textoVV.Label = '{0:,.2f}'.format(data['price'])
            self.texto24V.Label = '{0:.2%}'.format(data['percent_change_24h']/100)
            self.texto7dV.Label = '{0:.2%}'.format(data['percent_change_7d']/100)

            self.bcInfopanel.Show()
        
        if op == 'notMobile' :
            self.sendMpanel.Show()
        
        if op == 'notMail' : 
            self.bcEmail.Show()

        if op == 'autoNotmobile':
            if not self.bot._running :
                self.textSt.Label = 'NOT Running'
                self.bn02.Show()
                self.bn03.Hide()
            else:
                self.textSt.Label = 'Running'
                self.bn02.Hide()
                self.bn03.Show()
            self.bcAutonot.Show()

        self.Layout()

    def onButton (self, e):
        obj = e.GetEventObject()
        if obj.Name == 'sendBCm':
            cur = self.rbox.GetString(self.rbox.GetSelection())
            stat, data = comm.get_btdata(cur)
            if stat :
                stat, data = comm.post_IFTTT_event('bitcoin_'+cur+'_price', data)
                wx.MessageBox('IFTTT Request Sended OK...' , 'Mobile Notification', wx.OK )
        
        if obj.Name == 'startrob':
            time = float(self.textDT.GetValue()) * 3600
            p_val = self.textCh.GetValue()
            mval = self.textTh.GetValue()
            self.bot = resident.watchbot(True, time, p_val, mval)

        if obj.Name == 'stoprob':
            self.bot.terminate()   
        
        if obj.Name == 'sendMail':
            sender_address = self.textGu.GetValue()
            sender_pass = self.textPa.GetValue()
            receiver_address = self.textDes.GetValue()
            stat = mailhand.send_mail(sender_address, sender_pass, receiver_address)
            if stat : 
                wx.MessageBox( "Mail with BC Information sended OK!...", 'E-Mail Notification', wx.OK )    

        if self.bcInfopanel.IsShown : self.bcInfopanel.Hide()
        if self.sendMpanel.IsShown : self.sendMpanel.Hide()
        if self.bcAutonot.IsShown : self.bcAutonot.Hide()
        
    def Onquit(self, e):
            self.Close()

"""
class askbcwindow(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        panel = wx.Panel(self, -1)
        txt = wx.StaticText(panel, label='Entramos!')
"""
class ExceptionDialog(GMD.GenericMessageDialog):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, msg):
        """Constructor"""
        GMD.GenericMessageDialog.__init__(self, None, msg, "Error message:",
                                          wx.OK|wx.ICON_WARNING)
        
#----------------------------------------------------------------------
def ExceptionHook(etype, value, trace):
    """
    Handler for all unhandled exceptions.
    :param `etype`: the exception type (`SyntaxError`, `ZeroDivisionError`, etc...);
    :type `etype`: `Exception`
    :param string `value`: the exception error message;
    :param string `trace`: the traceback header, if any (otherwise, it prints the
     standard Python header: ``Traceback (most recent call last)``.
    """
    frame = wx.GetApp().GetTopWindow()

#    tmp = traceback.format_exception(etype, value, trace)
    tmp = traceback.format_exception_only(etype, value)
    exception = "".join(tmp)
    dlg = ExceptionDialog(exception)

    dlg.ShowModal()
    dlg.Destroy()    