git clone https://github.com/re3Dprinting/touchscreen.git --branch feature/octo-integration
git clone https://github.com/jim-thompson/OctoPrint.git --branch devel OctoPrint
ln -s OctoPrint OctoPrint-1.4.0rc3
cd OctoPrint
python3 -m virtualenv --system-site-packages ./venv
. venv/bin/activate
pip install --upgrade pip
pip install gitpython
pip install -e .[develop,plugins]
ln -s ../touchscreen/ClientApp/img .
ln -s ../../touchscreen/ClientApp ./src/touchscreen
mkdir localgcode
