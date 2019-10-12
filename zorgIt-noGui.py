from datetime import datetime
import time
from dateutil.parser import parse
import re
import pyperclip



# Fill the clipboard for testing purposes only
# flightTime = '01:01:31 h'
# departureTime = '10. Oct 2019 08:30:26'
# clipboard = pyperclip.copy(flightTime)
# clipboard = pyperclip.copy(departureTime)
# clipboard = pyperclip.copy('')


# Get current Clipboard
clipboard = pyperclip.paste()
print('[Clipboard].[Get]', repr(clipboard), '[length]=', len(clipboard))

# Check if clipboard = blanco
if clipboard == '':
    print('[Clipboard].[Get] =', repr(clipboard))

# next check if length of input is 10 or less test it for vallide time so we can start Fleetsaver
elif len(clipboard) <= 10:
    print('[Clipboard].[Length] <=10 ## lets do a RegExp on it')


    # Clipboard without the ' h' will pass the parse test! 
    try:
            print('[Clipboard].[Parse] Able to  to parse', parse(clipboard))
            
    except Exception as err:
            print('[Clipboard].[Parse] Not able to parse: ', clipboard, err)


    # Create a RegEx for time match HH:MM:SS  like 76:13:06 or  01:00:00 h (one Hour)
    durationRegEx = re.compile(r'(\d+):(\d\d):(\d\d)')	
    mo = durationRegEx.search(clipboard)

    
    # Try to find a matching object 'duration' Regular Expression
    if mo:			
        print('[Clipboard].[Regex] There is a match!! >>', repr(mo.groups()),'<<')
        hour, minutes, second = mo.groups()
        totalDuration = int(hour) * 3600 + int(minutes) * 60 + int(second)
        
        print('\nFlight Duration: ', totalDuration, 'Sec')

        # Run fleetsaver calculations and create a list for display
        theNewList = [' Clipboard data:  ' + clipboard]		        	# This is the list that will be displayed

        currentTime_Utc = datetime.utcnow().timestamp()			    	# UTC Time in unix sec.
        currentTime_Loc = datetime.now().timestamp()				# Local Time in unix sec.
        time_Difference = currentTime_Utc - currentTime_Loc			# Global Time difference

        for durationPercent in range(1, 101):
            duration = totalDuration / (durationPercent / 100)			# get 1 - 100% of the Total duration

            timeOfArrival = currentTime_Utc + (2 * duration)			# Double the trip you have to get back to!
            timeOfArrival = timeOfArrival - time_Difference			# Adjust to local time

            dt_object = datetime.fromtimestamp(timeOfArrival)			# Time object of the time traveling to and from destination

            durationPercent = str(durationPercent) + '%'			# make it look nice
            durationPercent.ljust(5, ' ')					# Align Left in a 5 char space fill with ''
           
            newLine = 'Speed [' + durationPercent.center(5,' ') + ']  Return at '+ time.asctime(time.localtime(timeOfArrival))
            theNewList.append(newLine)                                          # Append 'newLine' to 'theList'
    
        for items in theNewList:
            print(items)
            
    else:
        print('[Clipboard] :  No match!  Need  01:43:03 for example')

    
# If length is valid to parse to a date start the Fleet Recaller
else:
    try:
        dt =  parse(clipboard)
        # print('DepartureTime: ', clipboard, ' Parse >> ', dt)

        # Get local Timezone
        timezone = datetime.now() - datetime.utcnow()
        
        # create a time <class 'datetime'> element
        now = datetime.utcnow()
        verschil = now - dt
        newtime = now + verschil
        local = newtime + timezone

        print(local.strftime("\nYour Fleet will return on %c"))
           
    except Exception as err:
            print('[clipboard].[Parse].Error!!  Need "10. Oct 2019 08:30:26" for example.')

    

input('-+- Press enter -+-')