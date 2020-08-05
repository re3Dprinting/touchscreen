import QtQuick 2.11
import QtQuick.Controls 1.2
import QtQuick.Controls.Styles 1.4

Rectangle{
    id: main
    TableView{
        property int selectedRow: -1
        id: tableView
        horizontalScrollBarPolicy: Qt.ScrollBarAlwaysOff
        verticalScrollBarPolicy: Qt.ScrollBarAsNeeded
        backgroundVisible: false
        objectName: "tableView"
        anchors.fill: parent
        model: tableModel
        alternatingRowColors: false
        style: TableViewStyle{
            decrementControl: Rectangle{
                color: "transparent"
            }
            incrementControl: Rectangle{
                color: "transparent"
            }
            scrollBarBackground: Rectangle{
                color: "transparent"
                width: 6
            }
            handle: Rectangle {
                implicitWidth: 6
                color:  "#393b3f"
                radius: 3
            }
            minimumHandleLength: 20
        }
        headerDelegate:
        Rectangle{
            height: 30
            color: "white"
            Text{
                font.family: "Lato"
                font.pixelSize: 23
                text: styleData.value
                anchors.fill: parent
                horizontalAlignment: styleData.column === 0 ? Text.AlignRight : Text.AlignLeft
                anchors.leftMargin: 10
                anchors.rightMargin: 10
//                anchors.left: parent.left
//                anchors.right: parent.right
            }
        }

        rowDelegate: Rectangle{
            anchors.left: parent.left
            anchors.right: parent.right
            height:40
            color: styleData.row === tableView.selectedRow? "#ffd400" : "transparent"
        }
        onClicked: {
            tableView.selectedRow = row
            model.rowClicked(row)
        }


        TableViewColumn{
            title: tableModel.getTitle(0)
            movable: false
            delegate: columndel
            width: main.width * tableModel.getColumnWeight(0)
            resizable: false
        }
        TableViewColumn{
            title: tableModel.getTitle(1)
            movable: false
            delegate: columndel
            width: main.width * tableModel.getColumnWeight(1)
            resizable: false
        }
    }

    Component{
        id: columndel
        Rectangle{
            color: "transparent"
            Text{
                font.family: "Lato"
                font.pixelSize: 14
                anchors.fill: parent
                anchors.leftMargin: 10
                anchors.rightMargin: 10
                horizontalAlignment: styleData.column === 0 ? Text.AlignRight : Text.AlignLeft
                verticalAlignment: Text.AlignVCenter
                text: tableView.model.get(styleData.row, styleData.column)
            }
        }
    }

}

/*##^##
Designer {
    D{i:0;autoSize:true;height:480;width:640}
}
##^##*/
