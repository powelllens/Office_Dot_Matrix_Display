#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import time, sys, random, os.path, datetime as dt
from bs4 import BeautifulSoup
from display_class import *
from waldhof import *
from adler import *

global debug
global lockfile_path
global loadnewconfig
global select
global switchontime
global switchofftime
global activerandom
global activated_modes
global time_modes
global quote_array
global displayBrightness
global animation_length
global animation_frame_delay
global config

debug = False

# Waldhof class init
waldhof = waldhof()
adler = adler()

lockfile_path = './LOCKFILE'
loadnewconfig = True

#define all necessary variables
select = 0
switchontime = 0
switchofftime = 24
activerandom = True

# Load mode specific config
activated_modes = [False,False,False,False,False,False,False,False]
time_modes = [1,1,1,1,1,1,1,1]

quote_array = []

# Init and rename Display Class with rows,chain,parallel,pwmbits,brightness,luminaceCorrection
displayBrightness = 10
display = display_class(32,6,1,11,displayBrightness,True)

#example to draw text
#display.drawtext(x,y,"EXAPMLE-Text","7x14B",R,G,B,True)

#example to draw images
#showimage(x,y,"./images/icon.png")

#example to update the screen
#display.updateScreen()

#example to clear the canvas
#display.clearoffsetScreen()

def str2bool(v):
    if v == 'True':
        return True
    else:
        return False

def loadingConfig():
    global config
    global select
    global switchontime
    global switchofftime
    global activerandom
    global activated_modes
    global time_modes
    global quote_array
    global displayBrightness
    global animation_length
    global animation_frame_delay

    config_path = './displayconfig.xml'
    quotes_path = './quotes.txt'
    animations_path = './animations'

    if debug:
        print 'Config File is avaliable?: ' + str(os.path.isfile(config_path))

    with open(config_path) as f:
        content = f.read()
    f.close()

    config = BeautifulSoup(content, 'html.parser')
    # print(config.prettify())

    # Load over all display settings
    select = int(config.settings.startwithmode.contents[0])

    switchontime = int(config.settings.switchontime.contents[0])
    switchofftime = int(config.settings.switchofftime.contents[0])
    displayBrightness = int(config.settings.displaybrightness.contents[0])
    activerandom = str2bool(config.settings.activaterandom.contents[0])
    display.setBrightness(displayBrightness)

    # welcome
    activated_modes[0] = str2bool(config.modes.welcome.activate.contents[0])
    time_modes[0] = int(config.modes.welcome.time.contents[0])
    # revenuecounter
    activated_modes[1] = str2bool(config.modes.revenuecounter.activate.contents[0])
    time_modes[1] = int(config.modes.revenuecounter.time.contents[0])
    # employee
    activated_modes[2] = str2bool(config.modes.employee.activate.contents[0])
    time_modes[2] = int(config.modes.employee.time.contents[0])
    # soccertable
    activated_modes[3] = str2bool(config.modes.soccertable.activate.contents[0])
    time_modes[3] = int(config.modes.soccertable.time.contents[0])
    # freudenberglogo
    activated_modes[4] = str2bool(config.modes.freudenberglogo.activate.contents[0])
    time_modes[4] = int(config.modes.freudenberglogo.time.contents[0])
    # hockeytable
    activated_modes[5] = str2bool(config.modes.hockeytable.activate.contents[0])
    time_modes[5] = int(config.modes.hockeytable.time.contents[0])
    # quotes
    activated_modes[6] = str2bool(config.modes.quotes.activate.contents[0])
    time_modes[6] = int(config.modes.quotes.time.contents[0])
    # animations
    activated_modes[7] = str2bool(config.modes.animations.activate.contents[0])
    time_modes[7] = int(config.modes.animations.time.contents[0])

    #Load Quote Array
    f = open(quotes_path, 'r')
    quote_array = []
    for line in f:
        quote_array.append(line)
    f.close

    # Load animations to buffer for preprocessing the animations
    if activated_modes[7]:
        if debug:
            print 'Try to buffer the animated images...'

        display.clearoffsetScreen()
        display.drawtext(6,1,"Loading Config...","7x13B",5,148,208,True)
        display.updateScreen()

        animation_length, animation_frame_delay = display.load_animations(animations_path)

        display.clearoffsetScreen()
        display.updateScreen()

        if debug:
            print 'Animations lengths:', animation_length

