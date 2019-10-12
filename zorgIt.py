from datetime import datetime
import time
from dateutil.parser import parse
import re
import sys
import os
import pyperclip
from appJar import gui

myVersion = 'V3.0.0'
appName = 'ZorgIt - Fleet Save Tuning'

# Fill the clipboard for testing purposes only
flightTime = '01:01:31 h'
departureTime = '10. Oct 2019 08:30:26'

# clipboard = pyperclip.copy(flightTime)
# clipboard = pyperclip.copy(departureTime)
# clipboard = pyperclip.copy('')


def updateNewInfo():
    """ Special 'Valhalla' request user input values """
    userInput = app.getEntry("userInput")
    app.clearListBox('theListBox', callFunction=True)
    pyperclip.copy(userInput)
    
    app.addListItems('theListBox', getClipboard())
    app.selectListItemAtPos('theListBox', 0, callFunction=False)


def updateNewClipboard():
    app.setEntry("userInput", pyperclip.paste())
    app.clearListBox('theListBox', callFunction=True)
    app.addListItems('theListBox', getClipboard())
    app.selectListItemAtPos('theListBox', 0, callFunction=False)


def Quit():									                                                            # Leave the program normal
    """  Leave this program """
    app.stop(event=None)


def Input():
    """   User input makes the input button remove """
    app.clearListBox('theListBox', callFunction=True)                                                   # Clear the listbox before filling it
    app.hideButton('Input')

    try:									                        # Do not trip if widget is already there
        app.addEntry("userInput")
        app.setFocus("userInput")
        app.setEntry("userInput", "00:00:00")
        app.setEntryAlign("userInput", "center")
    except Exception as err:
        print(err)
        return

    try:
        app.addButtons(['Process user Input', 'From Clipboard'], [updateNewInfo,  updateNewClipboard])
    except Exception as err:
        print(err)
        return


def Info():									                        # Display some information
    theMessage = [
        ' ',
        ' ',
        '                     By the Power of Thor and Freaker',
        '',
        '                             You will flight save !!',
        '',
        '                      Use this program at own risk!']

    app.clearListBox('theListBox', callFunction=False)
    app.addListItems('theListBox', list(theMessage))
    app.selectListItemAtPos('theListBox', 0, callFunction=False)


