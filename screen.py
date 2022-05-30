#!/usr/bin/env python3
import gi
from multiprocessing import Pipe
from threading import Thread

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk, GObject, Gdk

#<',=,~~
#   rat to eat bugs

class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()


#Get builder
builder = Gtk.Builder()
builder.add_from_file("/home/vms/raspi-datalogger-and-screen/screengui.glade")
builder.connect_signals(Handler())

#Get styling
cssProvider = Gtk.CssProvider() 
cssProvider.load_from_path("/home/vms/raspi-datalogger-and-screen/screen.css") 
context = Gtk.StyleContext()
screen = Gdk.Screen.get_default()
context.add_provider_for_screen(screen,cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

#Get objects in window
window = builder.get_object("window1")
bat_level = builder.get_object("levelBar1")

#Add color offsets to state of charge level bar
Gtk.LevelBar.add_offset_value(bat_level, Gtk.LEVEL_BAR_OFFSET_LOW, 0)
Gtk.LevelBar.add_offset_value(bat_level, Gtk.LEVEL_BAR_OFFSET_HIGH, 0)
Gtk.LevelBar.add_offset_value(bat_level, Gtk.LEVEL_BAR_OFFSET_FULL, 0)
Gtk.LevelBar.add_offset_value(bat_level, "low-offset", 0.33)
Gtk.LevelBar.add_offset_value(bat_level, "med-offset", 0.66)
Gtk.LevelBar.add_offset_value(bat_level, "high-offset", 1.0)

latGDisplay = builder.get_object("latGDisplay")
batTempDisplay = builder.get_object("batTempDisplay")
mphDisplay = builder.get_object("mphDisplay")
tcDisplay = builder.get_object("tcDisplay")
lapDisplay = builder.get_object("lapDisplay")
splitDisplay = builder.get_object("splitDisplay")

latGFrame = builder.get_object("latGFrame")
batFrame = builder.get_object("batTempFrame")
tcFrame = builder.get_object("tcFrame")

rat = builder.get_object("rat")

tcStyleContext = tcFrame.get_style_context()
bfStyleContext = batFrame.get_style_context()
latGStyleContext = latGFrame.get_style_context()
ratContext = rat.get_style_context()

#names are a holdover from past design, should be called laps
lap1 = builder.get_object("split1")
lap2 = builder.get_object("split2")
lap3 = builder.get_object("split3")
lap4 = builder.get_object("split4")
lap5 = builder.get_object("split5")
lap6 = builder.get_object("split6")

spContext = splitDisplay.get_style_context()

lp1Context = lap1.get_style_context()
lp2Context = lap2.get_style_context()
lp3Context = lap3.get_style_context()
lp4Context = lap4.get_style_context()
lp5Context = lap5.get_style_context()
lp6Context = lap6.get_style_context()

lapsTaken = 0;

#Update color of text using its style context
def update_text_color(styleContext, value):
    if value < 40:
        styleContext.remove_class("red")
        styleContext.remove_class("yellow")
        styleContext.add_class("lime")	
    elif value < 55:
        styleContext.remove_class("lime")
        styleContext.remove_class("red")
        styleContext.add_class("yellow")
    else:
        styleContext.remove_class("yellow")
        styleContext.remove_class("lime")
        styleContext.add_class("red")

#changes the text color of a specific split based on style context, and given value
def color_split( split):
    if split[1] == '-':
        spContext.remove_class("red")
        spContext.add_class("lime")
    elif split[0] == '+':
        spContext.remove_class("lime")
        spContext.add_class("red")
    else:
        spContext.remove_class("red")
        spContext.remove_class("lime")

#updates text colors of laps
def color_laps():
    global lapsTaken
    lapsTaken += 1
    if 1 <= lapsTaken:
        lp1Context.remove_class("white")
    if 2 <= lapsTaken:
        lp2Context.remove_class("white")
    if 3 <= lapsTaken:
        lp3Context.remove_class("white")
    if 4 <= lapsTaken:
        lp4Context.remove_class("white")
    if 5 <= lapsTaken:
        lp5Context.remove_class("white")
    if 6 <= lapsTaken:
        lp6Context.remove_class("white")

def color_battery():
    if batTempDisplay.get_text() == "OK":
        bfStyleContext.remove_class("back-red")	
        bfStyleContext.add_class("back-green")	
    else:
        bfStyleContext.remove_class("back-green")	
        bfStyleContext.add_class("back-red")	


def color_tc(tcState):
    if True == tcState:
        tcStyleContext.add_class("back-cyan")	
    else:
        tcStyleContext.remove_class("back-cyan")	

def color_latG(latG):
    if 1.5 <= latG:
        latGStyleContext.remove_class("back-green")	
        latGStyleContext.remove_class("back-yellow")	
        latGStyleContext.add_class("back-red")	
    elif 1.3 <= latG:
        latGStyleContext.remove_class("back-green")	
        latGStyleContext.remove_class("back-red")	
        latGStyleContext.add_class("back-yellow")	
    else:
        latGStyleContext.remove_class("back-yellow")	
        latGStyleContext.remove_class("back-red")	
        latGStyleContext.add_class("back-green")	


def color_rat(value):
    update_text_color(ratContext, value)


#provide updated values to the display by reading from a pipe
def update_thread(connection): 
    while 1:
        #get data from the pipe
        mph, soc, batStr, lapFormatted, splitFormatted, newLap, tcOn, latG = connection.recv() 

        #update labels
        GLib.idle_add(mphDisplay.set_text, str(mph))
        GLib.idle_add(batTempDisplay.set_text, batStr)
        GLib.idle_add(lapDisplay.set_text, lapFormatted)
        GLib.idle_add(bat_level.set_value, soc/100)
        GLib.idle_add(latGDisplay.set_text, "{:.2f}".format(latG))
        
        #change colors accordingly 
        GLib.idle_add(color_battery)
        GLib.idle_add(color_rat, mph)
        GLib.idle_add(color_tc, tcOn)
        GLib.idle_add(color_latG, latG)
    
        if True == newLap:
            GLib.idle_add(lap6.set_text, lap5.get_text())
            GLib.idle_add(lap5.set_text, lap4.get_text())
            GLib.idle_add(lap4.set_text, lap3.get_text())
            GLib.idle_add(lap3.set_text, lap2.get_text())
            GLib.idle_add(lap2.set_text, lap1.get_text())
            GLib.idle_add(lap1.set_text, lapFormatted)
            GLib.idle_add(splitDisplay.set_text, splitFormatted)
            GLib.idle_add(color_laps)
            GLib.idle_add(color_split, splitFormatted)
            
    
def init():
    #Run the screen
    window.show_all()
    window.fullscreen()
    
def start_screen():
    #start the screen
    init()
    Gtk.main()

def start_with_pipe(connection):
    #create and start the update daemon
    updateDaemon = Thread(target=update_thread, args=(connection,), daemon=True)
    updateDaemon.start()

    start_screen()


if __name__ == "__main__":
    start_screen()
