set REPO=%1
set REV=%2
::Remove quotes with %var:"=%
start cmd /k python "%REPO:"=%\hooks\FTP.py" %REPO% %REV%