def Routine_Welcome():
    global config
    global loadnewconfig
    if debug:
        print 'Print Welcome Screen'
    #**********************************************************
    # Welcome Programm
    start_time = time.time()
    past_time = 0.0

    if len(config.modes.welcome.contents[5]) > 0:
        person_name = config.modes.welcome.contents[5].contents[0]
    else:
        person_name = ''

    xPosition = 100 - (len(person_name) * 3.5)

    display.clearoffsetScreen()

    display.drawtext(6,1,"Welcome to the Office:","7x13B",5,148,208,True)
    display.drawtext(xPosition,18,person_name,"7x13B",5,148,208,True)
    display.updateScreen()

    while past_time < time_modes[0]:
        # Programm sequence...

        if os.path.isfile(lockfile_path):
            loadnewconfig = True
            if debug:
                print 'found a LOCKFILE'
            break

        time.sleep(0.5)
        end_time = time.time()
        past_time = round(end_time - start_time,0)

def Routine_RevenueCounter():
    global config
    global loadnewconfig
    if debug:
        print 'Print Revenue Counter'
    #**********************************************************
    # Programm Part for the Revenue Counter:
    start_time = time.time()
    past_time = 0.0

    price = int(config.modes.revenuecounter.value.contents[0])

    while past_time < time_modes[1]:
        # Programm sequence...

        # check if a new config is avaliable
        if os.path.isfile(lockfile_path):
            loadnewconfig = True
            if debug:
                print 'found a LOCKFILE'
            break

        # Calculate the new time difference
        a = dt.datetime.now()
        b = dt.datetime(dt.datetime.now().year,01,01,00,00,00)
        saved_money = "%8.2f $"% round((price / 31536000.0) * (a-b).total_seconds(),2)
        xPosition = 100 - (len(saved_money) * 3.5)

        display.clearoffsetScreen()
        display.drawtext(6,1,"INNOVATION REVENUE","7x13B",0,74,193,True)
        display.drawtext(61,11,"- COUNTER -","7x13B",5,148,208,True)
        display.drawtext(xPosition,22,saved_money,"7x13B",216,228,249,True)
        #display.drawtext(1,24,str(past_time),"5x8",10,10,10,True)
        display.updateScreen()
        time.sleep(0.05)

        end_time = time.time()
        past_time = round(end_time - start_time,0)

def Routine_Employee():
    global config
    global loadnewconfig
    if debug:
        print 'Print Employees'
    #**********************************************************
    # Programm Part for Employee:
    start_time = time.time()
    past_time = 0.0
    employee = 0
    employeelog = [-1,-1,-1,-1,-1]
    employeelogcounter = 0
    displayimage = False
    line_number = 1

    while past_time < time_modes[2]:
        # Programm sequence...

        # check if a new config is avaliable
        if os.path.isfile(lockfile_path):
            loadnewconfig = True
            if debug:
                print 'found a LOCKFILE'
            break

        errorcounter = 0
        while employee in employeelog and errorcounter < 100:
            employee = int(round(random.random()*4,0))
            errorcounter = errorcounter + 1
        employeelog[employeelogcounter] = employee
        employeelogcounter = employeelogcounter + 1

        if employeelogcounter > 4:
            employeelog = [-1,-1,-1,-1,-1]
            employeelogcounter = 0

        try:
            display.clearoffsetScreen()

            employee_tmp = getattr(config.modes.employee, 'employee_' + str(employee + 1))
            if len(employee_tmp.contents[1]) > 0:
                display.drawtext(0,0,str(employee_tmp.contents[1].contents[0]),"7x13B",255,255,255,True)
                for line_number in range(1, 3):
                    if len(getattr(employee_tmp, 'line' + str(line_number))) > 0:
                        line_tmp = getattr(employee_tmp, 'line' + str(line_number))
                        display.drawtext(int(line_tmp['x']),
                                         int(line_tmp['y']),
                                         str(line_tmp.contents[0]),
                                         str(line_tmp['font']),
                                         int(line_tmp['red']),
                                         int(line_tmp['green']),
                                         int(line_tmp['blue']),True)
                if len(employee_tmp.contents[9]) > 0:
                    display.showimage(160,0,str(employee_tmp.contents[9].contents[0]))
                displayimage = True

            display.updateScreen()

        except:
            print "Unexpected error in Employee:", sys.exc_info()[0]
            if debug:
                print 'Employee: ' + str(employee)
                print 'Faild to display part of employee config'
            break

        if not debug:
            if displayimage:
                time.sleep(5)
                displayimage = False
        else:
            print employeelog
            time.sleep(2)

        end_time = time.time()
        past_time = round(end_time - start_time,0)

