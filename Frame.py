import wx
import wx.aui


class Frame(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        self._mgr = wx.aui.AuiManager()
        self._mgr.SetManagedWindow(self)
    
    def SetStatus(self, message, index=0):
        self.statusbar.SetStatusText(message, index)
    
    def ClearStatus(self):
        n=self.statusbar.GetFieldsCount()
        for i in range(0,n):
            self.statusbar.SetStatusText("",i)
    
