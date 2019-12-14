
from qt.notificationwindow import Ui_NotificationWindow


class NotifiactionWindow(QtWidgets.QWidget, Ui_NotificationWindow):
    def __init__(self, personality, parent=None):
        super(NotificationWindow, self).__init__()
		self.setupUi(self)
        parent_width = parent.width()
        parent_length = parent.length()

        