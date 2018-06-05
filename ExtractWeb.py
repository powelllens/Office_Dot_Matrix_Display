#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
"""
Created on Tue Nov 28 10:57:18 2017

@author: DAVIDRUCKES
"""

from bs4 import BeautifulSoup
import urllib
import os
import sys

program_path = os.path.dirname(sys.argv[0])
link = 'https://www.svw07.de/home'
table_data = [[[] for _ in range(4)] for _ in range(5)]

try:
    webpage = urllib.urlopen(link)          
    webpagecontent = webpage.read()
except Exception as e:
    print('*** Failed to reach Homepage of SV07 ***')
    print('*** Caught exception: ' + str(e.__class__) + ': ' + str(e))
    sys.exit(1)
    
soup = BeautifulSoup(webpagecontent, 'html.parser')

#Create table with all games
table = soup.find('table', id="kurztabelle")
#search for the first content relevant table (no header)
tr = table.find('tr').find_next('tr')
for tr_counter in range(0,5):
    td = tr.find_next('td')
    for td_counter in range(0,5):
        if td_counter == 1:
            image_path = td.img['src']
        else:
            if td_counter < 1:
                table_data[tr_counter][td_counter] = td.contents[0] 
            else:
                table_data[tr_counter][td_counter-1] = td.contents[0]
        td = td.find_next('td')
            
    tr = tr.find_next('tr')
    imagelocation = image_path
    image_name = './soccer/images/' + str(table_data[tr_counter][0]) + '_soccer.png'
    urllib.urlretrieve(image_path, image_name)

soccertable_path = './soccer/soccertable.xml'

with open(soccertable_path) as f:
    content = f.read()
f.close()

soccertable_xml = BeautifulSoup(content, 'html.parser')
soccertable = soccertable_xml.find('soccertable')
soccerteam = soccertable.find('soccer')

for soccerteam_counter in range(0,5):
    place = soccerteam.find('place')
    place.string = table_data[soccerteam_counter][0]
    name = soccerteam.find('name')
    name.string = table_data[soccerteam_counter][1]
    point_difference = soccerteam.find('difference')
    point_difference.string = table_data[soccerteam_counter][2]
    points = soccerteam.find('points')
    points.string = table_data[soccerteam_counter][3]
    soccerteam = soccerteam.find_next('soccer')

xml_file = soccertable_xml
f = open(soccertable_path,'w')
f.write(xml_file.encode('utf-8'))
f.close()
