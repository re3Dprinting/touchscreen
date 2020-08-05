from PyQt5 import QtCore

class TableModel(QtCore.QAbstractListModel):
    def __init__(self, parent, headers, columnWeight = [1,1], rowClickedSignal = None): 
        super().__init__()
        self.datalist = []
        self.headers = headers
        self.rowClickedSignal = rowClickedSignal
        self.columnWeight = list(map(lambda x: x/sum(columnWeight), columnWeight))

    def updateDataList(self, data):
        self.datalist = data
    def getDataList(self):
        return self.datalist
    
    @QtCore.pyqtSlot(int)
    def rowClicked(self, row):
        if(self.rowClickedSignal != None):
            self.rowClickedSignal.emit(row)

    def rowCount(self, parent):
        return len(self.datalist)
    def columnCount(self, parent):
        return len(self.datalist[0])
    
    @QtCore.pyqtSlot(int, int, result=str)
    def get(self, row, col):
        if len(self.datalist) > 0 :
            if isinstance(self.datalist[row], tuple):
                return str(self.datalist[row][col])
            return str(self.datalist[row].getDataFromIndex(col))
    @QtCore.pyqtSlot(int, result=str)
    def getTitle(self, index):
        return self.headers[index]
    @QtCore.pyqtSlot(int, result=float)
    def getColumnWeight(self, index):
        return self.columnWeight[index]