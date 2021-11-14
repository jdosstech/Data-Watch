import wx
import selectionscreen as ss

class DataWatch(wx.App):
    def __init__(self, *args, **kw):
        super(DataWatch, self).__init__(*args, **kw)
        sf = ss.SelectionFrame()
        sf.Show()

if __name__ == '__main__':
    app = DataWatch()
    app.MainLoop()      
