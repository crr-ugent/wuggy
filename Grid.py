import codecs
import sys

import wx
import wxspreadsheet

newline=u'\r\n' if sys.platform=='win32' else u'\n'

class Grid(wxspreadsheet.Spreadsheet):
    def __init__(self, *args, **kwds):
        wx.grid.Grid.__init__(self, *args, **kwds)
        self.rowcursor=0        
        
        # Init variables 
        self._lastCol = -1              # Init last cell column clicked
        self._lastRow = -1              # Init last cell row clicked
        self._selected = None           # Init range currently selected
                                        # Map string datatype to default renderer/editor
        # self.RegisterDataType(wx.grid.GRID_VALUE_STRING,
        #                       wx.grid.GridCellStringRenderer(),
        #                       CCellEditor(self))
        # self.__init_mixin__()
        self.CreateGrid(4, 3)           # By default start with a 4 x 3 grid
        self.SetColLabelSize(18)        # Default sizes and alignment
        self.SetRowLabelSize(50)
        self.SetRowLabelAlignment(wx.ALIGN_RIGHT, wx.ALIGN_BOTTOM)
        self.SetColSize(0, 75)          # Default column sizes
        self.SetColSize(1, 75)
        self.SetColSize(2, 75)
        
        self._undoStack = []
        self._redoStack = []
        self._stackPtr = 0
        
        # # Sink events
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnLeftClick)
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.OnRightClick)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.OnLeftDoubleClick)
        self.Bind(wx.grid.EVT_GRID_RANGE_SELECT, self.OnRangeSelect)
        self.Bind(wx.grid.EVT_GRID_ROW_SIZE, self.OnRowSize)
        self.Bind(wx.grid.EVT_GRID_COL_SIZE, self.OnColSize)
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.OnCellChange)
        self.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.OnGridSelectCell)
    
	
    def MakeArray(self):
        nrows=self.GetNumberRows()
        ncols=self.GetNumberCols()
        array=[]
        lastrow=0
        for rownum in range(0,nrows):
            line=[]
            for colnum in range(0,ncols):
                value=self.GetCellValue(rownum,colnum)
                line.append(value)
                if value!=u"":
                    lastrow=rownum+1
            array.append(line)
        return array[:lastrow]
    
    def Save(self, path, headers=False):
        output=self.MakeArray()
        if headers==True:
            line=[]
            for colnum in range(self.GetNumberCols()):
                line.append(self.GetColLabelValue(colnum))
            output.insert(0,line)
        f=codecs.open(path,'w','utf-8')
        for line in output:
            f.write(u'\t'.join(line))
            f.write(newline)
        f.close()
    
    def Fill(self,inputseqs):
        self.ClearGrid()
        nrows=self.GetNumberRows()
        nseqs=len(inputseqs)
        if nseqs>nrows:
            maxrow=nrows
            # an exception should be raised here, so that
            # the caller can alert the user
        else:
            maxrow=nseqs
        for rownum,row in enumerate(inputseqs[0:maxrow]):
            for colnum,value in enumerate(row):
                self.SetCellValue(rownum,colnum,value)
    
    def ReadFill(self, path):
        f=codecs.open(path,'rU','utf-8')
        inputseqs=[]
        for line in f:
            fields=line.strip(u'\n').split(u'\t')
            inputseqs.append(fields)
        f.close()
        self.Fill(inputseqs)
    
    def ImportData(self):
        dialog=wx.FileDialog(self.GetParent(), "Choose a file","",style=wx.OPEN)
        if wx.ID_OK==dialog.ShowModal():
            path=dialog.GetPath()
            self.ReadFill(path)
        else:
            pass
        dialog.Destroy()

    def SaveData(self, headers=False):
        dialog=wx.FileDialog(self,"Choose a file","",style=wx.SAVE)
        if wx.ID_OK==dialog.ShowModal():
            path=dialog.GetPath()
            self.Save(path, headers=headers)
        else:
            pass
        dialog.Destroy()

    def DisplayRow(self, fields, rownum=None):
        if rownum==None:
            rownum=self.rowcursor
        if rownum+1>=self.GetNumberRows():
            self.AppendRows(1)
        for colnum,value in enumerate(fields):
            self.SetCellValue(rownum,colnum,fields[colnum])
        self.rowcursor=rownum+1
        self.AutoSizeColumns()
        self.ForceRefresh()
	
    def SetNumberRows(self, numRows=1):
        """ Set the number of rows in the sheet """
        # Check for non-negative number
        if numRows < 0:  return False

        # Adjust number of rows
        curRows = self.GetNumberRows()
        if curRows < numRows:
            self.AppendRows(numRows - curRows)
        elif curRows > numRows:
            self.DeleteRows(numRows, curRows - numRows)

        return True


class InputGrid(Grid):
    def __init__(self, *args, **kwds):
        Grid.__init__(self, *args, **kwds)
    
    def Segment(self, generator, replace=False):
        array=self.MakeArray()
        warnings=[]
        for rownum, (word, segments, expression) in enumerate(array):
            word=word.replace(u' ','')  # remove spaces
            if segments==u"" or replace==True:
                segments=generator.lookup(word)
                segments=u"" if segments==None else segments
                self.SetCellValue(rownum,1,segments)
                if word!="" and segments=="":
                    message=u"row %d: no segments found for %s" % (rownum+1, word)
                    warnings.append(message)
        return warnings
    

class ResultsGrid(Grid):
    def __init__(self, *args, **kwds):
        Grid.__init__(self, *args, **kwds)
    