def resource_path(relative_path):					                         	# Get relative path for use with pyinstaller
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def getClipboard():

    # Get current Clipboard
    global clipboard
    clipboard = pyperclip.paste()
    print('[Clipboard].[Get]', repr(clipboard)[:25] + '....', '[length]=', len(clipboard))

    # Check if clipboard is empty
    if clipboard == '':
        print('[Clipboard].[Get]', repr(clipboard))
        app.warningBox('Clipboard Error!!',  'Clipboard is Empty\n\nExamples: \n\n' + repr(flightTime) + '\n' + repr(departureTime))
        print('Error??')
        exit()

    # next check if length of input is 10 or less test it for valid time so we can start Fleet saver
    elif len(clipboard) <= 10:
        print('[Clipboard].[Length] <=10 ## lets do a RegExp on it')
        
        clipboard = clipboard.strip(' h')                                                   # Clipboard without the ' h' will pass the parse test!

        try:
            print('[Clipboard].[Parse] Able to  to parse', parse(clipboard))
        except Exception as err:
            print('[Clipboard].[Parse] Not able to parse: ', clipboard, err)
            app.warningBox('Clipboard Error!!', 'Clipboard is unable to parse.\n\nExamples: \n\n' + repr(flightTime) + '\n' + repr(departureTime))
            exit()

        # Create a RegEx for time match HH:MM:SS  like 76:13:06 or  01:00:00 h (one Hour)
        durationRegEx = re.compile(r'(\d+):(\d\d):(\d\d)')
        mo = durationRegEx.search(clipboard)

        # Try to find a matching object 'duration' Regular Expression
        if mo:
            print('[Clipboard].[Regex] There is a match!! >>', repr(mo.groups()), '<<')

            app.setLabel('labelTitle', 'Fleet Saver ' + myVersion)

            hour, minutes, second = mo.groups()
            totalDuration = int(hour) * 3600 + int(minutes) * 60 + int(second)

            print('\nFlight Duration: ', totalDuration, 'Sec')

            # Run fleet saver calculations and create a list for display
            theNewList = [' Clipboard data:  ' + clipboard]		                         	# This is the list that will be displayed

            currentTime_Utc = datetime.utcnow().timestamp()			                   	    # UTC Time in unix sec.
            currentTime_Loc = datetime.now().timestamp()			                	    # Local Time in unix sec.
            time_Difference = currentTime_Utc - currentTime_Loc			                    # Global Time difference

            for durationPercent in range(1, 101):
                duration = totalDuration / (durationPercent / 100)		                    # get 1 - 100% of the Total duration

                timeOfArrival = currentTime_Utc + (2 * duration)		                    # Double the trip you have to get back to!
                timeOfArrival = timeOfArrival - time_Difference			                    # Adjust to local time

                durationPercent = str(durationPercent) + '%'			                    # make it look nice
                durationPercent.ljust(5, ' ')					                            # Align Left in a 5 char space fill with ''

                newLine = ' Speed  [' + durationPercent.center(5, ' ') + ']  Return @ ' + time.asctime(time.localtime(timeOfArrival))
                theNewList.append(newLine)                                                  # Append 'newLine' to 'theList'

            return theNewList
        else:
            print('[Clipboard] :  No match!  Need  01:43:03 h for example')

    # If length is valid to parse to a date start the Fleet Recall
    else:
        try:
            userTime = parse(clipboard)
            # print('DepartureTime: ', clipboard, ' Parse >> ', dt)

            # Get local Timezone
            timezone = datetime.now() - datetime.utcnow()

            # create a time <class 'datetime'> element
            currentTime = datetime.utcnow()
            deltaTime = currentTime - userTime
            newTime = currentTime + deltaTime
            localTime = newTime + timezone
            app.setLabel('labelTitle', 'Fleet Recall ' + myVersion)

            print(localTime.strftime("\nYour Fleet will return on %c"))
            return ["", "", "", "    Your Fleet will return on".center(75, ' '), "            ", localTime.strftime("%c").center(75, ' ')]

        except Exception as err:
            print('[clipboard].[Parse].Error!!  Need "10. Oct 2019 08:30:26" for example.', err)
            app.warningBox('Clipboard Error!!', 'Clipboard parse error\n\nExamples: \n\n' + repr(flightTime) + '\n' + repr(departureTime))
            exit()
    
app = gui(appName + ' ' + myVersion, "378x300")				    	                        # Initialise the appJar Gui with Name and Size
app.setBg("SteelBlue")							                                            # Set background to blue steel
app.setFont(11)								                    	                        # Use font Size 11
app.setLocation(x=860, y=10)						                       	                # move app window to top right corner
app.setTransparency(90)								                                        # make it look little transparent
app.setOnTop(stay=False)						                	                        # Do not stay on top of all windows
app.showIcon = False
app.setIcon(resource_path('favicon.ico'))				                                    # Set favicon.ico inclusive relative path for use in pyinstaller

app.addLabel("labelInfo", "@xx[{::::::::::::::-     By the Power of Thor & Freaker (c) 2019")
app.getLabelWidget("labelInfo").config(font="Times 10")
app.setLabelFg("labelInfo", "LightSteelBlue")
app.addLabel('labelTitle', 'Fleet Save Tuner')
app.getLabelWidget("labelTitle").config(font="Times 18")

clipboard = pyperclip.paste()

theList = getClipboard()
app.addListBox('theListBox', theList)						                                # Make the a List Object in appJar
app.selectListItemAtPos('theListBox', 0, callFunction=False)

app.buttons(["Info", "Quit", "Input"], [Info, Quit, Input])			                        # Define the buttons info and exit

app.go()                                                                                    # Start the GUI interface
