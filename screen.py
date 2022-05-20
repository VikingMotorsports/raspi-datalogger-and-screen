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

coolTempDisplay = builder.get_object("coolantTempDisplay")
batTempDisplay = builder.get_object("batTempDisplay")
mphDisplay = builder.get_object("mphDisplay")

coolFrame = builder.get_object("coolTempFrame")
batFrame = builder.get_object("batTempFrame")

rat = builder.get_object("rat")

cfStyleContext = coolFrame.get_style_context()
bfStyleContext = batFrame.get_style_context()
ratContext = rat.get_style_context()

lapDisplay = builder.get_object("lapDisplay")
splitDisplay = builder.get_object("splitDisplay")

split1 = builder.get_object("split1")
split2 = builder.get_object("split2")
split3 = builder.get_object("split3")
split4 = builder.get_object("split4")
split5 = builder.get_object("split5")
split6 = builder.get_object("split6")

splitAmount = 0;

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

#updates the background color of the object associated with the given style context
def update_background_color(styleContext, value):
    if value < 33:
        styleContext.remove_class("back-red")
        styleContext.remove_class("back-yellow")
        styleContext.add_class("back-green")	
    elif value < 66:
        styleContext.remove_class("back-green")
        styleContext.remove_class("back-red")
        styleContext.add_class("back-yellow")
    else:
        styleContext.remove_class("back-yellow")
        styleContext.remove_class("back-green")
        styleContext.add_class("back-red")

def color_cool(temp):
    update_background_color(cfStyleContext, temp)

def color_battery(temp):
    update_background_color(bfStyleContext, temp)

def color_rat(value):
    if(
    update_text_color(ratContext, value)

def update_split_color():

#provide updated values to the display by reading from a pipe
def update_thread(connection): 
    while True:
        #get data from the pipe
        mph, soc, coolTemp, batTemp, lapTime, newLap = connection.recv() 

        #update labels
        GLib.idle_add(mphDisplay.set_text, str(mph))
        GLib.idle_add(coolTempDisplay.set_text, str(coolTemp))
        GLib.idle_add(batTempDisplay.set_text, str(batTemp))
        GLib.idle_add(lapDisplay.set_text, lapTime)
        GLib.idle_add(bat_level.set_value, soc/100)
        if True == newLap:
            GLib.idle_add(split6.set_text, split5.get_text())
            GLib.idle_add(split5.set_text, split4.get_text())
            GLib.idle_add(split4.set_text, split3.get_text())
            GLib.idle_add(split3.set_text, split2.get_text())
            GLib.idle_add(split2.set_text, split1.get_text())
            GLib.idle_add(split1.set_text, splitDisplay.get_text())
            GLib.idle_add(splitDisplay.set_text, lapTime)

        #change colors accordingly 
        GLib.idle_add(color_cool, coolTemp)
        GLib.idle_add(color_battery, batTemp)
        GLib.idle_add(color_rat, mph)
    
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