def Routine_Soccer():
    global loadnewconfig
    if debug:
        print 'Print Soccer'
    #**********************************************************
    # Programm Part for the Soccer table:
    start_time = time.time()
    past_time = 0.0
    while past_time < time_modes[3]:

        display.clearoffsetScreen()
        display.drawtext(2,2,"Preparing Football","8x13B",0,74,193,True)
        display.drawtext(1,18,"Tables...","8x13B",5,148,208,True)
        display.updateScreen()

        soccertable = waldhof.getNewFootballTable()

        try:
            if debug:
                print 'Try to connect to Waldhof'
            soccertable = waldhof.getNewFootballTable()

            if debug:
                print 'Recieved a soccertable'

            waldhof_check = False

            for i in range(0,4):
                if 'Waldhof' in soccertable[i][1]:
                    waldhof_check = True
                    if debug:
                        print 'Waldhof found in the table'
        except:
            if debug:
                print 'failed to load table'
            break

        if waldhof_check == False:
            if debug:
                print 'Waldhof in the table not avaliable'
            break

        # Programm sequence...

        x = 0
        i = 0

        for i in range(0,5):
            if i < 5:
                display.clearoffsetScreen()
                display.drawtext(1,x + 4,soccertable[i][0],"7x14B",255,255,255,True)
                display.drawtext(7,x + 5,'. ' + soccertable[i][1],"6x13",255,255,255,True)
                display.drawtext(1,x + 19,'Goal dif: ' + soccertable[i][2],"6x10",255,255,255,True)
                display.drawtext(85,x + 19,'Points: ' + soccertable[i][3],"6x10",255,255,255,True)
                display.showimage(160,x + 5,'./images/' + str(i+1) + '_soccer.png')
                display.updateScreen()
                if not debug:
                    time.sleep(4)
                else:
                    time.sleep(1)

            # check if a new config is avaliable
            if os.path.isfile(lockfile_path):
                loadnewconfig = True
                if debug:
                    print 'found a LOCKFILE'
                break

            if i < 4:
                for x in range(0,-34,-2):
                    display.clearoffsetScreen()

                    display.drawtext(1,x + 4,soccertable[i][0],"7x14B",255,255,255,True)
                    display.drawtext(7,x + 5,'. ' + soccertable[i][1],"6x13",255,255,255,True)
                    display.drawtext(1,x + 19,'Goal dif: ' + soccertable[i][2],"6x10",255,255,255,True)
                    display.drawtext(85,x + 19,'Points: ' + soccertable[i][3],"6x10",255,255,255,True)
                    display.showimage(160,x+5,'./images/' + str(i+1) + '_soccer.png')

                    display.drawtext(1,x + 36,soccertable[i+1][0],"7x14B",255,255,255,True)
                    display.drawtext(7,x + 37,'. ' + soccertable[i+1][1],"6x13",255,255,255,True)
                    display.drawtext(1,x + 51,'Goal dif: ' + soccertable[i+1][2],"6x10",255,255,255,True)
                    display.drawtext(85,x + 51,'Points: ' + soccertable[i+1][3],"6x10",255,255,255,True)
                    display.showimage(160,x + 37,'./images/' + str(i+2) + '_soccer.png')

                    display.updateScreen()
                    if not debug:
                        time.sleep(0.1)
            x = 0
        end_time = time.time()
        past_time = round(end_time - start_time,0)

