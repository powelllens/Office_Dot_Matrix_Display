# Office Dot Matrix Display
--
All software, description and required steps that are created during the development of the Office Dot Matrix Display

The Display is buildup with six 32x32 RGB LED Dot Matrix Display's in series, controlled by Raspberry Pi 2. 

To run the software, set up the config file and start officedisplay.py.
For console information during runtime, enable the debug var in the main file.

##Features:
* Welcome screen for visitors
* Logo mode to show the companys logo
* Employee mode to introduce the office employees with a funny sentence and an image
* Revenue counter mode (a value that is increased over the yaer in dollar)
* Quote mode for some funny random quotes
* soccer mode to show the first five table places
* hockey mode to show the first five table places
* animation mode to load and show .gif animations (see known bugs)

##ToDo before first start:
*Led library istalled for python (see hzeller instructions)
*All fonts are needed in .bdf
*The file locations in the could should be changed to the needed location

##Notes:
*The quote file is empty
*The image and animation location is empty
*The config xml file is nearly empty

##ToDo general:
*Set up a Log file for exeptions
*Set up Web-Server for config editing

##Known Bugs:
*The animation mode in combination with any other mode is still buggy and the display keeps flickering randomly
**(If you would like to use animations, you should load a seperate config for animations only)

The Library that ist used to control and handle the Display panels is from hzeller/rpi-rgb-led-matrix and can be found under:

<https://github.com/hzeller/rpi-rgb-led-matrix>

And is distributed under:
The LED-matrix **library** is (c) Henner Zeller <h.zeller@acm.org> with
GNU General Public License Version 2.0 <http://www.gnu.org/licenses/gpl-2.0.txt>





