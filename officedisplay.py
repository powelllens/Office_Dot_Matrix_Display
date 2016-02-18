#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import time, sys, random, os.path, datetime as dt, untangle
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
    global select
    global switchontime
    global switchofftime
    global activerandom
    global configobj
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

    configobj = untangle.parse(config_path)

    # Load over all display settings
    select = int(configobj.config.settings.startwithmode.cdata)

    switchontime = int(configobj.config.settings.switchontime.cdata)
    switchofftime = int(configobj.config.settings.switchofftime.cdata)
    displayBrightness = int(configobj.config.settings.displaybrightness.cdata)
    activerandom = str2bool(configobj.config.settings.activaterandom.cdata)
    display.setBrightness(displayBrightness)

    # welcome
    activated_modes[0] = str2bool(configobj.config.modes.welcome.activate.cdata)
    time_modes[0] = int(configobj.config.modes.welcome.time.cdata)
    # revenuecounter
    activated_modes[1] = str2bool(configobj.config.modes.revenuecounter.activate.cdata)
    time_modes[1] = int(configobj.config.modes.revenuecounter.time.cdata)
    # employee
    activated_modes[2] = str2bool(configobj.config.modes.employee.activate.cdata)
    time_modes[2] = int(configobj.config.modes.employee.time.cdata)
    # soccertable
    activated_modes[3] = str2bool(configobj.config.modes.soccertable.activate.cdata)
    time_modes[3] = int(configobj.config.modes.soccertable.time.cdata)
    # logo
    activated_modes[4] = str2bool(configobj.config.modes.freudenberglogo.activate.cdata)
    time_modes[4] = int(configobj.config.modes.freudenberglogo.time.cdata)
    # hockeytable
    activated_modes[5] = str2bool(configobj.config.modes.hockeytable.activate.cdata)
    time_modes[5] = int(configobj.config.modes.hockeytable.time.cdata)
    # quotes
    activated_modes[6] = str2bool(configobj.config.modes.quotes.activate.cdata)
    time_modes[6] = int(configobj.config.modes.quotes.time.cdata)
    # animations
    activated_modes[7] = str2bool(configobj.config.modes.animations.activate.cdata)
    time_modes[7] = int(configobj.config.modes.animations.time.cdata)

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
    global loadnewconfig
    if debug:
        print 'Print Welcome Screen'
    #**********************************************************
    # Welcome Programm
    start_time = time.time()
    past_time = 0.0

    person_name = str(configobj.config.modes.welcome.name.cdata)

    xPosition = 100 - (len(person_name) * 3.5)

    display.clearoffsetScreen()
    display.drawtext(6,1,"Welcome to the GPT Office:","7x13B",5,148,208,True)
    #display.drawtext(6,1,"Happy Birthday","7x13B",5,148,208,True)
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
    global loadnewconfig
    if debug:
        print 'Print Revenue Counter'
    #**********************************************************
    # Programm Part for the Revenue Counter:
    start_time = time.time()
    past_time = 0.0

    price = int(configobj.config.modes.revenuecounter.value.cdata)

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
        display.drawtext(6,1,"GPT P&D INNOVATION REVENUE","7x13B",0,74,193,True)
        display.drawtext(61,11,"- COUNTER -","7x13B",5,148,208,True)
        display.drawtext(xPosition,22,saved_money,"7x13B",216,228,249,True)
        #display.drawtext(1,24,str(past_time),"5x8",10,10,10,True)
        display.updateScreen()
        time.sleep(0.05)

        end_time = time.time()
        past_time = round(end_time - start_time,0)

