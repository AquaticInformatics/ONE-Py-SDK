python -m venv .venv
cd .venv/Scripts 
set-executionpolicy remotesigned 
.\Activate.ps1
python -m pip install pip --upgrade
cd ..\..
python -m pip install requests 
python -m pip install one_interfaces-4.4.0-py2.py3-none-any.whl
python -m pip install protobuf==3.20.1
mv one_interfaces.pth .\.venv\Lib\site-packages
del .\one_interfaces-4.4.0-py2.py3-none-any.whl