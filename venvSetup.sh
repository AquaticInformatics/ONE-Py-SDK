python3 -m venv .venv
cd .venv/Scripts 
source bin/activate activate
python -m pip install pip --upgrade
cd ../..
python3 -m pip install requests 
python3 -m pip install one_interfaces-4.4.0-py2.py3-none-any.whl
python3 -m pip install protobuf==3.20.1
mv one_interfaces.pth ./.venv/Lib/site-packages