def Routine_Employee():
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
            if employee == 0:
                if str(configobj.config.modes.employee.employee_1.name.cdata) != '':
                    display.drawtext(0,0,str(configobj.config.modes.employee.employee_1.name.cdata),"7x13B",255,255,255,True)
                    if str(configobj.config.modes.employee.employee_1.line1.cdata) != '':
                        display.drawtext(int(configobj.config.modes.employee.employee_1.line1['x']),
                                         int(configobj.config.modes.employee.employee_1.line1['y']),
                                         str(configobj.config.modes.employee.employee_1.line1.cdata),
                                         str(configobj.config.modes.employee.employee_1.line1['font']),
                                         int(configobj.config.modes.employee.employee_1.line1['red']),
                                         int(configobj.config.modes.employee.employee_1.line1['green']),
                                         int(configobj.config.modes.employee.employee_1.line1['blue']),True)
                    if str(configobj.config.modes.employee.employee_1.line2.cdata) != '':
                        display.drawtext(int(configobj.config.modes.employee.employee_1.line2['x']),
                                         int(configobj.config.modes.employee.employee_1.line2['y']),
                                         str(configobj.config.modes.employee.employee_1.line2.cdata),
                                         str(configobj.config.modes.employee.employee_1.line2['font']),
                                         int(configobj.config.modes.employee.employee_1.line2['red']),
                                         int(configobj.config.modes.employee.employee_1.line2['green']),
                                         int(configobj.config.modes.employee.employee_1.line2['blue']),True)
                    if str(configobj.config.modes.employee.employee_1.line3.cdata) != '':
                        display.drawtext(int(configobj.config.modes.employee.employee_1.line3['x']),
                                         int(configobj.config.modes.employee.employee_1.line3['y']),
                                         str(configobj.config.modes.employee.employee_1.line3.cdata),
                                         str(configobj.config.modes.employee.employee_1.line3['font']),
                                         int(configobj.config.modes.employee.employee_1.line3['red']),
                                         int(configobj.config.modes.employee.employee_1.line3['green']),
                                         int(configobj.config.modes.employee.employee_1.line3['blue']),True)
                    if str(configobj.config.modes.employee.employee_1.image.cdata) != '':
                        display.showimage(161,0,str(configobj.config.modes.employee.employee_1.image.cdata))
                    displayimage = True

            elif employee == 1:
                if str(configobj.config.modes.employee.employee_2.name.cdata) != '':
                    display.drawtext(0,0,str(configobj.config.modes.employee.employee_2.name.cdata),"7x13B",255,255,255,True)
                    if str(configobj.config.modes.employee.employee_2.line1.cdata) != '':
                        display.drawtext(int(configobj.config.modes.employee.employee_2.line1['x']),
                                         int(configobj.config.modes.employee.employee_2.line1['y']),
                                         str(configobj.config.modes.employee.employee_2.line1.cdata),
                                         str(configobj.config.modes.employee.employee_2.line1['font']),
                                         int(configobj.config.modes.employee.employee_2.line1['red']),
                                         int(configobj.config.modes.employee.employee_2.line1['green']),
                                         int(configobj.config.modes.employee.employee_2.line1['blue']),True)
                    if str(configobj.config.modes.employee.employee_2.line2.cdata) != '':
                        display.drawtext(int(configobj.config.modes.employee.employee_2.line2['x']),
                                         int(configobj.config.modes.employee.employee_2.line2['y']),
                                         str(configobj.config.modes.employee.employee_2.line2.cdata),
                                         str(configobj.config.modes.employee.employee_2.line2['font']),
                                         int(configobj.config.modes.employee.employee_2.line2['red']),
                                         int(configobj.config.modes.employee.employee_2.line2['green']),
                                         int(configobj.config.modes.employee.employee_2.line2['blue']),True)
                    if str(configobj.config.modes.employee.employee_2.line3.cdata) != '':
                        display.drawtext(int(configobj.config.modes.employee.employee_2.line3['x']),
                                         int(configobj.config.modes.employee.employee_2.line3['y']),
                                         str(configobj.config.modes.employee.employee_2.line3.cdata),
                                         str(configobj.config.modes.employee.employee_2.line3['font']),
                                         int(configobj.config.modes.employee.employee_2.line3['red']),
                                         int(configobj.config.modes.employee.employee_2.line3['green']),
                                         int(configobj.config.modes.employee.employee_2.line3['blue']),True)
                    if str(configobj.config.modes.employee.employee_2.image.cdata) != '':
                        display.showimage(161,0,str(configobj.config.modes.employee.employee_2.image.cdata))
                    displayimage = True

            elif employee == 2:
                if str(configobj.config.modes.employee.employee_3.name.cdata) != '':
                    display.drawtext(0,0,str(configobj.config.modes.employee.employee_3.name.cdata),"7x13B",255,255,255,True)
                    if str(configobj.config.modes.employee.employee_3.line1.cdata) != '':
                        display.drawtext(int(configobj.config.modes.employee.employee_3.line1['x']),
                                         int(configobj.config.modes.employee.employee_3.line1['y']),
                                         str(configobj.config.modes.employee.employee_3.line1.cdata),
                                         str(configobj.config.modes.employee.employee_3.line1['font']),
                                         int(configobj.config.modes.employee.employee_3.line1['red']),
                                         int(configobj.config.modes.employee.employee_3.line1['green']),
                                         int(configobj.config.modes.employee.employee_3.line1['blue']),True)
                    if str(configobj.config.modes.employee.employee_3.line2.cdata) != '':
                        display.drawtext(int(configobj.config.modes.employee.employee_3.line2['x']),
                                         int(configobj.config.modes.employee.employee_3.line2['y']),
                                         str(configobj.config.modes.employee.employee_3.line2.cdata),
                                         str(configobj.config.modes.employee.employee_3.line2['font']),
                                         int(configobj.config.modes.employee.employee_3.line2['red']),
                                         int(configobj.config.modes.employee.employee_3.line2['green']),
                                         int(configobj.config.modes.employee.employee_3.line2['blue']),True)
                    if str(configobj.config.modes.employee.employee_3.line3.cdata) != '':
                        display.drawtext(int(configobj.config.modes.employee.employee_3.line3['x']),
                                         int(configobj.config.modes.employee.employee_3.line3['y']),
                                         str(configobj.config.modes.employee.employee_3.line3.cdata),
                                         str(configobj.config.modes.employee.employee_3.line3['font']),
                                         int(configobj.config.modes.employee.employee_3.line3['red']),
                                         int(configobj.config.modes.employee.employee_3.line3['green']),
                                         int(configobj.config.modes.employee.employee_3.line3['blue']),True)
                    if str(configobj.config.modes.employee.employee_3.image.cdata) != '':
                        display.showimage(161,0,str(configobj.config.modes.employee.employee_3.image.cdata))
                    displayimage = True

            elif employee == 3:
                if str(configobj.config.modes.employee.employee_4.name.cdata) != '':
                    display.drawtext(0,0,str(configobj.config.modes.employee.employee_4.name.cdata),"7x13B",255,255,255,True)
                    if str(configobj.config.modes.employee.employee_4.line1.cdata) != '':
                        display.drawtext(int(configobj.config.modes.employee.employee_4.line1['x']),
                                         int(configobj.config.modes.employee.employee_4.line1['y']),
                                         str(configobj.config.modes.employee.employee_4.line1.cdata),
                                         str(configobj.config.modes.employee.employee_4.line1['font']),
                                         int(configobj.config.modes.employee.employee_4.line1['red']),
                                         int(configobj.config.modes.employee.employee_4.line1['green']),
                                         int(configobj.config.modes.employee.employee_4.line1['blue']),True)
                    if str(configobj.config.modes.employee.employee_4.line2.cdata) != '':
                        display.drawtext(int(configobj.config.modes.employee.employee_4.line2['x']),
                                         int(configobj.config.modes.employee.employee_4.line2['y']),
                                         str(configobj.config.modes.employee.employee_4.line2.cdata),
                                         str(configobj.config.modes.employee.employee_4.line2['font']),
                                         int(configobj.config.modes.employee.employee_4.line2['red']),
                                         int(configobj.config.modes.employee.employee_4.line2['green']),
                                         int(configobj.config.modes.employee.employee_4.line2['blue']),True)
                    if str(configobj.config.modes.employee.employee_4.line3.cdata) != '':
                        display.drawtext(int(configobj.config.modes.employee.employee_4.line3['x']),
                                         int(configobj.config.modes.employee.employee_4.line3['y']),
                                         str(configobj.config.modes.employee.employee_4.line3.cdata),
                                         str(configobj.config.modes.employee.employee_4.line3['font']),
                                         int(configobj.config.modes.employee.employee_4.line3['red']),
                                         int(configobj.config.modes.employee.employee_4.line3['green']),
                                         int(configobj.config.modes.employee.employee_4.line3['blue']),True)
                    if str(configobj.config.modes.employee.employee_4.image.cdata) != '':
                        display.showimage(161,0,str(configobj.config.modes.employee.employee_4.image.cdata))
                    displayimage = True

            elif employee == 4:
                if str(configobj.config.modes.employee.employee_5.name.cdata) != '':
                    display.drawtext(0,0,str(configobj.config.modes.employee.employee_5.name.cdata),"7x13B",255,255,255,True)
                    if str(configobj.config.modes.employee.employee_5.line1.cdata) != '':
                        display.drawtext(int(configobj.config.modes.employee.employee_5.line1['x']),
                                         int(configobj.config.modes.employee.employee_5.line1['y']),
                                         str(configobj.config.modes.employee.employee_5.line1.cdata),
                                         str(configobj.config.modes.employee.employee_5.line1['font']),
                                         int(configobj.config.modes.employee.employee_5.line1['red']),
                                         int(configobj.config.modes.employee.employee_5.line1['green']),
                                         int(configobj.config.modes.employee.employee_5.line1['blue']),True)
                    if str(configobj.config.modes.employee.employee_5.line2.cdata) != '':
                        display.drawtext(int(configobj.config.modes.employee.employee_5.line2['x']),
                                         int(configobj.config.modes.employee.employee_5.line2['y']),
                                         str(configobj.config.modes.employee.employee_5.line2.cdata),
                                         str(configobj.config.modes.employee.employee_5.line2['font']),
                                         int(configobj.config.modes.employee.employee_5.line2['red']),
                                         int(configobj.config.modes.employee.employee_5.line2['green']),
                                         int(configobj.config.modes.employee.employee_5.line2['blue']),True)
                    if str(configobj.config.modes.employee.employee_5.line3.cdata) != '':
                        display.drawtext(int(configobj.config.modes.employee.employee_5.line3['x']),
                                         int(configobj.config.modes.employee.employee_5.line3['y']),
                                         str(configobj.config.modes.employee.employee_5.line3.cdata),
                                         str(configobj.config.modes.employee.employee_5.line3['font']),
                                         int(configobj.config.modes.employee.employee_5.line3['red']),
                                         int(configobj.config.modes.employee.employee_5.line3['green']),
                                         int(configobj.config.modes.employee.employee_5.line3['blue']),True)
                    if str(configobj.config.modes.employee.employee_5.image.cdata) != '':
                        display.showimage(161,0,str(configobj.config.modes.employee.employee_5.image.cdata))
                    displayimage = True

            display.updateScreen()
        except:
            print "Unexpected error:", sys.exc_info()[0]
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
                for x in range(0,-32,-2):
                    display.clearoffsetScreen()

                    display.drawtext(1,x + 4,soccertable[i][0],"7x14B",255,255,255,True)
                    display.drawtext(7,x + 5,'. ' + soccertable[i][1],"6x13",255,255,255,True)
                    display.drawtext(1,x + 19,'Goal dif: ' + soccertable[i][2],"6x10",255,255,255,True)
                    display.drawtext(85,x + 19,'Points: ' + soccertable[i][3],"6x10",255,255,255,True)
                    display.showimage(160,x+5,'./images/' + str(i+1) + '_soccer.png')

                    display.drawtext(1,x + 34,soccertable[i+1][0],"7x14B",255,255,255,True)
                    display.drawtext(7,x + 35,'. ' + soccertable[i+1][1],"6x13",255,255,255,True)
                    display.drawtext(1,x + 49,'Goal dif: ' + soccertable[i+1][2],"6x10",255,255,255,True)
                    display.drawtext(85,x + 49,'Points: ' + soccertable[i+1][3],"6x10",255,255,255,True)
                    display.showimage(160,x + 35,'./images/' + str(i+2) + '_soccer.png')

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
                display.drawtext(1,x,hockeytable[i][0],"7x14B",255,255,255,True)
                display.drawtext(7,x + 1,'. ' + hockeytable[i][1],"6x13",255,255,255,True)
                display.drawtext(1,x + 15,'Games: ' + hockeytable[i][2],"6x9",255,255,255,True)
                display.drawtext(67,x + 15,'Points: ' + hockeytable[i][3],"6x9",255,255,255,True)
                display.drawtext(1,x + 24,'Goals: ' + hockeytable[i][4] + ':' + hockeytable[i][5],"6x9",255,255,255,True)
                display.showimage(160,x + 35,'./images/' + str(i+1) + '_hockey.png')
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
                    display.showimage(160,x + 35,'./images/' + str(i+1) + '_hockey.png')

                    display.drawtext(1,x,hockeytable[i][0],"7x14B",255,255,255,True)
                    display.drawtext(7,x + 31,'. ' + hockeytable[i][1],"6x13",255,255,255,True)
                    display.drawtext(1,x + 45,'Games: ' + hockeytable[i][2],"6x9",255,255,255,True)
                    display.drawtext(67,x + 45,'Points: ' + hockeytable[i][3],"6x9",255,255,255,True)
                    display.drawtext(1,x + 54,'Goals: ' + hockeytable[i][4] + ':' + hockeytable[i][5],"6x9",255,255,255,True)
                    display.showimage(160,x + 65,'./images/' + str(i+2) + '_hockey.png')

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

        display.show_animation_image(animation_number,frame,Loop_play)

        time.sleep(delay)

        # check if a new config is avaliable
        if os.path.isfile(lockfile_path):
            loadnewconfig = True
            if debug:
                print 'found a LOCKFILE'

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

        if os.path.isfile(lockfile_path):
            loadnewconfig = True


try:
    Main()

except:
    print "Unexpected error:", sys.exc_info()[0]
    raise
    display.matrix.Clear
    sys.exit(0)