def Routine_Logo():
    global loadnewconfig
    if debug:
        print 'Print Logo'
    #**********************************************************
    # Programm Part for Freudenberg Logo:
    start_time = time.time()
    past_time = 0.0

    display.clearoffsetScreen()
    display.showimage(0,8,"./images/freudenberg.png")
    display.updateScreen()

    while past_time < time_modes[4]:

        # Programm sequence...
        # check if a new config is avaliable
        if os.path.isfile(lockfile_path):
            loadnewconfig = True
            if debug:
                print 'found a LOCKFILE'
            break

        time.sleep(1)

        end_time = time.time()
        past_time = round(end_time - start_time,0)

def Routine_Hockey():
    global loadnewconfig
    if debug:
        print 'Print Hockey'
    #**********************************************************
    # Programm Part for the Hockey table:
    start_time = time.time()
    past_time = 0.0
    while past_time < time_modes[5]:

        display.clearoffsetScreen()
        display.drawtext(2,2,"Preparing Hockey","8x13B",0,74,193,True)
        display.drawtext(1,18,"Tables...","8x13B",5,148,208,True)
        display.updateScreen()

        try:
            if debug:
                print 'Try to connect to Adler'
            hockeytable = adler.getNewHockeyTable()
            if debug:
                print 'Recieved a Hockeytable'
        except:
            if debug:
                print 'failed to load table'
            break

        # Programm sequence...

        x = 0
        i = 0

        for i in range(0,5):
            if i < 5:
                display.clearoffsetScreen()
                display.drawtext(1,x,str(hockeytable[i][0]),"7x14B",255,255,255,True)
                display.drawtext(7,x + 1,'. ' + hockeytable[i][1],"6x13",255,255,255,True)
                display.drawtext(1,x + 15,'Games: ' + hockeytable[i][2],"6x9",255,255,255,True)
                display.drawtext(67,x + 15,'Points: ' + hockeytable[i][3],"6x9",255,255,255,True)
                display.drawtext(1,x + 24,'Goals: ' + hockeytable[i][4] + ':' + hockeytable[i][5],"6x9",255,255,255,True)
                display.showimage(160,x + 5,'./images/' + str(i+1) + '_hockey.png')
                display.updateScreen()
                if not debug:
                    time.sleep(4)
                else:
                    time.sleep(1)

            # check if a new config is avaliable
            if os.path.isfile(lockfile_path):
                loadnewconfig = True
                if debug:
                    print 'found a LOCKFILE'
                break

            if i < 4:
                for x in range(0,-32,-2):
                    display.clearoffsetScreen()

                    display.drawtext(1,x,hockeytable[i][0],"7x14B",255,255,255,True)
                    display.drawtext(7,x + 1,'. ' + hockeytable[i][1],"6x13",255,255,255,True)
                    display.drawtext(1,x + 15,'Games: ' + hockeytable[i][2],"6x9",255,255,255,True)
                    display.drawtext(67,x + 15,'Points: ' + hockeytable[i][3],"6x9",255,255,255,True)
                    display.drawtext(1,x + 24,'Goals: ' + hockeytable[i][4] + ':' + hockeytable[i][5],"6x9",255,255,255,True)
                    display.showimage(160,x + 5,'./images/' + str(i+1) + '_hockey.png')

                    display.drawtext(1,x + 32,hockeytable[i+1][0],"7x14B",255,255,255,True)
                    display.drawtext(7,x + 33,'. ' + hockeytable[i+1][1],"6x13",255,255,255,True)
                    display.drawtext(1,x + 47,'Games: ' + hockeytable[i+1][2],"6x9",255,255,255,True)
                    display.drawtext(67,x + 47,'Points: ' + hockeytable[i+1][3],"6x9",255,255,255,True)
                    display.drawtext(1,x + 56,'Goals: ' + hockeytable[i+1][4] + ':' + hockeytable[i+1][5],"6x9",255,255,255,True)
                    display.showimage(160,x + 37,'./images/' + str(i+2) + '_hockey.png')

                    display.updateScreen()
                    if not debug:
                        time.sleep(0.1)
            x = 0
        end_time = time.time()
        past_time = round(end_time - start_time,0)

