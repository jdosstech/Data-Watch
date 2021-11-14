import wx

class WatchListFrame(wx.Frame):
    def __init__(self, crypto):
        wx.Frame.__init__(self, None, wx.ID_ANY, title='Data Watch', pos=wx.DefaultPosition, size=(1000, 700), style=wx.DEFAULT_FRAME_STYLE)
        self.SetBackgroundColour(wx.TheColourDatabase.Find('WHITE'))

if __name__ == '__main__':
    app = wx.App()
    frm = WatchListFrame(None)
    frm.Show()
    app.MainLoop()
