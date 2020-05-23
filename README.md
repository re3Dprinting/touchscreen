# DashboardApp

This application was architechted specifically for re:3D's Gigabot 3D Printers to collect and store data on a local and cloud server.

re:3D is a manufacturer of the world's most affordable industrial large-scale 3D Printer. The organization manages an expanding fleet of 15 printers inhouse. The company has a high printing volume that consists of contract printing and production parts. re:3D must aim to reduce printing downtime to maximize return on these machines. Thus a lot of monitoring and maintenence is required.

This is a standalone Dashboard Application aims to facilitate printer management and maintence. The application runs a server that communicates with clients connected to Gigabot 3D Printers. The clients extract live data from the 3D Printers and pushes it to a local server.

Hardware Arcitechture:
Raspberry Pi w/ 7" touch screen
Chromebook hacked with GalliumOS

Software Arcitechture
Server that spawns threads when a client is detected
Client continuously listens for COM port and server connection
Qt front end running on the server end to display real time data
Server pushes data up to cloud database periodically.

Sources:
https://www.techbeamers.com/python-tutorial-write-multithreaded-python-server/

---

vdevel/1.0.23
-USB update feature implementation
-Checksum validation implemented before software starts
-Backup created when user attempts to

---
