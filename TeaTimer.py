import badger2040
import machine
from breakout_rtc import BreakoutRTC
from pimoroni_i2c import PimoroniI2C
import time

# initialise the badger and clear the screen
badger2040.system_speed(badger2040.SYSTEM_SLOW)
display = badger2040.Badger2040()
display.update_speed(badger2040.UPDATE_NORMAL)

# define the buttons as inputs
button_a = machine.Pin(badger2040.BUTTON_A, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_b = machine.Pin(badger2040.BUTTON_B, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_c = machine.Pin(badger2040.BUTTON_C, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_up = machine.Pin(badger2040.BUTTON_UP, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_down = machine.Pin(badger2040.BUTTON_DOWN, machine.Pin.IN, machine.Pin.PULL_DOWN)
# the User button (boot/usr on back of board) is inverted from the others
button_user = machine.Pin(badger2040.BUTTON_USER, machine.Pin.IN, machine.Pin.PULL_UP)


PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}  # i2c pins 4, 5 for Breakout Garden
PINS_PICO_EXPLORER = {"sda": 20, "scl": 21}  # Default i2c pins for Pico Explorer

i2c = PimoroniI2C(**PINS_BREAKOUT_GARDEN)
rtcbreakout = BreakoutRTC(i2c)

message = None
twelveTwentyfour = True
debugMode = 0
debugScreen = None
bst = False

def buttonHandler(pin):
    # Need to mark these as globals, so buttonHandler knows not to create it's own ones
    global message
    global twelveTwentyfour
    global debugScreen
    global debugMode
    
    #Neet to tell the clock to update it's readable time from the actual counter
    rtcbreakout.update_time()
    
    hour = handleTimezone()
    minute = rtcbreakout.get_minutes()
    
    if debugMode == 1:
        debugScreen = 'Do debug'
        # set time etc
        if pin == button_a: #Exit debug mode
            debugScreen = None
            debugMode = 0
            message = 'Back to normal'
            return
        if pin == button_b: #Minute - 1
            newMin = minute - 1
            rtcbreakout.set_minutes(newMin)
            return
        if pin == button_c: #Minute + 1
            newMin = minute + 1
            rtcbreakout.set_minutes(newMin)
            return
        if pin == button_up: #Page Dn from Page 1
            debugMode = 2          
            return
        if pin == button_down: #Page Up from Page 1
            debugMode = 2          
            return
        if pin == button_user: #n/a
            return
    elif debugMode == 2:
        debugScreen = 'Do debug'
        # set time etc
        if pin == button_a: #Exit debug mode
            debugScreen = None
            debugMode = 0
            message = 'Back to normal'
            return
        if pin == button_b: #Hour - 1
            newHour = hour - 1
            rtcbreakout.set_hours(newHour)
            return
        if pin == button_c: #Hour + 1
            newHour = hour + 1
            rtcbreakout.set_hours(newHour)
            return
        if pin == button_up: #Page Dn from Page 2
            debugMode = 1          
            return
        if pin == button_down: #Page Up from Page 2
            debugMode = 2          
            return
        if pin == button_user: #n/a
            return
    else:
        #Regular operations
        if pin == button_a:
            if twelveTwentyfour:
                twelveTwentyfour = False
            else:
                twelveTwentyfour = True
            message = "Tea"
            return
        if pin == button_b:
            message = "Button b"
            return
        if pin == button_c:
            message = "Button c"
            return
        if pin == button_up:
            debugScreen = "Test"
            debugMode = 1
            return
        if pin == button_down:
            message = "Button Down"
            return
        if pin == button_user:
            message = "Button Usr"
            return


# Figure out whether it's BST or GMT at the moment, returns the appropriate hour number.
def handleTimezone ():
    global bst
    rtcbreakout.update_time()
    year = rtcbreakout.get_year()
    month = rtcbreakout.get_month()
    day = rtcbreakout.get_date()
    hours = rtcbreakout.get_hours()
    
    newHour = hours
    
    HHMarch   = time.mktime((year,3 ,(31-(int(5*year/4+4))%7),1,0,0,0,0,0)) #Time of March change to BST
    HHOctober = time.mktime((year,10,(31-(int(5*year/4+1))%7),1,0,0,0,0,0)) #Time of October change to GMT
    now = time.mktime((year, month, day, hours, 0,0,rtcbreakout.get_weekday(), 0,0))

    if now < HHMarch :               # we are before last sunday of march
        #if bst:
        newHour = hours #- 1
        bst = False
    elif now < HHOctober :           # we are before last sunday of october
        #if not bst:
        newHour = hours + 1
        bst = True 
    else:                            # we are after last sunday of october
        #if bst:
        newHour = hours #- 1
        bst = False
    return(newHour)


# define interrupts for the buttons
button_a.irq(trigger=machine.Pin.IRQ_RISING, handler=buttonHandler)
button_b.irq(trigger=machine.Pin.IRQ_RISING, handler=buttonHandler)
button_c.irq(trigger=machine.Pin.IRQ_RISING, handler=buttonHandler)
button_up.irq(trigger=machine.Pin.IRQ_RISING, handler=buttonHandler)
button_down.irq(trigger=machine.Pin.IRQ_RISING, handler=buttonHandler)
button_user.irq(trigger=machine.Pin.IRQ_RISING, handler=buttonHandler)


#display.text(
#    text,         # string: the text to draw
#    x,            # int: x coordinate for the left middle of the text
#    y,            # int: y coordinate for the left middle of the text
#    scale=1.0,    # float: size of the text
#    rotation=0.0  # float: rotation of the text in degrees
#)
#screen is 296 x 128 pixels!  centre is 148x, 64y

#image(
#    data,   # bytearray: raw image data 1bpp
#    w=296,  # int: width in pixels
#    h=128,  # int: height in pixels
#    x=0,    # int: destination x
#    y=0,    # int: destination y
#)

teapot = bytearray(int(120 * 120 / 8))
open("/images/teapot.bin", "rb").readinto(teapot)

#Pretend a button has been pushed on power-up
buttonHandler(button_c)

while True:    
    if message is not None:
        # Clear previous message
        display.pen(15)
        display.clear()
        
        # Start populating screen message
        display.pen(0)
        display.thickness(3)
        display.text('Tea', 270, 25, 1.5, 90)
        display.text('Made:', 225, 0, 1.5, 90)
        
        # Get time from the RTC and check for 12/24hr mode
        hour = handleTimezone()
        minute = rtcbreakout.get_minutes()
        
        amPm = ''
        if twelveTwentyfour:
            amPm = 'am'
            if hour > 11:
                amPm = 'pm'
                if hour > 12:
                    hour = hour - 12
            
        minString = str(minute)
        if minute < 10:
            minString = '0' + str(minute)
        hourString = str(hour)
        if hour < 10:
            hourString = '0' + str(hour)
            
        # Carry-on writing to the screen
        nowTime = '' + hourString + ':' + minString        
        display.text(nowTime, 180, 0, 1.4, 90)
        display.thickness(2)
        display.text(amPm, 150, 90, 0.7, 90)
        # Add the teapot image, draw to the screen, and finally wipe the message
        display.image(teapot, 120, 120, 5,5)
        display.update()
        message = None
        #Kill power to the board once the screen has updated
        display.halt()
        
    elif debugScreen is not None:
        # Clear previous message
        display.pen(15)
        display.clear()
        display.pen(0)
        display.thickness(2)
        display.text('^         ', 285, 25, 0.5, 90)
        
        #add screen-specific controls
        if debugMode == 1:
            display.text('Min-1 >', 155, 60, 0.5, 90)
            display.text('Min+1 >', 250, 60, 0.5, 90)
        else:
            display.text('Hour-1 >', 155, 50, 0.5, 90)
            display.text('Hour+1 >', 250, 50, 0.5, 90)
            
        display.text('Change page', 275, 20, 0.5, 90)
        display.text('Exit >', 38, 80, 0.5, 90)
        
        hour = handleTimezone()
        if hour < 10:
            hour = '0' + str(hour)
        minute = rtcbreakout.get_minutes()
        if minute < 10:
            minute = '0' + str(minute)
        seconds = rtcbreakout.get_seconds()
        if seconds < 10:
            seconds = '0' + str(seconds)
        
        nowTime = ''+str(hour) + ':' + str(minute) + ':' + str(seconds)
        if bst:
            nowTime += ' BST'
        else:
            nowTime += ' GMT'
        display.text(nowTime, 0,30,0.75,0)
        
        display.update()
        debugScreen = None


#to do -
    #consider stewed timer?