#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

from bs4 import BeautifulSoup

class waldhof:
    def getNewFootballTable(self):
        #try:
        #  execfile('./ExtractWeb.py')
        #except:
        #  pass
        self.table_data = [[[] for _ in range(4)] for _ in range(5)]
        soccertable_path = '/programs/office_display/soccer/soccertable.xml'
        soccertable_path = './soccer/soccertable.xml'
        
        with open(soccertable_path) as f:
            self.content = f.read()
        f.close()

        self.soccertable_xml = BeautifulSoup(self.content, 'html.parser')
        self.soccertable = self.soccertable_xml.find('soccertable')
        self.soccerteam = self.soccertable.find('soccer')

        for self.soccerteam_counter in range(0,5):
            self.place = self.soccerteam.find('place')
            self.table_data[self.soccerteam_counter][0] = self.place.contents[0]
            self.name = self.soccerteam.find('name')
            self.table_data[self.soccerteam_counter][1] = self.name.contents[0]
            self.point_difference = self.soccerteam.find('difference')
            self.table_data[self.soccerteam_counter][2] = self.point_difference.contents[0]
            self.points = self.soccerteam.find('points')
            self.table_data[self.soccerteam_counter][3] = self.points.contents[0]
            self.soccerteam = self.soccerteam.find_next('soccer')
        
        return self.table_data
