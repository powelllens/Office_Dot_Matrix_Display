#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import urllib2
import shutil

class waldhof:
    def getNewFootballTable(self):
        self.url = 'file:./offline_page/svw07_home.htm'
        self.f = urllib2.urlopen(self.url)
        self.table_data = [[[] for _ in range(4)] for _ in range(5)]

        i = 0
        self.table_point = 0
        while i < 2000:
            self.line = self.f.readline()
            if '<TD class="views-field views-field-counter">' in self.line:
                self.table_data[self.table_point][0] = self.line[(self.line.find('counter">')+9):-(len(self.line)-self.line.find('</TD>'))]
                self.line = self.f.readline()
                self.line = self.f.readline()
                self.line = self.f.readline()
                self.image = self.line[(self.line.find('src">')+19):-(len(self.line)-self.line.find('</TD>')+2)]
                self.line = self.f.readline()
                self.table_data[self.table_point][1] = self.line[(self.line.find('title">')+7):-(len(self.line)-self.line.find('</TD>'))]
                self.line = self.f.readline()
                self.table_data[self.table_point][2] = self.line[(self.line.find('difference">')+12):-(len(self.line)-self.line.find('</TD>'))]
                self.line = self.f.readline()
                self.table_data[self.table_point][3] = self.line[(self.line.find('points">')+8):-(len(self.line)-self.line.find('</TD>'))]

                self.imagelocation = './offline_page/' + self.image
                self.image_name = './images/' + self.table_data[self.table_point][0] + '_soccer.png'
                shutil.copy(self.imagelocation, self.image_name)
                #image = urllib2.URLopener()
                #image.retrieve(self.url,self.image_name)

                self.table_point = self.table_point + 1
            if self.table_point > 4:
                break
            i = i + 1
        self.f.close()
        return self.table_data
