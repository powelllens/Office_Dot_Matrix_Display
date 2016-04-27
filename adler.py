#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import urllib2
import shutil

class adler:
    def getNewHockeyTable(self):
        self.url = 'file:./offline_page/hockey_table.htm'
        self.f = urllib2.urlopen(self.url)
        self.table_data = [[[] for _ in range(6)] for _ in range(5)]
        i = 0
        self.found_line = False
        while i < 500:
            self.line = self.f.readline()
            if '<TBODY>' in self.line:
                self.found_line = True
                break
            i = i + 1

        if self.found_line == True:
            for i  in range(0, 5):
                self.line = self.f.readline()
                self.line = self.f.readline()
                self.line = self.f.readline()
                # Platz
                self.table_data[i][0] = self.line[(self.line.find('acenter">')+9):-(len(self.line)-self.line.find('</TD>'))]
                for u in range(0,3):
                    self.line = self.f.readline()
                # Image
                self.image = self.line[(self.line.find('src="')+5):-(len(self.line)-self.line.find('"><A'))]
                self.imagelocation = './offline_page/' + self.image
                self.image_name = './images/' + self.table_data[i][0] + '_hockey.png'
                shutil.copy(self.imagelocation, self.image_name)
                # Name
                self.table_data[i][1] = self.line[(self.line.find('alt="')+5):-(len(self.line)-self.line.find('" src="'))]
                self.line = self.f.readline()
                self.line = self.f.readline()
                self.line = self.f.readline()
                # Games
                self.table_data[i][2] = self.line[(self.line.find('acenter">')+9):-(len(self.line)-self.line.find('</TD>'))]
                for u in range(0,7):
                    self.line = self.f.readline()
                # Points
                self.table_data[i][3] = self.line[(self.line.find('highlight">')+11):-(len(self.line)-self.line.find('</TD>'))]
                self.line = self.f.readline()
                self.line = self.f.readline()
                # Goals
                self.table_data[i][4] = self.line[(self.line.find('acenter">')+9):-(len(self.line)-self.line.find('</TD>'))]
                self.line = self.f.readline()
                # Enemy Goal
                self.table_data[i][5] = self.line[(self.line.find('acenter">')+9):-(len(self.line)-self.line.find('</TD>'))]
        self.f.close()
        return self.table_data