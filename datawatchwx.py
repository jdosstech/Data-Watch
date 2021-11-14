import wx

class SelectionFrame(wx.Frame):
    def __init__(self, *args, **kw):
        style = wx.DEFAULT_FRAME_STYLE & (~wx.MAXIMIZE_BOX) & (~wx.MINIMIZE_BOX) # Hide the maximize and minimize buttons on the window
        super(SelectionFrame, self).__init__(*args, **kw, style=style)
        self.SetSize(size=(620, 420))
        self.SetTitle('Data Watch - Selection Screen')
        #super(SelectionFrame, self).__init__(self, None, title='Data Watch Selection Screen' size=(420, 680))
        #wx.Frame.__init__(self, None, title='Data Watch Selection Screen' size=(420, 680))

        self.SetBackgroundColour(wx.TheColourDatabase.Find('WHITE'))

        pnl = wx.Panel(self)

        self.search = wx.TextCtrl(pnl)
        self.search.SetMaxLength(5)
        self.search.SetHint('Crypto')
        self.search.Bind(wx.EVT_TEXT, self.OnTextChange)

        self.button = wx.Button(pnl, label='Search', size=self.search.GetSize()) # Clicking this button sends the user to the main view
        self.button.Disable()

        # and create a sizer to manage the layout of child widgets
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.search, 0, wx.CENTER)
        sizer.Add(self.button, 0, wx.CENTER)
        pnl.SetSizer(sizer)

    def OnExit(self, event):
            self.Close(True)
    
    def OnTextChange(self, event):
        value = self.search.GetValue()
        if value == '':
            self.button.Disable()
        else:
            self.button.Enable()

        cursor = self.search.GetInsertionPoint()
        self.search.ChangeValue(value.upper())
        self.search.SetInsertionPoint(cursor)
    
    def OnClick(self, event):
        self.Hide()

if __name__ == '__main__':
    app = wx.App()
    frm = SelectionFrame(None)
    frm.Show()
    app.MainLoop()        
