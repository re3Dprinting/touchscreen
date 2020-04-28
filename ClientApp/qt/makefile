%.py: %.ui
	pyuic5 $< -o $@

OBJS = \
     activeprintwidget.py \
     debugwindow.py \
     duexsetupwindow.py \
     infowindow.py \
     notactiveprintwidget.py \
     notificationwindow.py \
     runout.py \
     serialwindow.py \
     serverwindow.py \
     userupdatewindow.py \
     home_qt.py \
     printpage_qt.py \
     controlpage_qt.py \
     temperaturepage_qt.py \
     settingspage_qt.py \
     mainwindow_qt.py

all: $(OBJS)

clean:
	rm -f $(OBJS)
