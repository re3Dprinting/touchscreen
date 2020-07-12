from PyQt5 import QtCore

class TableModel(QtCore.QAbstractListModel):
    def __init__(self, parent, rowClickedSignal): 
        super().__init__()
        self.datalist = []
        self.rowClickedSignal = rowClickedSignal

    def updateData(self, data):
        self.datalist = data
    
    @QtCore.pyqtSlot(int)
    def rowClicked(self, row):
        self.rowClickedSignal.emit(row)

    def rowCount(self, parent):
        return len(self.datalist)
    def columnCount(self, parent):
        return len(self.datalist[0])
    
    @QtCore.pyqtSlot(int, int, result=str)
    def get(self, row, col):
        if len(self.datalist) > 0 :
            return self.datalist[row].getDataFromIndex(col)
