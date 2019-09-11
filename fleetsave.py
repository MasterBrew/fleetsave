from sys import exit
import os
import sys
import re
import pyperclip
from datetime import datetime
from appJar import gui
from time import sleep


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# print('\nPath to the favicon.ico')
# print('-'*60)
# print(resource_path('myFavicon.ico').center(60, ' '))
# print('-'*60)

Version = "V1.33"

app = gui("ZorgEmpire Fleetsaver " + Version, "378x620")
app.setBg("SteelBlue")
app.setFont(11)
app.setLocation(x=890, y=5)
app.setTransparency(90)
app.setOnTop(stay=False)

app.showIcon = False
app.setIcon(resource_path('myFavicon.ico'))

utcNow = datetime.utcnow().timestamp()
myNow = datetime.now().timestamp()
myUtcDif = utcNow - myNow

# See if there is a clipboard to work with.
if pyperclip == '':
    print('No clipboard content..')
    sleep(10)
    exit()

# Get Clipboard content
clipBoard = pyperclip.paste()
if len(clipBoard) <= 8:
    pass
    # print('[Clp] : ', clipBoard[:10])
else:
    print('Nothing found like ->  01:43:03  for example')
    sleep(10)
    exit()

# Create a RegEx for time match Hour:minutes:sec  like  76:13:06 or   01:00:00  (one Hour)
durationRegEx = re.compile(r'(\d+):(\d\d):(\d\d)')
mo = durationRegEx.search(clipBoard)

if mo:
    # print('There is a match!!')
    hour, minutes, second = mo.groups()
    totalDuration = int(hour) * 3600 + int(minutes) * 60 + int(second)
else:
    print('[Clp] :  No match!. Need  01:43:03 for example')
    sleep(10)
    exit()

theList = []
print()
for percentage in range(1, 101):
    duration = totalDuration / (percentage / 100)
    timeOfArrive = utcNow + (2 * duration)
    timeOfArrive = timeOfArrive - myUtcDif

    dt_object = datetime.fromtimestamp(timeOfArrive)

    percentage = str(percentage) + '%'

    # fixed length of 9 for all days justify Rightside
    dayNameOfArrival = dt_object.strftime('%A').center(11, ' ')
    # timeOfArrival = f'[{dt_object.hour:02d}:{dt_object.minute:02d}:{dt_object.second:02d}]'
    timeOfArrival = f'{dt_object.hour:02d}:{dt_object.minute:02d}'.ljust(10, ' ')

    dayOfArrival = dt_object.strftime("%d").ljust(2, ' ')
    monthOfArrival = dt_object.strftime("%B").ljust(9, ' ')
    yearOfArrival = dt_object.strftime("%Y").ljust(4, ' ')
    percentage =  percentage.rjust(8, ' ') + ' '

    theLine = percentage + ' ' + dayNameOfArrival + ' ' + timeOfArrival + ' ' + dayOfArrival + ' ' + monthOfArrival + ' ' + yearOfArrival
    theList.append(theLine)

# theList.reverse()

app.addListBox('theList', theList , rowspan=2)

app.go()

