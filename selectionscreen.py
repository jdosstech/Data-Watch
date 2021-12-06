import wx
import watchlist

class SelectionFrame(wx.Frame):
    def __init__(self):
        style = wx.DEFAULT_FRAME_STYLE & (~wx.MAXIMIZE_BOX) & (~wx.MINIMIZE_BOX) & (~wx.RESIZE_BORDER) # Hide the maximize and minimize buttons and make the window non-resizable
        wx.Frame.__init__(self, None, wx.ID_ANY, title='Data Watch - Selection Screen', pos=wx.DefaultPosition, size=(620, 420), style=style)

        #self.SetBackgroundColour(wx.TheColourDatabase.Find('WHITE'))

        pnl = wx.Panel(self)

        self.search = wx.TextCtrl(pnl)
        self.search.SetMaxLength(5)
        self.search.SetHint('Crypto')
        self.search.Bind(wx.EVT_TEXT, self.OnTextChange)

        self.button = wx.Button(pnl, label='Search', size=self.search.GetSize()) # Clicking this button sends the user to the main view
        self.button.Disable()
        self.button.Bind(wx.EVT_BUTTON, self.OnClick)

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
        frm = watchlist.WatchListFrame(self.search.GetValue()) # 
        self.Hide()
        frm.Show()


if __name__ == '__main__':
    app = wx.App()
    frm = SelectionFrame()
    frm.Show()
    app.MainLoop()        
