#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import sys
import glob
from rgbmatrix import RGBMatrix
from PIL import ImageFont, ImageDraw, Image

class display_class:
    global AnimationCanvas

    def __init__(self,rows,chain,parallel,pwmBits,brightness,luminanceCorrect):
        self.matrix = RGBMatrix(rows,chain,parallel)
        self.matrix.pwmBits = pwmBits
        self.matrix.brightness = brightness
        self.matrix.luminanceCorrect = luminanceCorrect
        # The canvas to work on without chanching the Screen
        self.offsetCanvas = self.matrix.CreateFrameCanvas()
        # Kill the screen at programm start
        self.offsetCanvas.Fill(0,0,0)
        self.offsetCanvas = self.matrix.SwapOnVSync(self.offsetCanvas)

    def setBrightness(self,brightness):
        self.matrix.brightness = brightness
        # The canvas to work on without chanching the Screen
        self.offsetCanvas = self.matrix.CreateFrameCanvas()
        self.offsetCanvas.Fill(0,0,0)
        self.offsetCanvas = self.matrix.SwapOnVSync(self.offsetCanvas)
        #print 'Brightsness is set to: ' + str(brightness)
        #print 'With type: ' + str(type(brightness))

    def setpwmBits(self,pwmBits):
        self.matrix.pwmBits = pwmBits

    def setluminaceCorrect(self,luminanceCorrect):
        self.matrix.luminanceCorrect = luminanceCorrect

    def updateScreen(self):
        self.offsetCanvas = self.matrix.SwapOnVSync(self.offsetCanvas)

    def clearoffsetScreen(self):
        self.offsetCanvas.Fill(0,0,0)

    # Display image on the given coordinates
    def showimage(self,x,y,imagepath):
        # Imports an Image from the given path, accepted are .jpg .gif .png
        self.im = Image.open(imagepath)
        self.xy = [0,0]
        self.xymax = self.im.size
        self.alpha = 255
        if self.im.mode == 'RGB':
            for self.xy[0] in range(0,self.xymax[0]):
                for self.xy[1] in range(0,self.xymax[1]):
                    self.tmp = (self.xy[0],self.xy[1])
                    self.red, self.green, self.blue = self.im.getpixel(self.tmp)
                    self.offsetCanvas.SetPixel(x + self.xy[0],y + self.xy[1],self.red,self.green,self.blue)
        elif self.im.mode == 'RGBA':
            for self.xy[0] in range(0,self.xymax[0]):
                for self.xy[1] in range(0,self.xymax[1]):
                    self.tmp = (self.xy[0],self.xy[1])
                    self.red, self.green, self.blue, self.alpha = self.im.getpixel(self.tmp)
                    if self.alpha > 50:
                        self.offsetCanvas.SetPixel(x + self.xy[0],y + self.xy[1],self.red,self.green,self.blue)

    # Textrenderer to display Text
    def drawtext(self,x,y,text,fonttype,red,green,blue,clear):
        self.fonthight = fonttype[fonttype.find('x')+1:len(fonttype)]
        if not self.fonthight.isdigit():
            self.fonthight = self.fonthight[0:len(self.fonthight)-1]
        self.fontwidth = fonttype[0:fonttype.find('x')]

        self.im = Image.new("I", (len(text)*int(self.fontwidth),int(self.fonthight)-1))
        self.draw = ImageDraw.Draw(self.im)
        self.font = ImageFont.load("/programs/rpi-rgb-led-matrix-master/fonts/" + fonttype + ".pil")
        self.draw.text((0, -1), text, font=self.font)
        self.xy = [0,0]
        self.xymax = self.im.size
        for self.xy[0] in range(0,self.xymax[0]):
            for self.xy[1] in range(0,self.xymax[1]):
               self.tmp = (self.xy[0],self.xy[1])
               if self.im.getpixel(self.tmp) > 0:
                   self.offsetCanvas.SetPixel(x + self.xy[0],y + self.xy[1],red,green,blue)
               elif clear == True:
                   self.offsetCanvas.SetPixel(x + self.xy[0],y + self.xy[1],0,0,0)


    def load_animations(self,path):
        # load and preprocess animations to speed up things as fast as possibel!
        global AnimationCanvas

        self.animation_length = [0]
        self.frame_delay = [0]
        self.anim_counter = 0
        AnimationCanvas = []
        path = path + '/*.gif'

        for self.infile in glob.glob(path):
            AnimationCanvas.append([])
            if self.anim_counter > 0:
                self.animation_length.append(1)
                self.frame_delay.append(1)
            self.animation_length[self.anim_counter] = self.anim_counter + 1
            self.im = Image.open(self.infile)
            self.frame_delay[self.anim_counter] = self.im.info['duration']
            self.frame_counter = 0

            try:
                while 1:
                    AnimationCanvas[self.anim_counter].append(0)
                    AnimationCanvas[self.anim_counter][self.frame_counter] = self.matrix.CreateFrameCanvas()
                    self.xy = [0,0]
                    self.xymax = self.im.size
                    self.image = self.im.convert('RGB')
                    for self.xy[0] in range(0,self.xymax[0]):
                        for self.xy[1] in range(0,self.xymax[1]):
                            self.tmp = (self.xy[0],self.xy[1])
                            self.red, self.green, self.blue = self.image.getpixel(self.tmp)
                            AnimationCanvas[self.anim_counter][self.frame_counter].SetPixel(self.xy[0],self.xy[1],
                                                                                            self.red,self.green,self.blue)
                    self.im.seek(self.im.tell()+1)
                    self.frame_counter = self.im.tell()
            except:
                pass

            self.animation_length[self.anim_counter] = self.frame_counter
            self.anim_counter += 1

        return self.animation_length, self.frame_delay

    def show_animation_image(self,animation_number,frame_number,Loop_play):
        global AnimationCanvas
        self.matrix.Swa (AnimationCanvas[animation_number][frame_number])
