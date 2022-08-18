
pip uninstall warg apppath draugr devpack

REM cd ..\..

cd ..\warg
python .\setup.py develop

cd ..\apppath
python .\setup.py develop

cd ..\draugr
python .\setup.py develop

cd ..\devpack
python .\setup.py develop