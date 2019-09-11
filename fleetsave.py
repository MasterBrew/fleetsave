import re
import pyperclip
from datetime import datetime
from appJar import gui
from time import sleep

Version = "V1.10"

def Quit():
    app.stop(event=None)

# Setup the Gui
app = gui("ZorgEmpire Fleetsaver " + Version, "378x620")
app.setBg("SteelBlue")
app.setFont(11)

app.setLocation(x=890, y=5)
app.setTransparency(90)
app.setOnTop(stay=False)

app.showIcon = False
#app.setIcon("favicon.ico")

utcNow = datetime.utcnow().timestamp()
myNow = datetime.now().timestamp()
myUtcDif = utcNow - myNow

# See if there is a clipboard to work with.
if pyperclip == '':
    app.warningBox('[Clipboard]', 'No Content!!  Need  01:43:03 for example')
    # print('No clipboard content..')
    exit()

# Get Clipboard content
clipBoard = pyperclip.paste()
if len(clipBoard) <= 8:
    pass
    # print('[Clp] : ', clipBoard[:10])
else:
    app.warningBox('[Clipboard]','Nothing found like ->  01:43:03  for example')
    exit()

# Create a RegEx for time match Hour:minutes:sec  like  76:13:06 or   01:00:00  (one Hour)
durationRegEx = re.compile(r'(\d+):(\d\d):(\d\d)')
mo = durationRegEx.search(clipBoard)

if mo:
    # print('There is a match!!')
    hour, minutes, second = mo.groups()
    totalDuration = int(hour) * 3600 + int(minutes) * 60 + int(second)
else:
    # clipBoard = '01:00:11'
    print('[Clp] :  No match!.')
    sleep(1)
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

