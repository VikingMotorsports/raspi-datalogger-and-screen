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
builder.add_from_file("screengui.glade")
builder.connect_signals(Handler())

#Get styling
cssProvider = Gtk.CssProvider()
cssProvider.load_from_path("screen.css")
context = Gtk.StyleContext()
screen = Gdk.Screen.get_default()
context.add_provider_for_screen(screen,cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

#Get objects in window
window = builder.get_object("window1")
battery = builder.get_object("levelBar1")

coolTempDisplay = builder.get_object("coolantTempDisplay")
batTempDisplay = builder.get_object("batTempDisplay")
motorTempDisplay = builder.get_object("motorTempDisplay")
mphDisplay = builder.get_object("mphDisplay")

coolFrame = builder.get_object("coolTempFrame")
batFrame = builder.get_object("batTempFrame")
motorFrame = builder.get_object("motorTempFrame")

rat = builder.get_object("rat")

cfStyleContext = coolFrame.get_style_context()
bfStyleContext = batFrame.get_style_context()
mfStyleContext = motorFrame.get_style_context()
ratContext = rat.get_style_context()

lapDisplay = builder.get_object("lapDisplay")

#open the styleing file
cssFile = open("screen.css", "r")

#Update color of rat using its style context
def update_rat(styleContext, value):
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

#provide updated values to the display by reading from a pipe
def update_thread(connection):

    while(1):
        #get data from the pipe
        mph, soc, coolTemp, batTemp, motTemp = connection.recv()

        #update diplays
        mphDisplay.set_text(str(mph))
        coolTempDisplay.set_text(str(coolTemp))
        batTempDisplay.set_text(str(batTemp))
        motorTempDisplay.set_text(str(motTemp))
        lapDisplay.set_text("TIME")
        battery.set_value(soc/100)

        #change colors accordingly
        update_background_color(cfStyleContext, coolTemp)
        update_background_color(bfStyleContext, batTemp)
        update_background_color(mfStyleContext, motTemp)
        update_rat(ratContext, mph)

def init():
    #Run the screen
    window.show_all()
    window.fullscreen()

def start_screen(connection):
    #create and start the update daemon
    updateDaemon = Thread(target=update_thread, args=(connection,), daemon=True)
    updateDaemon.start()

    #start the screen
    init()
    Gtk.main()

if __name__ == "__main__":
    start_screen()