def Routine_Quotes():
    global loadnewconfig
    if debug:
        print 'Print Quotes'
    #**********************************************************
    # Programm Part for the quotes table:#
    start_time = time.time()
    past_time = 0.0
    while past_time < time_modes[6]:
        linenumber = int(round(random.random()*(len(quote_array)-1),0))
        tmp = str.split(quote_array[linenumber],'-')
        display.clearoffsetScreen()
        for x in range(0,len(tmp)):
            if len(tmp[x]) > 3:
                display.drawtext(0,x*11,tmp[x],"6x10",255,255,255,True)
        display.updateScreen()

        # check if a new config is avaliable
        if os.path.isfile(lockfile_path):
            loadnewconfig = True
            if debug:
                print 'found a LOCKFILE'
            break

        time.sleep(10)

        end_time = time.time()
        past_time = round(end_time - start_time,0)

def Routine_animations():
    global loadnewconfig
    global animation_length
    global animation_frame_delay

    if debug:
        print 'Print Animations'

    display.matrix.Fill(0,0,0)

    start_time = time.time()
    past_time = 0.0

    animation_number = int(round(random.random()*(len(animation_length)-1),0))
    frame = 0
    max_frame = animation_length[animation_number]
    delay = animation_frame_delay[animation_number] / 1000.0
    Loop_play = False

    while past_time < time_modes[7]:

        display.show_animation_image(animation_number,frame)

        time.sleep(delay)

        # check if a new config is avaliable
        if os.path.isfile(lockfile_path):
            loadnewconfig = True
            if debug:
                print 'found a LOCKFILE'
            break

        frame += 1
        if frame > max_frame:
            frame = 0
            Loop_play = True

        end_time = time.time()
        past_time = round(end_time - start_time,0)


def Main():
    global select
    global loadnewconfig
    global displayBrightness

    screenlog = [-1,-1,-1,-1,-1,-1,-1,-1]
    screenlogcounter = 0

    while True:
        if loadnewconfig:
            # After a Systemstart, the standard values are loaded
            try:
                if debug:
                    print 'loading Config...'
                loadingConfig()
                if debug:
                    print 'Finished loading!'
            except:
                if debug:
                    print 'Error during Config loading!'
            try:
                if os.path.isfile(lockfile_path):
                    os.remove('./LOCKFILE')
            except:
                if debug:
                    print 'No File to delete!'
                continue
            loadnewconfig = False
        else:
            if activerandom:
                errorcounter = 0
                while select in screenlog and errorcounter < 100:
                    select = int(round(random.random()*7,0))
                    errorcounter = errorcounter + 1
                screenlog[screenlogcounter] = select
                screenlogcounter = screenlogcounter + 1
                if screenlogcounter > 7:
                    screenlog = [-1,-1,-1,-1,-1,-1,-1,-1]
                    screenlogcounter = 0
            else:
                select = select + 1
                if select > 7:
                    select = 0

        #Disable the Display if the time is out of setting and if it's weekend
        weekday = dt.date.today().isoweekday()
        hournow = dt.datetime.now().hour

        if  weekday > 7 or hournow >= switchofftime or hournow < switchontime:
            if debug:
                print 'Switch off Panels! Weekday: ' + str(weekday) + ' Hour: ' + str(hournow)
                print 'Switch off/on time: ' + str(switchofftime) + ' ' + str(switchontime)
            display.clearoffsetScreen()
            display.updateScreen()
            # To slow down things add Time
            time.sleep(1)
        else:

            if select == 0 and activated_modes[0]:
                Routine_Welcome()
            elif select == 1 and activated_modes[1]:
                Routine_RevenueCounter()
            elif select == 2 and activated_modes[2]:
                Routine_Employee()
            elif select == 3 and activated_modes[3]:
                Routine_Soccer()
            elif select == 4 and activated_modes[4]:
                Routine_Logo()
            elif select == 5 and activated_modes[5]:
                Routine_Hockey()
            elif select == 6 and activated_modes[6]:
                Routine_Quotes()
            elif select == 7 and activated_modes[7]:
                Routine_animations()
                display.matrix.SwapOnVSync(display.offsetCanvas)

        if os.path.isfile(lockfile_path):
            loadnewconfig = True


try:
    Main()

except:
    print "Unexpected error:", sys.exc_info()[0]
    raise
    display.matrix.Clear
    sys.exit(0)
