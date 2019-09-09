@echo off
cls

echo 000 INFO: Adding Path to Microsoft.Windows.Common-Controls Location
set PATH=%PATH%;C:\Windows\System32\downlevel;

echo 000 INFO: Moving to the Magic place
cd C:\Python37\scripts

echo 000 INFO: Mantronix is shuffeling the box of O and 1's.

pyinstaller --noconsole --onefile --clean --distpath C:\Users\gebruiker\Desktop\fleetsave^
	    --icon=C:\Users\gebruiker\Desktop\fleetsave\favicon.ico^
	    --add-data=C:\Users\gebruiker\Desktop\fleetsave\favicon.ico;img^
 	    C:\Users\gebruiker\Desktop\fleetsave\fleetsave.py

echo 77777 INFO: Moving to the Birthplace of this monster
cd C:\Users\gebruiker\Desktop\fleetsave

echo 88888 INFO: Removing __pycache__
rm -r __pycache__

echo 99999 INFO: Testing if its realy works! 
fleetsave.exe

