%.py: %.ui
	pyuic5 $< -o $@

OBJS = \
     activeprintwidget.py \
     duexsetupwindow.py \
     notactiveprintwidget.py \
     notificationwindow.py \
     runout.py \
     serverwindow.py \
     userupdatewindow.py \
     home_qt.py \
     printpage_qt.py \
     controlpage_qt.py \
     temperaturepage_qt.py \
     settingspage_qt.py \
     debugpage_qt.py \
     infopage_qt.py \
     serialpage_qt.py \
     mainwindow_qt.py

all: $(OBJS)

clean:
	rm -f $(OBJS)
